---
allowed-tools: Bash(*), Grep, Glob, Read
argument-hint: [scan-type]
description: Comprehensive security analysis and vulnerability detection
model: claude-sonnet-4-20250514
---

Perform a comprehensive security analysis of the codebase with the following focus areas:

## Security Scan Types:
Analyze `$ARGUMENTS` to determine scan type (default: full):
- `secrets` - Scan for hardcoded secrets, keys, passwords
- `dependencies` - Check for vulnerable dependencies
- `code` - Static code analysis for security issues
- `config` - Review configuration files for security misconfigurations
- `full` - Complete security audit

## Analysis Framework:
1. **Secret Detection**:
   - Scan for API keys, passwords, tokens in code
   - Check environment files and configs
   - Identify potential credential leaks in git history

2. **Dependency Vulnerabilities**:
   - Analyze package.json, requirements.txt, etc.
   - Check for known vulnerable packages
   - Suggest updates and alternatives

3. **Code Security Issues**:
   - SQL injection vulnerabilities
   - XSS vulnerabilities
   - Path traversal issues
   - Insecure cryptographic practices
   - Authentication/authorization flaws

4. **Configuration Security**:
   - Insecure default settings
   - Exposed debug modes
   - Weak security headers
   - Improper file permissions

## Project-Specific Checks:
Consider project type and frameworks for targeted analysis:
- **Web apps**: OWASP Top 10, CSP headers, HTTPS enforcement
- **APIs**: Authentication, input validation, rate limiting
- **Python**: Bandit security linting, dependency checks
- **JavaScript/Node**: npm audit, ESLint security rules

## Deliverables:
1. Security risk assessment with severity ratings
2. Actionable remediation recommendations
3. Best practices for ongoing security
4. Tools and processes for continuous security monitoring

Start by identifying the project structure and then perform the appropriate security analysis based on the detected technologies and frameworks.