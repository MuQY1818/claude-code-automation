<div align="center">
  <img src="assets/logo.png" alt="Claude Code 自动化系统" width="200"/>
  
# Claude Code 自动化系统
</div>

[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/downloads/)
[![版本](https://img.shields.io/badge/版本-v2.0.0-green.svg)](https://github.com/anthropics/claude-code)
[![许可证](https://img.shields.io/badge/许可证-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/claude--code-automation-purple.svg)](https://claude.ai/code)

**增强的 Claude Code 自动化框架，具备智能钩子、自定义命令和双语文档生成功能。**

这个仓库提供了一个复杂的双层自动化系统，通过上下文感知的提示修改、高级开发工作流程和智能项目分析来扩展 Claude Code 的功能。

## 功能特性

### **原生钩子系统**
- **UserPromptSubmit 钩子** - 基于上下文的智能提示修改
- **超级思考模式** - 为复杂问题提供深度分析提示
- **简洁回应** - 对简单查询自动提供简短答案
- **学习支持** - 为教育场景提供增强解释
- **摘要模式** - 项目感知的 `-d` 标志处理

### **自定义命令系统**
- **11 个专业命令** - 高级开发工作流程自动化
- **安全分析** (`/security`) - 多层漏洞扫描
- **PR 创建** (`/create-PR`) - 智能拉取请求生成
- **代码重构** (`/refactor`) - 具备分支安全保护的上下文感知代码改进
- **文件审查** (`/file-review`) - 综合代码分析
- **Git 提交** (`/git-commit`) - 超级思考驱动的提交信息生成
- **项目清理** (`/clean-project`) - 具备 git 保护的安全项目清理
- **双语文档** (`/create-readme`, `/update-readme`) - 带备份功能的英文/中文 README 自动化

### **上下文智能**
- **项目检测** - 自动识别项目类型（Web、Python、Java、Rust、Go、Docker）
- **语言分析** - 智能检测编程语言和框架
- **Git 集成** - 分支跟踪、变更分析和提交智能
- **工具验证** - 先决条件检查和环境验证

## 安装

### 先决条件
- **Python 3.8+** （用于自动化框架）
- **Claude Code CLI** 已安装并配置
- **Git** 用于版本控制功能
- **GitHub CLI** (`gh`) 用于 PR 创建（可选）
- **Node.js/npm** 或相关包管理器（取决于项目）

### 设置
```bash
# 克隆仓库
git clone https://github.com/muqy1818/claude-code-automation.git
cd claude-code-automation

# .claude/ 配置已为此项目准备就绪
# 在此目录使用 Claude Code 时，钩子系统将自动激活

# 全局安装（可选）：
# cp .claude/settings.json ~/.claude/settings.json
```

## 快速开始

### 1. **启用钩子系统**
当您在此目录中使用 Claude Code 时，钩子系统会自动激活：

```bash
# 测试 -d 摘要模式
echo "解释钩子如何工作 -d" | claude

# 测试超级思考模式
echo "设计可扩展的微服务架构" | claude
```

### 2. **使用自定义命令**
通过斜杠命令访问高级自动化：

```bash
# 生成安全分析
/security

# 安全清理项目（新功能）
/clean-project --dry-run

# 创建智能 README（双语）
/create-readme --lang=both --style=standard

# 智能 PR 创建
/create-PR --draft

# 上下文感知重构（安全：需要新分支）
/refactor --type=performance
```

## 使用方法

### 钩子系统
自动化系统通过 **两层** 运作：

#### **第一层：原生 Claude Code 钩子**
- 在到达 Claude 之前修改提示
- 在 `.claude/settings.json` 中配置
- 按序执行：ultrathink → answer_in_short → explain → default

```bash
# 钩子激活示例
"复杂算法设计问题"                    # → 触发超级思考
"什么是 Python？"                    # → 触发简洁回应
"帮我学习递归"                       # → 触发解释模式
"优化这段代码 -d"                    # → 触发摘要模式
```

#### **第二层：自定义命令系统**
- 高级开发工作流程
- 上下文感知执行
- 由 `/core` Python 框架驱动

### 自定义命令

#### **文档命令**
```bash
# 生成新的 README
/create-readme --lang=en --style=comprehensive
/create-readme --lang=zh --style=minimal
/create-readme --lang=both --style=standard

# 更新现有 README
/update-readme --sections=installation,usage
/update-readme --lang=both --preserve=true
```

#### **开发命令**
```bash
# 安全分析
/security secrets              # 扫描硬编码秘密
/security dependencies         # 检查易受攻击的依赖
/security full                # 完整安全审计

# 项目清理（新功能）
/clean-project --dry-run       # 预览清理（安全）
/clean-project --mode=moderate # 更彻底的清理
/clean --mode=safe            # 基本清理的别名

# 代码改进（安全：使用功能分支）
git checkout -b refactor/improvements
/refactor src/                # 重构特定目录
/refactor --type=pattern      # 提取模式并减少重复
/file-review --focus=security # 以安全为重点的代码审查
```

#### **Git 集成**
```bash
# 智能提交生成
/git-commit --dry-run         # 预览生成的提交信息
/git-commit --type=feat       # 覆盖自动检测
/commit --style=conventional  # 使用传统提交的别名

# 拉取请求管理
/create-PR main               # 针对主分支创建 PR
/create-PR --draft            # 创建草稿 PR
/push-to-github              # 经过验证的 git 推送
/explain-pull-request        # 记录架构变更
```

## 架构

系统使用具备全面安全措施的 **双层架构**：

### **核心组件**
- **上下文管理器** (`core/context_manager.py`) - 项目智能和检测
- **命令注册表** (`core/command_registry.py`) - 命令执行和验证
- **钩子调度器** (`core/hook_dispatcher.py`) - 命令级钩子管理
- **原生钩子** (`hooks/UserPromptSubmit/`) - 提示修改脚本

### **安全特性**
- **分支保护** - 修改文件的命令需要功能分支
- **备份创建** - 破坏性操作前自动备份
- **预览模式** - 执行前预览更改
- **Git 安全** - 永不触及主/master分支的危险操作

### **配置系统**
- **原生钩子**：`.claude/settings.json` (Claude Code 格式)
- **自定义命令**：`.claude/settings/commands.json` (命令定义)
- **全局设置**：`.claude/settings/global.json` (系统默认值)
- **项目设置**：`.claude/settings/project.json` (项目特定覆盖)

## 双语支持

系统提供全面的双语文档生成：

### **语言选项**
- `--lang=en` - 英文文档（默认）
- `--lang=zh` - 中文文档
- `--lang=both` - 生成两种语言版本

### **技术方法**
- **英文为主** - 主要文档语言
- **中文本地化** - 技术准确性与文化适应
- **一致结构** - 跨语言的镜像部分
- **技术术语** - 保留英文技术词汇

## 贡献

1. **Fork 仓库**
2. **创建功能分支**：`git checkout -b feature/amazing-feature`
3. **进行更改** 并彻底测试
4. **运行钩子系统测试**：使用各种提示类型进行测试
5. **提交更改**：`git commit -m '添加惊人功能'`
6. **推送到分支**：`git push origin feature/amazing-feature`
7. **开启拉取请求** 使用 `/create-PR` 命令

### **开发环境设置**
```bash
# 克隆并设置
git clone https://github.com/muqy1818/claude-code-automation.git
cd claude-code-automation

# 测试钩子系统
echo "测试提示 -d" | python .claude/hooks/UserPromptSubmit/append_default.py

# 测试命令系统（可能需要Python路径设置）
# 命令通过 Claude Code 接口工作，不是直接执行

# 测试安全特性
/clean-project --dry-run      # 应显示预览而不更改
```

## 许可证

本项目在 MIT 许可证下授权 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 安全指南

### **分支安全**
修改文件的命令（`/refactor`、`/header-comments`）需要功能分支：
```bash
git checkout -b feature/your-changes
/refactor  # 现在运行安全
```

### **备份保护**
文档命令（`/create-readme`、`/update-readme`）自动创建备份：
```bash
/update-readme  # 创建 backups/README.md.backup.TIMESTAMP
```

## 致谢

- **Anthropic** - 提供 Claude Code 平台和 API
- **Claude Code 社区** - 提供自动化模式和最佳实践
- **贡献者** - 提供功能增强和错误修复

---

**用心为安全第一的智能开发自动化制作**