# crush.skill 详细安装说明

## Claude Code 安装

### 全局安装（推荐）

在终端执行以下命令，将 crush.skill 安装到 Claude Code 全局 skills 目录：

```shell
git clone https://github.com/NatalieCao323/crush-skill ~/.claude/skills/crush
```

### 项目级安装

如果你只想在某个项目中使用，在该项目根目录执行：

```shell
mkdir -p .claude/skills
git clone https://github.com/NatalieCao323/crush-skill .claude/skills/crush
```

### 验证安装

安装完成后，打开 Claude Code，输入：

```
/create-crush
```

如果看到 crush.skill 的引导信息，说明安装成功。

---

## OpenClaw 安装

[OpenClaw](https://openclaw.ai) 是一个兼容 Claude Code Skill 格式的开源 AI Agent 框架，支持在本地或服务器上运行 Skill。

### 安装步骤

```shell
git clone https://github.com/NatalieCao323/crush-skill ~/.openclaw/workspace/skills/crush
```

### 验证安装

启动 OpenClaw 后，在对话框中输入：

```
/create-crush
```

### OpenClaw 特有功能

在 OpenClaw 中使用 crush.skill，额外支持：

- **批量分析**：同时导入多个聊天记录文件，自动合并分析
- **历史版本**：每次更新 crush 档案都会自动存档，支持回滚
- **导出报告**：将体检报告导出为 PDF 或 Markdown 文件

---

## 网页版 Claude（无需安装）

不需要安装任何工具，直接用 Claude Projects 运行，详见 [WEB_TUTORIAL.md](WEB_TUTORIAL.md)。

---

## 依赖安装

```shell
cd ~/.claude/skills/crush  # 或你的安装路径
pip3 install -r requirements.txt
```

依赖均为轻量级库，安装时间约 10 秒。

---

## 微信聊天记录导出指南

要分析 crush，你需要先导出聊天记录。以下是推荐工具：

### WeChatMsg（推荐，Windows）

- GitHub：https://github.com/LC044/WeChatMsg
- 支持系统：Windows
- 导出格式：txt / html / csv
- 使用方法：下载安装 → 登录微信 PC 版 → 选择联系人 → 导出为 txt

### 留痕（macOS）

- 支持系统：macOS
- 导出格式：JSON
- 适合 Mac 用户

### PyWxDump（高级用户）

- GitHub：https://github.com/xaoyaoo/PyWxDump
- 支持系统：Windows
- 导出格式：SQLite 数据库

### 手动复制粘贴（最简单）

1. 在微信中打开与 crush 的聊天窗口
2. 手动选择并复制关键对话（建议至少 30 条）
3. 粘贴到一个 `.txt` 文件，格式如下：

```
小明: 要是你在就好了
我: 我也想你啊
小明: 哦
小明: 最近很忙，改天吧
小明: 睡了吗
```

---

## 使用方法

安装完成后，在 Claude Code 或 OpenClaw 中按以下步骤操作：

### 第一步：创建 crush 档案

```
/create-crush
```

Claude 会引导你：
1. 输入 crush 的名字/昵称
2. 上传聊天记录文件（或粘贴文本）
3. 补充主观描述（ta 是什么样的人？你们是怎么认识的？）

### 第二步：查看体检报告

```
/{slug}-report
```

输出内容包括：
- 贝叶斯升温指数（0-100，越高越有戏）
- 依恋类型诊断（回避型/焦虑型/安全型/恐惧-回避型）
- 心理环境分析（10 种情景）
- 下一步行动建议 + 逐字话术

### 第三步：聊天演习

```
/{slug}
```

Claude 会完全模仿对方的语气、回复节奏、口头禅，陪你演习下一次对话。

### 其他命令

| 命令 | 说明 |
|---|---|
| `/list-crushes` | 列出所有已创建的 crush 档案 |
| `/update-crush {slug}` | 追加新的聊天记录 |
| `/delete-crush {slug}` | 删除某个档案 |
| `/wake-up {slug}` | 清醒了，删除档案，"下一个更乖" |

---

## 常见问题

### Q: 数据会上传到云端吗？

A: 不会。所有数据都存储在你的本地文件系统中，不会上传到任何服务器。Claude Code 和 OpenClaw 在本地运行，聊天记录只在你的电脑上处理。

### Q: 可以同时分析多个 crush 吗？

A: 可以。每个 crush 会生成独立的 `crushes/{slug}/` 目录，互不干扰。

### Q: 支持 QQ 聊天记录吗？

A: 支持。QQ 导出步骤：打开 QQ → 左下角 ≡ → 设置 → 通用 → 聊天记录 → 导出为 txt → 在 `/create-crush` 时上传。

### Q: 贝叶斯升温指数是什么？

A: 每条消息都会被打上三个标签：
- **先验置信度**：这句话是不是 ta 的真实意图（0-1）
- **时间衰减系数**：越久的消息权重越低
- **情绪关联强度**：吵架/开心的事权重拉满

最终升温权重 = 先验置信度 × e^(-衰减×天数) × (1 + 情绪强度)

### Q: Claude Code 和 OpenClaw 有什么区别？

A: Claude Code 是 Anthropic 官方的命令行工具，需要 Claude Pro 订阅。OpenClaw 是开源框架，支持接入多种 LLM（包括本地模型），适合有技术背景的用户。crush.skill 两者均支持。

### Q: 安装后没有反应怎么办？

A: 确认 `~/.claude/skills/crush/SKILL.md`（或 `~/.openclaw/workspace/skills/crush/SKILL.md`）文件是否存在，并重启 Claude Code / OpenClaw。

---

⚠️ **本项目仅用于个人情感分析，不用于骚扰、跟踪或侵犯他人隐私。**
