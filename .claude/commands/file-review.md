---
allowed-tools: Read, Grep, Glob, Bash(*)
argument-hint: [file-pattern] [--focus=security|performance|quality]
description: Comprehensive file and code review with intelligent analysis
model: claude-sonnet-4-20250514
---

Perform comprehensive code review based on specified focus and file patterns:

## Review Scope:
- `$ARGUMENTS` can specify file patterns (e.g., "*.py", "src/**", specific file)
- `--focus` parameter determines review emphasis:
  - `security` - Security vulnerabilities and best practices
  - `performance` - Performance issues and optimization opportunities
  - `quality` - Code quality, maintainability, and best practices
  - `all` (default) - Comprehensive review across all areas

## Review Framework:

### 1. Security Review:
- Input validation and sanitization
- Authentication and authorization checks
- Cryptographic practices
- Dependency vulnerabilities
- Information disclosure risks

### 2. Performance Review:
- Algorithm complexity analysis
- Memory usage patterns
- Database query optimization
- Caching strategies
- Async/concurrency patterns

### 3. Quality Review:
- Code readability and maintainability
- Design patterns and architecture
- Error handling and logging
- Test coverage and quality
- Documentation completeness

## Context-Aware Analysis:
Consider project type for specialized review:

### Web Applications:
- XSS/CSRF protection
- API design and versioning
- Frontend performance optimization
- SEO and accessibility

### Backend Services:
- Scalability considerations
- Database design patterns
- Monitoring and observability
- Error handling strategies

### Libraries/Packages:
- API design consistency
- Backward compatibility
- Documentation quality
- Example usage patterns

## Review Process:
1. **File Discovery**: Identify files matching patterns
2. **Context Analysis**: Understand file purpose and dependencies
3. **Code Analysis**: Apply appropriate review criteria
4. **Issue Prioritization**: Rank findings by severity and impact
5. **Recommendations**: Provide actionable improvement suggestions

## Deliverables:
- Detailed findings with severity levels
- Code examples showing issues and fixes
- Best practice recommendations
- Refactoring suggestions
- Testing recommendations

Begin by analyzing the specified files and applying the appropriate review focus.