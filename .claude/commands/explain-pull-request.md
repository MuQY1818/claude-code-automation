---
allowed-tools: Read, Write, Bash(*), Glob, Grep
argument-hint: [component] [--detailed]
description: Analyze and document code architecture and patterns
model: claude-sonnet-4-20250514
---

Generate comprehensive documentation for code architecture and design patterns:

## Documentation Scope:
Based on `$ARGUMENTS`:
- If component specified: Focus on specific module/component
- If `--detailed` flag: Include implementation details and examples
- Default: High-level architecture overview

## Architecture Analysis:
1. **System Overview**:
   - Project structure and organization
   - Key components and their responsibilities
   - Data flow and interactions
   - External dependencies and integrations

2. **Design Patterns**:
   - Identify used patterns (MVC, Observer, Factory, etc.)
   - Document pattern implementation
   - Explain rationale for pattern choices

3. **Technology Stack**:
   - Languages, frameworks, and libraries
   - Infrastructure and deployment considerations
   - Database schema and data models

## Documentation Generation:
Create the following documentation artifacts:

### 1. README.md (if missing/outdated)
- Project overview and purpose
- Installation and setup instructions
- Usage examples and API documentation
- Contributing guidelines

### 2. ARCHITECTURE.md
- High-level system architecture
- Component interaction diagrams
- Design decisions and trade-offs
- Future architectural considerations

### 3. Component Documentation
- Individual module/component documentation
- API documentation with examples
- Configuration and customization options

### 4. Code Comments and Docstrings
- Function/method documentation
- Complex algorithm explanations
- TODO items and technical debt notes

## Context-Specific Documentation:

### For Web Applications:
- Frontend/backend separation
- API endpoint documentation
- State management patterns
- Component hierarchy

### For Libraries/Packages:
- Public API documentation
- Usage examples and tutorials
- Integration patterns
- Version compatibility

### For CLI Tools:
- Command documentation
- Configuration file examples
- Plugin/extension architecture

## Quality Standards:
- Clear, concise language
- Practical examples and use cases
- Up-to-date with current codebase
- Searchable and well-organized
- Include diagrams where helpful

Start by analyzing the current project structure and identifying documentation gaps.