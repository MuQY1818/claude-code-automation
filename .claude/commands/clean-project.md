---
allowed-tools: Bash(find:*, rm:*, ls:*), Read, Grep, Glob, LS
argument-hint: [--mode=safe|moderate] [--dry-run] [--preserve-git]
description: Safely clean project files while preserving code and git integrity
model: claude-sonnet-4-20250514
---

Perform safe, intelligent project cleanup that improves performance while guaranteeing zero damage to source code, configuration, or git repository.

## Critical Safety Requirements

⚠️  **MANDATORY BRANCH SAFETY** ⚠️  
**This command MUST be run on a new branch, never on main/master**

### **Pre-Execution Branch Check**
```bash
# Get current branch
current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")

# Check if on main/master branch
if [[ "$current_branch" == "main" || "$current_branch" == "master" ]]; then
    echo "🚨 ERROR: Cannot run cleanup on main/master branch!"
    echo "Please create and switch to a new branch first:"
    echo "  git checkout -b cleanup/safe-project-cleanup"
    echo "  Then run the command again."
    exit 1
fi

# Warn if not on a cleanup branch
if [[ ! "$current_branch" =~ ^(cleanup|clean|temp|feature)/ ]]; then
    echo "⚠️  WARNING: Recommended to use a dedicated cleanup branch"
    echo "Current branch: $current_branch" 
    read -p "Continue anyway? (y/N): " -n 1 -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Operation cancelled. Create a cleanup branch:"
        echo "  git checkout -b cleanup/safe-project-cleanup"
        exit 1
    fi
fi
```

### **Branch Creation Helper**
If running on main/master, automatically suggest:
```bash
echo "🔧 Creating safe cleanup branch..."
git checkout -b "cleanup/project-cleanup-$(date +%Y%m%d-%H%M%S)"
echo "✅ Safe to proceed on new branch: $(git branch --show-current)"
```

## Argument Processing

Analyze `$ARGUMENTS` for cleanup parameters:
- `--mode=safe|moderate` - Cleanup intensity level (default: safe)
- `--dry-run` - Preview changes without executing (recommended first run)
- `--preserve-git` - Extra git safety (enabled by default)
- `--skip-cache` - Skip package manager cache cleanup
- `--skip-build` - Skip build artifact cleanup

## Phase 1: Project Safety Analysis

### **Repository Protection Check**
```bash
!git status 2>/dev/null || echo "Not a git repository"
!git branch --show-current 2>/dev/null
!git status --porcelain 2>/dev/null
```

**Critical Safety Checks**:
- Detect if we're on main/master branch (extra caution)
- Check for uncommitted changes (preserve working state)
- Verify git repository health
- Never proceed if git appears corrupted

### **Project Type Detection**
Identify project structure for appropriate cleanup rules:

**Python Projects**:
- Look for: `requirements.txt`, `setup.py`, `pyproject.toml`
- Virtual environments: `venv/`, `env/`, `.venv/`
- Package patterns: `__pycache__/`, `*.pyc`, `*.pyo`

**Node.js Projects**:
- Look for: `package.json`, `yarn.lock`, `package-lock.json`
- Dependencies: `node_modules/`
- Build outputs: `dist/`, `build/`, `.next/`

**Other Project Types**:
- Rust: `Cargo.toml`, `target/`
- Go: `go.mod`, `bin/`
- Java: `pom.xml`, `target/`, `build/`

## Phase 2: Safe Mode Cleanup

### **Build Artifacts (Always Safe to Remove)**
Target files that can be regenerated:

**Python Build Artifacts**:
```bash
# Find and list Python cache files
find . -type d -name "__pycache__" 2>/dev/null
find . -name "*.pyc" -o -name "*.pyo" -o -name "*.pyd" 2>/dev/null
find . -type d -name "*.egg-info" 2>/dev/null
find . -type d -name "build" -path "*/setup.py/*" 2>/dev/null
find . -type d -name "dist" -path "*/setup.py/*" 2>/dev/null
```

**Testing Artifacts**:
```bash
find . -type d -name ".pytest_cache" 2>/dev/null
find . -type d -name ".coverage" 2>/dev/null
find . -name "coverage.xml" -o -name ".coverage.*" 2>/dev/null
```

**Temporary Files**:
```bash
find . -name "*.tmp" -o -name "*.temp" 2>/dev/null
find . -name "*.log" -not -path "./.git/*" 2>/dev/null
find . -name "*~" -o -name "*.bak" 2>/dev/null
```

**OS-Specific Files**:
```bash
find . -name ".DS_Store" -o -name "Thumbs.db" -o -name "desktop.ini" 2>/dev/null
```

### **Safe Removal Process**
For each category of files found:
1. **List files** that would be removed
2. **Calculate space** that would be freed
3. **Confirm category** is safe for removal
4. **Execute removal** only if not in dry-run mode

