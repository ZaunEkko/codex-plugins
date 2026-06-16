<div align="center">

# 🧩 Codex Plugins

### 个性化 Codex 工作流市场

*把顺手的 plugins、skills、hooks 和提示词风格，打包成别人也能安装的能力*

[![Codex](https://img.shields.io/badge/Codex-Workflow-111827.svg)](https://developers.openai.com/codex)
[![Marketplace](https://img.shields.io/badge/Marketplace-ZaunEkko-orange.svg)]()
[![Plugins](https://img.shields.io/badge/Includes-Plugins-blue.svg)]()
[![Hooks](https://img.shields.io/badge/Supports-Hooks-brightgreen.svg)]()

</div>

---

## ✨ 这个仓库是什么

这是一个面向 Codex 的个人工作流 marketplace。

它不是只放一个插件的仓库，而是用来持续沉淀一组可复用的 Codex 个性化能力：插件、skills、hooks、启动上下文、输出风格和开发辅助流程。目标是把平时用着顺手的 Codex 配置打包起来，让别人也可以直接安装、启用和复用。

---

## 🧰 收录范围

<table>
<tr>
<td width="50%">

### 🧩 Plugins
完整的 Codex 插件包，可以包含 manifest、hooks、skills、MCP 配置或其他可安装能力。

</td>
<td width="50%">

### 🧠 Skills
可复用的任务工作流，让 Codex 在特定场景下按固定方法做事。

</td>
</tr>
<tr>
<td width="50%">

### ⚡ Hooks
在 Codex 生命周期事件中自动运行脚本，例如 session start、tool use、stop 等。

</td>
<td width="50%">

### 🎨 Presets
输出风格、协作习惯、项目启动上下文等可以复用的个性化设置。

</td>
</tr>
</table>

---

## 📦 当前内容

<table>
<tr>
<td width="50%">

### 💡 explanatory-output-style
让 Codex 在会话启动时进入解释型输出风格，写代码时补充简短、贴近当前代码库的实现思路。

</td>
<td width="50%">

### 🧷 类型
`Plugin` + `SessionStart Hook`

通过 `startup`、`resume`、`clear`、`compact` 事件注入额外上下文。

</td>
</tr>
</table>

---

## 🚀 快速开始

### 📦 添加 marketplace

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
```

### 🧩 安装当前插件

```bash
codex plugin add explanatory-output-style@zaunekko
```

### 🔐 信任 hook

包含 command hook 的插件首次运行前需要在 Codex 中 review 并 trust。

```text
/hooks
```

---

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

- 希望 Codex 不只给结果，也解释实现选择
- 希望把常用提示词变成可安装插件
- 希望给团队或朋友共享同一套 Codex 工作方式

---

## 🏗️ 仓库结构

```text
codex-plugins/
├── .agents/
│   └── plugins/
│       └── marketplace.json          # Codex marketplace 入口
├── plugins/
│   └── explanatory-output-style/
│       ├── .codex-plugin/
│       │   └── plugin.json           # 插件 manifest
│       └── hooks/
│           ├── hooks.json            # SessionStart hook 配置
│           └── session_start.py      # additionalContext 输出脚本
└── README.md
```

未来可能扩展：

```text
codex-plugins/
├── plugins/                          # 可安装插件
├── skills/                           # 独立 skills 或 skill 模板
├── hooks/                            # 可复用 hook 脚本
└── presets/                          # 输出风格和工作流预设
```

---

## 🧭 Roadmap

| 类型 | 方向 | 状态 |
|------|------|------|
| 输出风格 | explanatory-output-style | ✅ 已提供 |
| 项目上下文 | 自动注入项目约定、目录说明、常用命令 | 🧪 计划中 |
| Review 风格 | 固定代码审查口径和检查清单 | 🧪 计划中 |
| 开发辅助 | 常用开发流程 skills | 🧪 计划中 |
| Hook 自动化 | session/tool/stop 生命周期脚本 | 🧪 计划中 |

---

## 🧪 本地验证

```bash
# 查看 marketplace 是否被 Codex 识别
codex plugin list

# 校验当前 hook 脚本语法
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py

# 直接查看 hook 输出
python plugins/explanatory-output-style/hooks/session_start.py
```

---

## ⚠️ Trust & Safety

<table>
<tr>
<td>

### ✅ 推荐做法
- 安装前看清插件说明
- 在 `/hooks` 中 review command hook
- 改动 hook 后重新 trust

</td>
<td>

### ❌ 不建议
- 盲目信任未知脚本
- 把敏感信息写进 hook 输出
- 在没确认用途时启用自动化脚本

</td>
</tr>
</table>

---

<div align="center">

### 💬 维护

这个仓库会持续收集和整理 Codex 的个人化插件、skills、hooks 与工作流预设。

**Made for reusable Codex workflows by ZaunEkko**

</div>
