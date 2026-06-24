<div align="center">

# 🧩 Codex Plugins

### 个性化 Codex 工作流市场

*把顺手的 plugins、skills、hooks 和提示词风格，打包成别人也能安装的能力*

[简体中文](README.md) · [English](i18n/en/README.md) · [繁體中文](i18n/zh-TW/README.md) · [日本語](i18n/ja/README.md) · [한국어](i18n/ko/README.md)

[![Codex](https://img.shields.io/badge/Codex-Workflow-111827.svg)](https://developers.openai.com/codex)
[![Marketplace](https://img.shields.io/badge/Marketplace-ZaunEkko-orange.svg)]()
[![Plugins](https://img.shields.io/badge/Includes-Plugins-blue.svg)]()
[![Hooks](https://img.shields.io/badge/Supports-Hooks-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## ✨ 这个仓库是什么

这是一个面向 Codex 的个人工作流 marketplace，用来持续沉淀可复用的 Codex 个性化能力：插件、skills、hooks、启动上下文、输出风格和开发辅助流程。

目标是把平时用着顺手的 Codex 配置打包起来，让别人也可以直接安装、启用和复用。

## 🧰 收录范围

| 类型 | 说明 |
|------|------|
| Plugins | 完整的 Codex 插件包，可以包含 manifest、hooks、skills、MCP 配置或其他可安装能力。 |
| Skills | 可复用的任务工作流，让 Codex 在特定场景下按固定方法做事。 |
| Hooks | 在 Codex 生命周期事件中自动运行脚本，例如 session start、tool use、stop 等。 |
| Presets | 输出风格、协作习惯、项目启动上下文等可以复用的个性化设置。 |

## 📦 当前内容

| 插件 | 类型 | 说明 | 文档 |
|------|------|------|------|
| explanatory-output-style | Plugin + SessionStart Hook | 把 Claude Code 官方 explanatory-output-style 插件的解释型协作体验适配到 Codex。 | [插件文档](docs/explanatory-output-style/README.md) |

## 🚀 快速开始

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add explanatory-output-style@zaunekko
```

包含 command hook 的插件首次运行前需要在 Codex 中 review 并 trust：

```text
/hooks
```

## 🎯 使用方式

安装并信任后，新开一个 Codex thread。当前插件会在会话启动阶段注入额外上下文：

```text
Codex Session Start
        ↓
explanatory-output-style
        ↓
additionalContext 注入
        ↓
Codex 使用解释型输出风格协作
```

适合这些场景：

- 希望 Codex 不只给结果，也解释实现选择。
- 希望把常用提示词变成可安装插件。
- 希望给团队或朋友共享同一套 Codex 工作方式。

## 📚 插件文档

每个插件单独维护文档，根 README 只保留入口导航：

- [explanatory-output-style](docs/explanatory-output-style/README.md)：解释型输出风格插件说明、安装、hook 信任方式和本地验证命令。

## 🏗️ 仓库结构

```text
codex-plugins/
├── .agents/plugins/marketplace.json
├── .github/workflows/ci.yml
├── docs/<plugin-name>/README.md
├── plugins/<plugin-name>/.codex-plugin/plugin.json
├── plugins/<plugin-name>/hooks/
├── tests/
└── README.md
```

## 🧭 Roadmap

| 类型 | 方向 | 状态 |
|------|------|------|
| 输出风格 | explanatory-output-style | ✅ 已提供 |
| 项目上下文 | 自动注入项目约定、目录说明、常用命令 | 🧪 计划中 |
| Review 风格 | 固定代码审查口径和检查清单 | 🧪 计划中 |
| 开发辅助 | 常用开发流程 skills | 🧪 计划中 |
| Hook 自动化 | session/tool/stop 生命周期脚本 | 🧪 计划中 |

## 🧪 本地验证

```bash
codex plugin list
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py
python plugins/explanatory-output-style/hooks/session_start.py
python -m unittest tests.test_explanatory_output_style
```

## ⚠️ Trust & Safety

- 安装前看清插件说明。
- 在 `/hooks` 中 review command hook。
- 改动 hook 后重新 trust。
- 不要把 API key、token、密码或机器专属路径写进 hook 输出。

## 📄 许可证

本项目使用 [MIT License](LICENSE) 开源。

## 🤝 社区与贡献

- [Contributing](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

<div align="center">

**Made for reusable Codex workflows by ZaunEkko**

</div>
