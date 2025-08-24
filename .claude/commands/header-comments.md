---
allowed-tools: Read, Edit, MultiEdit, Glob, Grep
argument-hint: [file-pattern] [--template=minimal|detailed|custom]
description: Add intelligent header comments to source files
model: claude-sonnet-4-20250514
---

⚠️  **CRITICAL SAFETY WARNING** ⚠️  
**This command modifies source files and MUST be run on a new branch, never on main/master**

## Critical Safety Requirements

### **Pre-Execution Branch Check**
```bash
# Get current branch
current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")

# Check if on main/master branch
if [[ "$current_branch" == "main" || "$current_branch" == "master" ]]; then
    echo "🚨 ERROR: Cannot run header-comments on main/master branch!"
    echo "This command modifies source files and could affect your codebase."
    echo "Please create and switch to a new branch first:"
    echo "  git checkout -b feature/add-header-comments-$(date +%Y%m%d-%H%M%S)"
    echo "  Then run the command again."
    exit 1
fi

# Verify working directory is clean
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  WARNING: You have uncommitted changes."
    echo "Adding headers will modify source files. Recommend committing changes first."
    git status --porcelain
    read -p "Continue anyway? (y/N): " -n 1 -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Operation cancelled. Commit your changes first:"
        echo "  git add -A && git commit -m 'Save work before adding headers'"
        exit 1
    fi
fi
```

## Header Comment Process

Add comprehensive header comments to source files with context-aware templates:

## Header Comment Scope:
Based on `$ARGUMENTS`:
- File patterns to target (e.g., "*.py", "src/**/*.js")
- Template style: `minimal`, `detailed`, or `custom`
- Default: Add appropriate headers to all source files

## Template Types:

### Minimal Template:
- File purpose and brief description
- Author and creation date
- License information (if applicable)

### Detailed Template:
- Comprehensive file description
- Usage examples and API overview
- Dependencies and requirements
- Author, creation date, and modification history
- License and copyright information

### Custom Template:
- Project-specific header format
- Company/organization branding
- Specific metadata requirements

## Context-Aware Headers:
Generate appropriate headers based on file type and project context:

### Python Files:
```python
"""
Module/script description.
Author: [Author Name]
Created: [Date]
License: [License Type]
"""
```

### JavaScript/TypeScript:
```javascript
/**
 * File description and purpose
 * @author [Author Name]
 * @created [Date]
 * @license [License Type]
 */
```

### CSS/SCSS:
```css
/*
 * Stylesheet description
 * Author: [Author Name]
 * Created: [Date]
 */
```

## Smart Content Generation:
1. **File Analysis**:
   - Determine file type and purpose
   - Analyze existing code to understand functionality
   - Identify key classes, functions, or components

2. **Context Gathering**:
   - Extract project information from package.json, setup.py, etc.
   - Determine license from repository
   - Get author information from git config

3. **Description Generation**:
   - Create meaningful descriptions based on code analysis
   - Include usage examples for key modules
   - Document important dependencies

## Header Management:
- Check for existing headers and update appropriately
- Preserve important existing information
- Maintain consistent formatting across files
- Handle different comment styles per language

## Project Integration:
- Respect existing code style and conventions
- Integration with linting tools and pre-commit hooks
- Batch processing with progress tracking
- Git integration for tracking changes

Start by analyzing the target files and gathering project context for intelligent header generation.