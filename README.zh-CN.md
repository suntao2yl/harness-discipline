# harness-discipline

[English](README.md) | [中文](README.zh-CN.md)

可复用的 AI-Coding 工程纪律 skill,既可以被
`harness-plan` / `harness-engineering` 组合调用,也可以独立使用。

## Skills 一览

### 核心(被 harness-plan / harness-engineering 调用)

| Slash command        | 作用                                                       |
| -------------------- | ---------------------------------------------------------- |
| `/tdd-plan`          | 测试优先计划:test cases + 实现骨架 + verification command |
| `/completion-verify` | 跑一份 contract 的 verification commands,产出 JSON 判定    |
| `/change-spec`       | 为 change unit (CHG-NNN) 生成 mini-RFC                      |

### 工程实践(独立使用)

| Skill 名         | 作用                                                                   |
| ---------------- | ---------------------------------------------------------------------- |
| `tdd`            | 红-绿-重构循环,垂直切片,测试不依赖实现细节                          |
| `write-a-skill`  | 写新 skill / 重构旧 skill 的方法学:progressive disclosure、≤100 行 |

### Autodrive 推荐(token / 安全)

| Skill 名         | 作用                                                                   |
| ---------------- | ---------------------------------------------------------------------- |
| `caveman`        | 超压缩输出模式,token 用量降 ~75%,技术内容无损                        |
| `git-guardrails` | 装一个 PreToolUse hook 拦截危险 git 命令(push / reset --hard 等)     |

每个 skill 独立,有自己的 SKILL.md(均 ≤100 行),可以单独被调用 ——
按需加载,不会一起打入 context。

后四个独立 skill(`tdd` / `write-a-skill` / `caveman` / `git-guardrails`)
改编自 [mattpocock/skills](https://github.com/mattpocock/skills),MIT。

## 为什么单独成包

`harness-plan` 和 `harness-engineering` 都需要 TDD 计划、完成度验证、
change spec 这三件能力。在本插件之前,这些能力以 prose 散落在两份
SKILL.md 里。抽到这里后:

- 消除重复与漂移
- 用户可以在 campaign 之外直接调用这些纪律
- 对齐 AI Coding 工程化的 OpenSpec / Superpowers / Harness 三层模型

能力归属的标准对照表见
`harness-engineering/docs/dedup-matrix.md`。

## 安装

### Claude Code

```bash
/plugin marketplace add suntao2yl/harness-discipline
/plugin install harness-discipline@harness-discipline-marketplace
```

安装后,`/tdd-plan` / `/completion-verify` / `/change-spec` 三个 slash
command 直接可用。

### Codex

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo suntao2yl/harness-discipline \
  --path plugins/harness-discipline/skills/tdd-plan
# 同样命令再装另外两个 skill,只换 --path 末段
```

## 用法快览

### `/tdd-plan`

输入:feature 描述、`--feature-id F003`,或 `--contract <path>`。

输出:JSON,字段包含 `framework_detected`、`test_cases`、
`implementation_skeleton`、`verification_command`。

```bash
/tdd-plan "build a CSV exporter with quote/escape handling"
/tdd-plan --feature-id F003
/tdd-plan --contract .harness/current-contract.json
```

输出 schema 详见 `skills/tdd-plan/resources/tdd-plan-template.md`。

### `/completion-verify`

输入:contract 路径、features.json + feature-id,或 stdin JSON。

输出:JSON,`status` 五种 — `pass` / `fail` / `partial` / `no_commands` /
`error`。退出码与 status 对应:0/1/2/3/3。

```bash
/completion-verify --contract .harness/current-contract.json
/completion-verify --feature .harness/features.json --feature-id F003
echo '{"id":"F","verification_commands":[{"command":"pytest"}]}' | /completion-verify --stdin
```

`.harness/` 存在时自动写入 `verify-<contract_id>-<ts>.log` 取证文件。
完整协议见 `skills/completion-verify/resources/completion-verify-protocol.md`。

### `/change-spec`

输入:change 描述,或 `--feature-id F003`。

输出:写入 markdown 文件(默认 `.harness/changes/CHG-NNN/spec.md`,
engineering 项目里写到 `.engineering/design/specs/`),并打印一行
`WROTE <path>`。

```bash
/change-spec "add CSV column-selector flag"
/change-spec --feature-id F003 --change-id CHG-002
/change-spec --output docs/specs/CHG-001.md --description "..."
```

输出格式与 lint 规则见
`skills/change-spec/resources/change-spec-schema.md`。

## 与上游 skill 的协作

| 上游               | 调用 discipline 的位置                       |
| ------------------ | -------------------------------------------- |
| harness-plan       | INIT 阶段调 `/tdd-plan`,Self-Test 阶段调 `/completion-verify` |
| harness-engineering | design phase 调 `/change-spec`,implementation advance 调 `/completion-verify` |

未装 discipline 时,两个上游 skill 都有内联 fallback(结论一致,
evidence 结构化程度低一点)。

## Autodrive 联动

`harness-plan autodrive on` 之后,无人值守跑 campaign。推荐同时启用:

- `caveman` — token 大幅降低,日志仍可读
- `git-guardrails` — 安装 hook 拦截 `git push` / `reset --hard` 等不可逆操作

两者只需各装一次,所有 autodrive session 自动生效。

## License

MIT
