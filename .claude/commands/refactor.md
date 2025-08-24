---
allowed-tools: Read, Edit, MultiEdit, Bash(*), Grep, Glob
argument-hint: [target] [--type=pattern|structure|performance]
description: Intelligent code refactoring with context awareness
model: claude-sonnet-4-20250514
---

⚠️  **CRITICAL SAFETY WARNING** ⚠️  
**This command modifies source code and MUST be run on a new branch, never on main/master**

## Critical Safety Requirements

### **Pre-Execution Branch Check**
```bash
# Get current branch
current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")

# Check if on main/master branch
if [[ "$current_branch" == "main" || "$current_branch" == "master" ]]; then
    echo "🚨 ERROR: Cannot run refactor on main/master branch!"
    echo "This command modifies source code and could break your project."
    echo "Please create and switch to a new branch first:"
    echo "  git checkout -b refactor/code-improvements-$(date +%Y%m%d-%H%M%S)"
    echo "  Then run the command again."
    exit 1
fi

# Warn if not on a feature/refactor branch
if [[ ! "$current_branch" =~ ^(refactor|feature|fix)/ ]]; then
    echo "⚠️  WARNING: Recommended to use a dedicated refactor branch"
    echo "Current branch: $current_branch" 
    echo "This command will modify source code files."
    read -p "Continue anyway? (y/N): " -n 1 -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Operation cancelled. Create a refactor branch:"
        echo "  git checkout -b refactor/code-improvements-$(date +%Y%m%d-%H%M%S)"
        exit 1
    fi
fi

# Verify working directory is clean
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  WARNING: You have uncommitted changes."
    echo "Refactoring will modify files. Recommend committing current changes first."
    git status --porcelain
    read -p "Continue anyway? (y/N): " -n 1 -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Operation cancelled. Commit your changes first:"
        echo "  git add -A && git commit -m 'Save work before refactoring'"
        exit 1
    fi
fi
```

## Refactoring Process

Perform intelligent refactoring based on project context and specified target:

## Refactoring Analysis:
1. **Target Identification**: 
   - If `$ARGUMENTS` specifies a file/directory, focus refactoring there
   - If no target specified, analyze entire codebase for refactoring opportunities

2. **Refactoring Type** (from --type argument):
   - `pattern` - Extract patterns, reduce duplication, improve abstractions
   - `structure` - Improve file organization, module structure
   - `performance` - Optimize algorithms, reduce complexity
   - `quality` - Improve readability, maintainability, documentation

## Context-Aware Refactoring:
Consider project type and apply appropriate refactoring strategies:

### For Python Projects:
- Extract functions and classes to reduce complexity
- Apply PEP 8 formatting and naming conventions
- Use dataclasses, type hints, and modern Python features
- Optimize imports and module structure

### For JavaScript/TypeScript:
- Extract reusable components and utilities
- Apply modern ES6+ patterns (arrow functions, destructuring)
- Improve async/await usage
- Optimize bundle size and performance

### For Web Applications:
- Component extraction and reusability
- CSS/styling optimization
- Performance optimizations (lazy loading, caching)
- Accessibility improvements

## Refactoring Process:
1. **Analysis Phase**:
   - Identify code smells and anti-patterns
   - Measure current complexity metrics
   - Find duplication and coupling issues

2. **Planning Phase**:
   - Prioritize refactoring opportunities
   - Plan incremental changes to minimize risk
   - Identify test requirements

3. **Execution Phase**:
   - Make systematic, small changes
   - Maintain functionality while improving structure
   - Update tests and documentation

4. **Validation Phase**:
   - Run tests to ensure no regression
   - Measure improvement in complexity metrics
   - Verify performance hasn't degraded

## Safety Measures:
- Always create backup or ensure git tracking
- Run existing tests after each refactoring step
- Make incremental changes with clear commit messages
- Validate refactoring doesn't break functionality

Begin by analyzing the current codebase structure and identifying the most impactful refactoring opportunities.