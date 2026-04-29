#!/usr/bin/env python3
"""Run a contract's verification commands and emit a structured JSON verdict.

This is the canonical completion-verification executor. Used by:
  - harness-plan (Self-Test phase) — passes its current-contract.json
  - harness-engineering (implementation advance) — passes the impl contract
  - users directly — `/completion-verify` slash command

Input: a contract JSON. Either via --contract <path>, or
       --feature <features.json> --feature-id Fxxx (extracts the feature),
       or --stdin (reads contract from stdin).

Output: JSON to stdout with status pass/fail/partial/no_commands/error.

Exit codes:
  0 = status pass
  1 = status fail
  2 = status partial (some pass, manual checks still pending)
  3 = usage error / no commands / contract parse error
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_TIMEOUT = 300
TAIL_BYTES = 500
EVIDENCE_DIR_NAME = ".harness"  # mirrors harness-plan layout when a campaign exists


def utc_now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")


def _tail(s: str, n: int = TAIL_BYTES) -> str:
    if not s:
        return ""
    return s[-n:] if len(s) > n else s


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--contract", help="Path to contract JSON.")
    g.add_argument("--feature", help="Path to features.json (use with --feature-id).")
    g.add_argument("--stdin", action="store_true", help="Read contract JSON from stdin.")
    p.add_argument("--feature-id", help="Feature id to extract from --feature.")
    p.add_argument("--project-root", default=".",
                   help="Project root (cwd for command execution; default '.').")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                   help="Per-command timeout in seconds (default 300).")
    p.add_argument("--no-evidence-log", action="store_true",
                   help="Don't write a .harness/verify-*.log evidence file.")
    return p.parse_args()


def load_contract(args: argparse.Namespace) -> dict[str, Any] | None:
    """Return the contract dict, or None on parse error.

    A contract is recognized by having either a `verification_commands` field
    (harness-plan contract shape) or a `verification` field (raw feature shape).
    """
    if args.stdin:
        raw = sys.stdin.read()
        try:
            return json.loads(raw)
        except Exception as exc:
            print(json.dumps({"status": "error", "error": f"stdin parse: {exc}"}))
            sys.exit(3)
    if args.contract:
        path = Path(args.contract)
        if not path.exists():
            print(json.dumps({"status": "error", "error": f"contract not found: {path}"}))
            sys.exit(3)
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(json.dumps({"status": "error", "error": f"contract parse: {exc}"}))
            sys.exit(3)
    if args.feature and args.feature_id:
        path = Path(args.feature)
        if not path.exists():
            print(json.dumps({"status": "error", "error": f"features file not found: {path}"}))
            sys.exit(3)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(json.dumps({"status": "error", "error": f"features parse: {exc}"}))
            sys.exit(3)
        feats = data.get("features") if isinstance(data, dict) else data
        if not isinstance(feats, list):
            print(json.dumps({"status": "error", "error": "features.json shape unsupported"}))
            sys.exit(3)
        for f in feats:
            if f.get("id") == args.feature_id:
                return f
        print(json.dumps({"status": "error", "error": f"feature {args.feature_id} not found"}))
        sys.exit(3)
    print(json.dumps({"status": "error", "error": "must provide --contract, --feature+--feature-id, or --stdin"}))
    sys.exit(3)


def extract_commands(contract: dict[str, Any]) -> tuple[list[dict], list[str]]:
    """Return (verification_command_objs, manual_check_strings)."""
    commands: list[dict] = []
    manual: list[str] = []

    # harness-plan contract shape: verification_commands: [{command, expected_output?}]
    raw_cmds = contract.get("verification_commands") or []
    for entry in raw_cmds:
        if isinstance(entry, dict) and entry.get("command"):
            commands.append({
                "command": str(entry["command"]),
                "expected_output": entry.get("expected_output"),
            })
        elif isinstance(entry, str) and entry.strip():
            commands.append({"command": entry.strip(), "expected_output": None})

    # harness-plan feature shape: verification: {command, manual_check, expected}
    v = contract.get("verification")
    if isinstance(v, dict):
        if v.get("command"):
            commands.append({
                "command": str(v["command"]),
                "expected_output": v.get("expected"),
            })
        if v.get("manual_check"):
            manual.append(str(v["manual_check"]))
    elif isinstance(v, str) and v.strip():
        commands.append({"command": v.strip(), "expected_output": None})

    # explicit manual_checks list (harness-plan contract)
    explicit_manual = contract.get("manual_checks") or []
    for m in explicit_manual:
        if isinstance(m, str) and m.strip():
            manual.append(m.strip())
        elif isinstance(m, dict):
            desc = m.get("description") or m.get("check") or ""
            if desc:
                manual.append(str(desc))

    return commands, manual


def run_one(cmd_obj: dict, project_root: Path, timeout: int) -> dict:
    """Run a single command; return result dict."""
    command = cmd_obj["command"]
    expected = cmd_obj.get("expected_output")
    started = time.monotonic()
    timed_out = False
    exit_code: int | None = None
    stdout = ""
    stderr = ""
    try:
        proc = subprocess.run(
            command, shell=True, cwd=str(project_root),
            capture_output=True, text=True, timeout=timeout,
        )
        exit_code = proc.returncode
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
    except subprocess.TimeoutExpired as e:
        timed_out = True
        stdout = (e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")) or ""
        stderr = (e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")) or ""
    duration_ms = int((time.monotonic() - started) * 1000)

    matched_expected: bool | None = None
    if expected:
        # expected may be a substring or a regex (we try both)
        try:
            matched_expected = bool(re.search(expected, stdout, re.MULTILINE))
        except re.error:
            matched_expected = expected in stdout

    return {
        "command": command,
        "exit_code": exit_code,
        "stdout_tail": _tail(stdout),
        "stderr_tail": _tail(stderr),
        "duration_ms": duration_ms,
        "timed_out": timed_out,
        "matched_expected": matched_expected,
        "expected_output": expected,
    }


def derive_status(results: list[dict], manual_pending: list[str]) -> str:
    if not results and not manual_pending:
        return "no_commands"
    if not results and manual_pending:
        return "partial"
    all_passed = all(
        (r["exit_code"] == 0) and (r["matched_expected"] is not False) and not r["timed_out"]
        for r in results
    )
    if all_passed and not manual_pending:
        return "pass"
    if all_passed and manual_pending:
        return "partial"
    return "fail"


def derive_contract_id(contract: dict[str, Any]) -> str:
    return (
        contract.get("id")
        or contract.get("feature_id")
        or contract.get("contract_id")
        or "unknown"
    )


def write_evidence_log(project_root: Path, contract_id: str, results: list[dict]) -> str | None:
    """Write a .harness/verify-*.log file. Return its path, or None if skipped."""
    target_dir = project_root / EVIDENCE_DIR_NAME
    if not target_dir.exists():
        # Don't auto-create the dir; only log when one is already present
        # (i.e., we're inside a harness-plan campaign).
        return None
    log_path = target_dir / f"verify-{contract_id}-{utc_now_compact()}.log"
    try:
        with log_path.open("w", encoding="utf-8") as fh:
            fh.write(f"# completion-verify evidence for {contract_id}\n\n")
            for r in results:
                fh.write(f"## {r['command']}\n")
                fh.write(f"exit_code: {r['exit_code']}  duration_ms: {r['duration_ms']}  "
                         f"timed_out: {r['timed_out']}  matched_expected: {r['matched_expected']}\n\n")
                fh.write("--- stdout (tail) ---\n")
                fh.write(r["stdout_tail"] + "\n\n")
                fh.write("--- stderr (tail) ---\n")
                fh.write(r["stderr_tail"] + "\n\n")
        return str(log_path.relative_to(project_root))
    except Exception:
        return None


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    contract = load_contract(args)

    cmd_objs, manual = extract_commands(contract)
    contract_id = derive_contract_id(contract)

    results = [run_one(c, project_root, args.timeout) for c in cmd_objs]
    status = derive_status(results, manual)

    evidence: str | None = None
    if not args.no_evidence_log and results:
        evidence = write_evidence_log(project_root, contract_id, results)

    out = {
        "status": status,
        "contract_id": contract_id,
        "verifications": results,
        "manual_checks_pending": manual,
        "evidence_log": evidence,
    }
    print(json.dumps(out, indent=2))

    return {
        "pass": 0,
        "fail": 1,
        "partial": 2,
        "no_commands": 3,
        "error": 3,
    }.get(status, 3)


if __name__ == "__main__":
    raise SystemExit(main())
