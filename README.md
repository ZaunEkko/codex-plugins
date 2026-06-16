<div align="center">

# 🧩 Codex Plugins

### 给 Codex 准备的一组个人工作流插件

*让 Codex 在启动时就进入你想要的协作状态*

[![Codex](https://img.shields.io/badge/Codex-Plugin-111827.svg)](https://developers.openai.com/codex)
[![Hooks](https://img.shields.io/badge/Powered%20by-SessionStart-blue.svg)]()
[![Marketplace](https://img.shields.io/badge/Marketplace-ZaunEkko-orange.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Local%20Codex-brightgreen.svg)]()

</div>

---

## ✨ 插件列表

<table>
<tr>
<td width="50%">

### 💡 explanatory-output-style
在 Codex 会话启动时注入解释型输出风格，让 Codex 在写代码时补充简短、贴近当前代码库的实现思路。

</td>
<td width="50%">

### ⚡ SessionStart Hook
通过 `startup`、`resume`、`clear`、`compact` 事件自动加载，不需要每次手动复制提示词。

</td>
</tr>
</table>

---

## 🚀 快速开始

### 📦 安装 marketplace

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
```

### 🧩 安装插件

```bash
codex plugin add explanatory-output-style@zaunekko
```

### 🔐 信任 Hook

这个插件使用 `SessionStart` hook。首次安装或 hook 内容变更后，Codex 会要求你在 `/hooks` 中 review 并 trust。

```text
/hooks
```

---

## 🎯 使用效果

安装并信任 hook 后，新开一个 Codex thread，插件会在会话启动阶段注入额外上下文。

```text
Codex Session Start
        ↓
explanatory-output-style hook
        ↓
additionalContext 注入
        ↓
Codex 使用解释型输出风格协作
```

输出风格会倾向于：

- 说明为什么这样改，而不只是贴结果
- 聚焦当前代码库的约定、权衡和实现选择
- 在写代码前后给出紧凑的 insight block

---

## 🏗️ 插件结构

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

---

## ⚙️ 核心配置

### marketplace

| 字段 | 当前值 | 说明 |
|------|--------|------|
| `name` | `zaunekko` | marketplace 名称 |
| `source.path` | `./plugins/explanatory-output-style` | 插件目录 |
| `installation` | `AVAILABLE` | 可安装 |
| `authentication` | `ON_INSTALL` | 安装时处理认证/信任流程 |

### hook

| 事件 | matcher | 作用 |
|------|---------|------|
| `SessionStart` | `startup\|resume\|clear\|compact` | 在会话启动、恢复、清空和压缩后注入风格上下文 |

---

## 🧪 本地验证

```bash
# 检查插件是否被 marketplace 识别
codex plugin list

# 校验 hook 脚本语法
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py

# 直接查看 hook 输出
python plugins/explanatory-output-style/hooks/session_start.py
```

---

## ⚠️ 注意事项

<table>
<tr>
<td>

### ✅ 适合
- 想让 Codex 多解释实现思路
- 想复用固定输出风格
- 想把提示词做成可安装插件

</td>
<td>

### ❌ 不适合
- 每次都要求极简输出
- 不希望 hook 注入任何上下文
- 没有信任本地 command hook

</td>
</tr>
</table>

---

<div align="center">

### 💬 维护

个人 Codex 插件市场，用来沉淀可复用的本地工作流。

**Made for Codex workflows by ZaunEkko**

</div>
