# Claude Code Automation System

[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-v2.0.0-green.svg)](https://github.com/anthropics/claude-code)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/claude--code-automation-purple.svg)](https://claude.ai/code)

**Enhanced Claude Code automation framework with intelligent hooks, custom commands, and bilingual documentation generation.**

This repository provides a sophisticated dual-layer automation system that extends Claude Code's capabilities with context-aware prompt modification, advanced development workflows, and intelligent project analysis.

## Features

### **Native Hook System**
- **UserPromptSubmit Hooks** - Intelligent prompt modification based on context
- **Ultra Think Mode** - Deep analysis prompts for complex problems
- **Concise Responses** - Automatic short answers for simple queries
- **Learning Support** - Enhanced explanations for educational contexts
- **Digest Mode** - Project-aware `-d` flag processing

### **Custom Command System**
- **10 Specialized Commands** - Advanced development workflow automation
- **Security Analysis** (`/security`) - Multi-layer vulnerability scanning
- **PR Creation** (`/create-PR`) - Intelligent pull request generation
- **Code Refactoring** (`/refactor`) - Context-aware code improvement
- **File Review** (`/file-review`) - Comprehensive code analysis
- **Git Commits** (`/git-commit`) - Ultra think-powered commit message generation
- **Bilingual Documentation** (`/create-readme`, `/update-readme`) - English/Chinese README automation

### **Context Intelligence**
- **Project Detection** - Automatic identification of project types (Web, Python, Java, Rust, Go, Docker)
- **Language Analysis** - Smart detection of programming languages and frameworks
- **Git Integration** - Branch tracking, change analysis, and commit intelligence
- **Tool Validation** - Prerequisite checking and environment validation

## Installation

### Prerequisites
- **Python 3.8+**
- **Claude Code CLI** installed and configured
- **Git** for version control features

### Setup
```bash
# Clone the repository
git clone https://github.com/muqy1818/claude-code-automation.git
cd claude-code-automation

# Install Python dependencies (if any)
pip install -r requirements.txt

# Configure Claude Code hooks
cp .claude/settings.json ~/.claude/settings.json
# OR for project-specific configuration
# The .claude/settings.json is already in place
```

## Quick Start

### 1. **Enable Hook System**
The hook system automatically activates when you use Claude Code in this directory:

```bash
# Test the -d digest mode
echo "explain how hooks work -d" | claude

# Test ultra think mode
echo "design a scalable microservices architecture" | claude
```

### 2. **Use Custom Commands**
Access advanced automation with slash commands:

```bash
# Generate security analysis
/security

# Create intelligent README (bilingual)
/create-readme --lang=both --style=standard

# Intelligent PR creation
/create-PR --draft

# Context-aware refactoring
/refactor --type=performance
```

## Usage

### Hook System
The automation system operates through **two layers**:

#### **Layer 1: Native Claude Code Hooks**
- Modifies prompts before they reach Claude
- Configured in `.claude/settings.json`
- Executes in sequence: ultrathink → answer_in_short → explain → default

```bash
# Examples of hook activation
"complex algorithm design problem"     # → Triggers ultra think
"what is Python?"                      # → Triggers concise response
"help me learn recursion"              # → Triggers explanation mode
"optimize this code -d"                # → Triggers digest mode
```

#### **Layer 2: Custom Command System**
- Advanced development workflows
- Context-aware execution
- Powered by `/core` Python framework

### Custom Commands

#### **Documentation Commands**
```bash
# Generate new README
/create-readme --lang=en --style=comprehensive
/create-readme --lang=zh --style=minimal
/create-readme --lang=both --style=standard

# Update existing README
/update-readme --sections=installation,usage
/update-readme --lang=both --preserve=true
```

#### **Development Commands**
```bash
# Security analysis
/security secrets              # Scan for hardcoded secrets
/security dependencies         # Check vulnerable dependencies
/security full                # Complete security audit

# Code improvement
/refactor src/                # Refactor specific directory
/refactor --type=pattern      # Extract patterns and reduce duplication
/file-review --focus=security # Security-focused code review
```

#### **Git Integration**
```bash
/create-PR main               # Create PR against main branch
/create-PR --draft            # Create draft PR
/push-to-github              # Validated git push
/explain-pull-request        # Document architecture changes
```

## Architecture

The system uses a **dual-layer architecture**:

### **Core Components**
- **Context Manager** (`core/context_manager.py`) - Project intelligence and detection
- **Command Registry** (`core/command_registry.py`) - Command execution and validation  
- **Hook Dispatcher** (`core/hook_dispatcher.py`) - Command-level hook management
- **Native Hooks** (`hooks/UserPromptSubmit/`) - Prompt modification scripts

### **Configuration System**
- **Native Hooks**: `.claude/settings.json` (Claude Code format)
- **Custom Commands**: `.claude/settings/commands.json` (command definitions)
- **Global Settings**: `.claude/settings/global.json` (system-wide defaults)
- **Project Settings**: `.claude/settings/project.json` (project-specific overrides)

## Bilingual Support

The system provides comprehensive bilingual documentation generation:

### **Language Options**
- `--lang=en` - English documentation (default)
- `--lang=zh` - Chinese documentation
- `--lang=both` - Generate both language versions

### **Technical Approach**
- **English Primary** - Main documentation language
- **Chinese Localization** - Technical accuracy with cultural adaptation
- **Consistent Structure** - Mirrored sections across languages
- **Technical Terms** - Preserves English technical vocabulary

## Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Run the hook system tests**: Test with various prompt types
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request** using `/create-PR` command

### **Development Setup**
```bash
# Clone and setup
git clone https://github.com/your-org/claude-code-automation.git
cd claude-code-automation

# Test hook system
echo "test prompt -d" | python .claude/hooks/UserPromptSubmit/append_default.py

# Test command registry
python .claude/core/command_registry.py list documentation
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Anthropic** - For Claude Code platform and API
- **Claude Code Community** - For automation patterns and best practices
- **Contributors** - For enhancements and bug fixes

---

**Made with care for intelligent development automation**