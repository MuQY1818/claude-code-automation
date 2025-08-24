---
allowed-tools: Read, Edit, MultiEdit, Glob, Grep
argument-hint: [file-pattern] [--template=minimal|detailed|custom]
description: Add intelligent header comments to source files
model: claude-sonnet-4-20250514
---

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