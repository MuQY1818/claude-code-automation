---
allowed-tools: Bash(git:*), Read, Grep, Glob
argument-hint: [--style=conventional] [--type=feat|fix|docs] [--dry-run] [--auto]
description: Generate intelligent commit messages using ultra think analysis  
model: claude-sonnet-4-20250514
---

Generate intelligent, context-aware commit messages through deep analysis of staged changes and project context.

## Ultra Think Analysis Framework

This command employs **ultra think** methodology to analyze code changes and generate high-quality commit messages that follow best practices and project conventions.

## Argument Processing
Analyze `$ARGUMENTS` for commit parameters:
- `--style=conventional|semantic|angular|custom` - Message format style (default: conventional)
- `--type=feat|fix|docs|style|refactor|test|chore` - Override automatic type detection
- `--scope=component` - Manually specify commit scope
- `--dry-run` - Preview message without committing
- `--auto` - Auto-commit without confirmation (use with caution)

## Phase 1: Deep Change Analysis

### **Staged Changes Detection**
Execute comprehensive git analysis:
```bash
!git status --porcelain
!git diff --staged --name-only
!git diff --staged --stat
!git diff --staged --numstat
```

### **Change Classification Intelligence**
Analyze each modified file to determine:

#### **Change Types Detection**:
- **New Features** (`feat`):
  - New functions, classes, modules added
  - New API endpoints or routes
  - New configuration options
  - New user-facing functionality

- **Bug Fixes** (`fix`):
  - Error handling improvements
  - Logic corrections and fixes
  - Performance issue resolutions
  - Security vulnerability patches

- **Documentation** (`docs`):
  - README updates, comments
  - API documentation changes
  - Code documentation improvements
  - Wiki or doc site updates
  - 

- **Refactoring** (`refactor`):
  - Code restructuring without behavior change
  - Function/variable renaming
  - File organization improvements
  - Code simplification

- **Tests** (`test`):
  - New test cases or test files
  - Test updates and improvements
  - Test configuration changes
  - Testing framework modifications

- **Styling** (`style`):
  - Code formatting changes only
  - Whitespace, indentation fixes
  - Linting rule compliance
  - Import statement organization

- **Chores** (`chore`):
  - Build script updates
  - Dependency updates
  - Configuration file changes
  - Tooling modifications

## Phase 2: Context Intelligence Integration

### **Project Context Analysis**
Leverage existing context management system:
- **Project Type**: Web, Python, Java, Rust, Go detection
- **Framework Detection**: React, Django, Spring, etc.
- **File Structure**: Module organization and architecture
- **Naming Conventions**: Existing project patterns

### **Scope Detection Logic**
Intelligently determine commit scope from file paths:

#### **Frontend Projects**:
- `src/components/auth/` → `scope: auth`
- `src/pages/dashboard/` → `scope: dashboard`  
- `src/services/api/` → `scope: api`
- `src/utils/` → `scope: utils`

#### **Backend Projects**:
- `api/auth/` → `scope: auth`
- `models/user.py` → `scope: user`
- `config/database.py` → `scope: config`
- `middleware/` → `scope: middleware`

#### **Full-Stack Projects**:
- `frontend/` changes → `scope: frontend`
- `backend/` changes → `scope: backend`
- Root config files → `scope: config`

### **Breaking Change Detection**
Analyze for potentially breaking changes:
- Public API modifications
- Configuration schema changes
- Database migration files
- Major dependency updates
- Function signature changes

## Phase 3: Historical Pattern Analysis

### **Commit History Analysis**
```bash
!git log --oneline -20 --format="%h %s"
!git log --grep="feat\|fix\|docs" --oneline -10
```

Detect existing team conventions:
- **Message Format**: Conventional commits vs custom format
- **Capitalization**: Sentence case vs lowercase
- **Length Patterns**: Typical subject line length
- **Scope Usage**: Common scopes in project history

### **Branch Context**
```bash
!git branch --show-current
!git status --branch --porcelain
```

Consider branch naming for additional context:
- `feature/auth-system` → likely `feat(auth):`
- `bugfix/login-error` → likely `fix(auth):`
- `docs/api-updates` → likely `docs(api):`

## Phase 4: Message Generation Strategy

### **Conventional Commits Format**
Generate messages following conventional commits specification:

```
type(scope): description

[optional body]

[optional footer]
```

### **Subject Line Generation**
1. **Type Selection**: Most significant change type
2. **Scope Detection**: Primary affected component
3. **Description**: Imperative mood, present tense
4. **Length Limit**: Max 50 characters for subject line

### **Body Generation Logic**
For complex changes, generate body with:
- **What**: Brief explanation of changes
- **Why**: Motivation for the change
- **Context**: Any important background information

### **Footer Generation**
Add footers for:
- **Breaking Changes**: `BREAKING CHANGE: description`
- **Issue References**: `Closes #123`, `Fixes #456`
- **Co-authors**: `Co-authored-by: Name <email>`

## Phase 5: Style Adaptations

### **Conventional Commits Style** (default)
```
feat(auth): add OAuth2 integration
fix(api): resolve user authentication timeout
docs(readme): update installation instructions
```

### **Semantic Style**  
```
feat(auth): add OAuth2 integration
fix(api): resolve user authentication timeout
docs(readme): update installation instructions
```

### **Angular Style**
```
feat(auth): add OAuth2 integration

Add support for OAuth2 authentication flow
with Google and GitHub providers

Closes #123
```

## Phase 6: Validation and Confirmation

### **Message Quality Checks**
- Subject line ≤ 50 characters
- Body lines ≤ 72 characters
- Imperative mood verification
- No trailing periods in subject
- Proper capitalization

### **Pre-commit Validation**
```bash
!git status --porcelain
# Ensure staged changes exist
# Check for merge conflicts
# Validate no untracked critical files
```

### **Interactive Confirmation**
Unless `--auto` flag is used:
1. Display generated commit message
2. Show `git status` context
3. Allow message editing
4. Confirm before executing `git commit`

### **Execution Strategy**
```bash
# For dry-run
echo "Generated commit message:"
echo "[message preview]"

# For actual commit
!git commit -m "generated message"
# Or with body:
!git commit -m "subject" -m "body content"
```

## Ultra Think Decision Tree

Apply **deep thinking** for complex scenarios:

### **Multi-Type Changes**
If changes span multiple types:
1. Identify the **most significant** change type
2. Consider if changes are **logically related**
3. If unrelated, suggest **splitting commits**
4. Prioritize user-facing changes over internal changes

### **Large Changeset Analysis**
For commits affecting >10 files:
1. **Group by logical functionality**
2. **Identify common theme** across changes
3. **Suggest atomic commits** if changes are unrelated
4. **Focus on primary impact** in message

### **Cross-Component Changes**
When changes affect multiple modules:
1. **Identify primary component** affected
2. **Use broader scope** if changes are tightly coupled
3. **Consider architecture-level** scope (e.g., `refactor(core):`)
4. **Document cross-component impact** in body

## Error Handling and Safety

### **Pre-flight Checks**
- Verify git repository exists
- Ensure staged changes are present
- Check for merge conflicts
- Validate branch state

### **Rollback Capability**  
- Support `git reset --soft HEAD~1` if immediate undo needed
- Preserve original working directory state
- Maintain staged changes integrity

Generate intelligent, contextually appropriate commit messages that follow best practices while adapting to project-specific conventions and team patterns.