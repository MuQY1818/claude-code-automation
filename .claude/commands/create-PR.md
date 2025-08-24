---
allowed-tools: Bash(git:*), Bash(gh:*)
argument-hint: [base-branch] [--draft]
description: Create intelligent pull request with context awareness
model: claude-sonnet-4-20250514
---

Create a comprehensive pull request with the following intelligent analysis:

## Analysis Required:
1. **Change Analysis**: Examine git diff and categorize changes (features, fixes, docs, tests)
2. **Commit Context**: Analyze commit messages and patterns
3. **Project Context**: Consider project type, languages, and frameworks
4. **Smart Title**: Generate appropriate PR title based on changes
5. **Comprehensive Description**: Include summary, changes, test plan, and context

## Process:
1. Check git status for uncommitted changes
2. Analyze commits ahead of base branch (default: main)
3. Categorize changed files and their purposes
4. Generate context-aware PR title and description
5. Create PR with appropriate labels and reviewers

## Arguments:
- `$ARGUMENTS` can include base branch name and `--draft` flag
- Default base branch: `main`
- Use `--draft` to create draft PR

## Validation:
- Ensure we're in a git repository
- Check for uncommitted changes
- Verify commits exist ahead of base branch
- Confirm GitHub CLI is available

!git status --porcelain
!git log main..HEAD --oneline
!gh pr create --title "$(generated_title)" --body "$(generated_description)" $ARGUMENTS