## Phase 3: Moderate Mode Additions

### **Local Development Artifacts**
When `--mode=moderate` is specified, additionally target:

**IDE and Editor Files**:
```bash
find . -name ".vscode/settings.json.bak" 2>/dev/null
find . -name "*.swp" -o -name "*.swo" 2>/dev/null
find . -name ".idea/workspace.xml.bak" 2>/dev/null
```

**Package Manager Caches** (with caution):
```bash
# Only clear cache subdirectories, never main directories
find . -path "*/node_modules/.cache/*" -type f 2>/dev/null
find . -path "*/.pip-cache/*" -type f 2>/dev/null
```

**Large Log Files** (rotate, don't delete):
```bash
find . -name "*.log" -size +10M -not -path "./.git/*" 2>/dev/null
```

## Phase 4: Project-Specific Intelligence

### **Python Project Optimizations**
For Python projects specifically:

**Virtual Environment Cleanup**:
- Clean `site-packages` cache but preserve installed packages
- Remove `__pycache__` recursively but preserve `.py` files
- Clear `pip` cache but maintain `pip.conf`

**Development Tool Artifacts**:
```bash
# Jupyter notebook checkpoints
find . -type d -name ".ipynb_checkpoints" 2>/dev/null

# Pytest artifacts
find . -type d -name ".pytest_cache" 2>/dev/null

# MyPy cache
find . -type d -name ".mypy_cache" 2>/dev/null
```

### **Web Project Optimizations**
For Node.js/web projects:

**Build System Cleanup**:
```bash
find . -type d -name "dist" -not -path "*/node_modules/*" 2>/dev/null
find . -type d -name "build" -not -path "*/node_modules/*" 2>/dev/null
find . -type d -name ".next" 2>/dev/null
```

**Package Manager Artifacts**:
- Clear npm/yarn cache directories
- Remove temporary install files
- Keep `node_modules` intact (never auto-remove)

## Phase 5: Safety Validation and Execution

### **Pre-Execution Safety Check**
Before any file removal:
```bash
# Verify git repository is still healthy
!git status --porcelain 2>/dev/null
!git fsck --no-progress --quiet 2>/dev/null || echo "Git integrity check failed"

# Ensure we're not accidentally targeting system directories
pwd | grep -E '^(/|C:\\)$' && echo "ERROR: Cannot clean system root"
```

### **Dry Run Mode**
When `--dry-run` is specified:
- **List all files** that would be removed
- **Calculate total space** that would be freed
- **Show removal commands** but don't execute
- **Provide safety summary** of what was preserved

```bash
echo "=== DRY RUN: Files that would be removed ==="
echo "Build artifacts: X files (Y MB)"
echo "Temporary files: X files (Y MB)"
echo "Cache files: X files (Y MB)"
echo "Total space to be freed: Y MB"
echo ""
echo "PRESERVED (never touched):"
echo "- All source code files"
echo "- All configuration files"
echo "- Git repository and history"
echo "- Virtual environments"
echo "- Dependencies (node_modules, site-packages)"
```

### **Safe Removal Execution**
For actual cleanup (not dry-run):
1. **Create removal log** with timestamp
2. **Remove files by category** with progress indication
3. **Verify no source files** were accidentally removed
4. **Report cleanup summary** with space freed
5. **Validate project still works** (quick smoke test)

### **Post-Cleanup Verification**
```bash
# Quick project health check
if [ -f "requirements.txt" ]; then
    echo "Python project structure preserved"
fi

if [ -f "package.json" ]; then
    echo "Node.js project structure preserved"
    npm list --depth=0 > /dev/null 2>&1 && echo "Dependencies intact"
fi

# Git repository health
!git status > /dev/null 2>&1 && echo "Git repository healthy"
```

## Safety Guarantees

### **Never Touch These**
- **Source Code**: `*.py`, `*.js`, `*.ts`, `*.rs`, `*.go`, etc.
- **Configuration**: `*.json`, `*.yaml`, `*.toml`, `*.ini`
- **Environment**: `.env`, `venv/`, `node_modules/`
- **Git**: `.git/` directory and all git metadata
- **Documentation**: `*.md`, `*.rst`, `docs/`
- **Tests**: `test_*.py`, `*.test.js`, `tests/`

### **Whitelist-Only Approach**
Only remove files matching explicit safe patterns:
- Build artifacts: `__pycache__/`, `dist/`, `build/`
- Temporary files: `*.tmp`, `*.log`, `*~`
- Cache directories: `.pytest_cache/`, `.mypy_cache/`
- OS artifacts: `.DS_Store`, `Thumbs.db`

### **Error Recovery**
- **Log all operations** for potential rollback
- **Stop on first error** rather than continue
- **Preserve working directory state**
- **Never modify git history** or branches

Clean projects safely and effectively while maintaining absolute protection for source code, configuration, and git repository integrity.