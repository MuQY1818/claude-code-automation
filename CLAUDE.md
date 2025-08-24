# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## System Architecture

This repository contains a **dual-layer automation framework** with complementary systems:

### **Layer 1: Native Claude Code Hooks**
- **Purpose**: Prompt modification and response behavior
- **Configuration**: `.claude/settings.json` (Claude Code native format)
- **Scope**: UserPromptSubmit events only

### **Layer 2: Custom Command System** 
- **Purpose**: Advanced development workflows and context-aware automation
- **Configuration**: `.claude/settings/` folder with custom Python framework
- **Scope**: Slash commands, project intelligence, command-level hooks

### Core Components

- **Native Hook Scripts** (`hooks/UserPromptSubmit/`): Prompt modification for response behavior
- **Command System Core** (`core/`): Advanced automation framework
  - **Context Manager** (`core/context_manager.py`): Intelligent project detection
  - **Command Registry** (`core/command_registry.py`): Slash command execution engine  
  - **Hook Dispatcher** (`core/hook_dispatcher.py`): Command-level hook system
- **Configuration System**: Multi-layered settings with global defaults and project-specific overrides

## Hook System

The automation operates through Claude Code's native hook system that modifies prompts before they reach Claude:

### Hook Configuration
Hooks are configured in `.claude/settings.json` using Claude Code's native format:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python \".claude/hooks/UserPromptSubmit/script.py\""
          }
        ]
      }
    ]
  }
}
```

### Active UserPromptSubmit Hooks (Execution Order)
1. **append_ultrathink** - Adds deep thinking prompts for complex architectural problems
2. **answer_in_short** - Enforces concise responses for simple queries  
3. **append_explain** - Adds explanation requests for learning scenarios
4. **append_default** - Activates with `-d` flag for project-aware digest mode

### Hook Execution Model
- Hooks execute **sequentially** in the order defined in settings.json
- Each hook receives the **original or previously modified prompt** from stdin
- Hooks output **modified prompts** to stdout
- **Exit code 0** indicates success, non-zero indicates error/skip
- The `-d` flag is **stripped from prompts** and triggers digest mode instructions

## Custom Command System

The advanced automation layer provides 10 specialized commands that operate independently of the native hook system:

### Core Development Commands
- `/security` - Multi-layered security analysis (secrets, dependencies, static analysis, config)
- `/create-PR` - Intelligent PR creation with context-aware titles and descriptions
- `/refactor` - Context-aware code refactoring (pattern, structure, performance, quality)
- `/file-review` - Comprehensive code analysis with focus areas
- `/push-to-github` - Validated git push with branch management
- `/header-comments` - Intelligent file header generation
- `/explain-pull-request` - Architectural documentation and analysis
- `/create-readme` - **NEW** Generate intelligent bilingual README with deep project analysis
- `/update-readme` - **NEW** Intelligently update existing README while preserving custom content
- `/git-commit` - **NEW** Generate intelligent commit messages using ultra think analysis

### Command System Architecture
- **Context-Aware Execution** - Commands adapt behavior based on detected project type, languages, frameworks
- **Parameter validation** with type checking and choices
- **Prerequisite checking** (git repo, required tools)
- **Pre/post command hooks** for extended automation workflows
- **Intelligent error handling** with detailed validation messages

### Command-Level Hook System
Unlike native prompt hooks, the command system supports:
- **PreCommand hooks** - Execute before command runs (validation, setup)
- **PostCommand hooks** - Execute after command completes (cleanup, notifications)
- **OnFileChange hooks** - Trigger on file system changes
- **OnGitAction hooks** - Respond to git operations

This provides enterprise-grade automation capabilities beyond simple prompt modification.

## Context Detection System

The system automatically detects and adapts to different project environments:

### Project Type Detection
- **Web**: `package.json`, `webpack.config.js`, `yarn.lock`
- **Python**: `requirements.txt`, `setup.py`, `pyproject.toml`
- **Java**: `pom.xml`, `build.gradle`
- **Rust**: `Cargo.toml`
- **Go**: `go.mod`, `go.sum`
- **Docker**: `Dockerfile`, `docker-compose.yml`

### Dynamic Context Injection
- **Language detection** via file extensions and patterns
- **Framework identification** from dependency analysis
- **Git state tracking** (branch, uncommitted changes, main branch detection)
- **Tool availability** checking (git, docker, npm, pip, etc.)

## Development Workflows

### Security Analysis (`/security`)
Performs comprehensive security audits:
- **Secret detection** - API keys, tokens, credentials
- **Dependency scanning** - Known vulnerabilities in packages
- **Static analysis** - Code-level security issues (SQL injection, XSS)
- **Configuration review** - Security misconfigurations

### Pull Request Creation (`/create-PR`)
Intelligent PR workflow:
- **Change categorization** (features, fixes, docs, tests)
- **Commit message analysis** for context
- **Auto-generated titles and descriptions** based on diff analysis
- **Support for draft PRs and custom base branches**

### Refactoring (`/refactor`)
Context-aware code improvement:
- **Pattern extraction** - Reduce duplication, improve abstractions
- **Structure optimization** - File organization, module design
- **Performance enhancement** - Algorithm optimization, complexity reduction
- **Quality improvement** - Readability, maintainability, documentation

### Bilingual README Generation (`/create-readme`, `/update-readme`)
**NEW** Intelligent documentation automation with bilingual support:

#### **Create README** (`/create-readme`)
- **Deep Project Analysis** - Automatic detection of project type, languages, frameworks
- **Bilingual Support** - Generate English (primary) and Chinese versions
- **Style Levels** - Minimal, standard, or comprehensive documentation
- **Smart Content** - Context-aware sections based on detected technologies
- **Technical Intelligence** - Automatic badge generation, installation instructions, usage examples

#### **Update README** (`/update-readme`) 
- **Content Preservation** - Maintains author's voice and custom content
- **Selective Enhancement** - Updates outdated information while preserving unique elements
- **Bilingual Synchronization** - Keeps English and Chinese versions consistent
- **Smart Gap Analysis** - Identifies missing sections and outdated information
- **Incremental Updates** - Section-specific updates with rollback capability

#### **Language Support**
- `--lang=en` (default) - English documentation
- `--lang=zh` - Chinese documentation  
- `--lang=both` - Generate both language versions
- **Technical Accuracy** - Proper localization while preserving technical terms
- **Cultural Adaptation** - Appropriate examples and references for target audience

### Intelligent Git Commit (`/git-commit`)
**NEW** Ultra think-powered commit message generation:

#### **Deep Change Analysis**
- **Multi-Type Detection** - Automatic classification (feat, fix, docs, refactor, test, chore)
- **Scope Intelligence** - File-path-based scope detection for modular projects
- **Breaking Change Detection** - Identifies API modifications and major changes
- **Historical Pattern Analysis** - Learns from existing commit conventions

#### **Context-Aware Generation**
- **Conventional Commits** - Standard `type(scope): description` format
- **Project Adaptation** - Respects existing team conventions and patterns
- **Branch Context** - Incorporates branch naming patterns for additional intelligence
- **Multi-Component Changes** - Handles complex changesets across multiple modules

#### **Style Support**
- `--style=conventional` (default) - Standard conventional commits
- `--style=semantic` - Emoji-enhanced commit messages
- `--style=angular` - Angular project conventions
- `--dry-run` - Preview without committing
- `--auto` - Skip confirmation for automated workflows

## Configuration Management

### Settings Hierarchy
1. **Global settings** (`.claude/settings/global.json`) - System-wide defaults
2. **Project settings** (`.claude/settings/project.json`) - Project-specific overrides
3. **Hook configuration** (`.claude/settings/hooks.json`) - Hook priorities and conditions
4. **Command definitions** (`.claude/settings/commands.json`) - Command parameters and validation

### Key Configuration Areas
- **Security constraints** - Allowed tool patterns and safe execution modes
- **Performance tuning** - Parallel execution, caching, lazy loading
- **Integration settings** - Git, GitHub, package managers
- **User preferences** - Verbosity, auto-confirmation, learning modes

## Hook Development Guidelines

### Creating New Hooks for Claude Code
1. **Read from stdin** - Accept the prompt text as input from standard input
2. **Write to stdout** - Output the modified prompt to standard output
3. **Use exit codes** - Exit with 0 for success, non-zero for error/skip
4. **Handle edge cases** - Always output something to stdout (original prompt if no modification)
5. **Apply conditional logic** - Skip modification when not applicable

### Hook Script Structure
```python
#!/usr/bin/env python3
import sys

def main():
    try:
        # Read prompt from stdin
        prompt = sys.stdin.read().strip()
        
        # Apply your logic here
        if should_modify_prompt(prompt):
            modified_prompt = modify_prompt(prompt)
            print(modified_prompt)
        else:
            print(prompt)  # Output unchanged
            
        sys.exit(0)  # Success
    except Exception:
        sys.exit(1)  # Error

if __name__ == "__main__":
    main()
```

### Adding Hooks to Configuration
1. Add your script to `.claude/hooks/UserPromptSubmit/your_hook.py`
2. Update `.claude/settings.json` to include your hook:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python \".claude/hooks/UserPromptSubmit/your_hook.py\""
          }
        ]
      }
    ]
  }
}
```

## System Integration

### Git Integration
- **Automatic branch detection** and main branch identification
- **Uncommitted change tracking** for workflow decisions
- **Commit message analysis** for PR and documentation generation

### GitHub Integration
- **GitHub CLI integration** for PR creation and management
- **Issue linking** and automatic label assignment
- **Repository context** in command execution

### Package Manager Support
- **Multi-language support** - npm, pip, cargo, go mod
- **Dependency analysis** for security scanning
- **Tool availability detection** for prerequisite checking