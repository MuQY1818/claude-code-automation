---
allowed-tools: Bash(git:*), Bash(gh:*)
argument-hint: [branch-name] [--force]
description: Intelligent git push with validation and context awareness
model: claude-sonnet-4-20250514
---

Perform intelligent git push with comprehensive validation and safety checks:

## Push Strategy:
Based on `$ARGUMENTS`:
- If branch specified: Push to specific branch
- If `--force` flag: Allow force push with extra warnings
- Default: Push current branch to origin

## Pre-Push Validation:
1. **Git Status Check**:
   - Verify all changes are committed
   - Check for untracked important files
   - Validate branch state

2. **Branch Analysis**:
   - Identify current branch
   - Check if branch exists on remote
   - Analyze commits ahead/behind remote

3. **Safety Checks**:
   - Prevent accidental force push to main/master
   - Warn about large file additions
   - Check for sensitive data in commits

## Context-Aware Pushing:
Consider project and branch context:

### Main/Master Branch Protection:
- Extra confirmation for direct pushes to main
- Suggest PR workflow for protected branches
- Check branch protection rules

### Feature Branch Workflow:
- Auto-set upstream for new branches
- Suggest branch naming conventions
- Check for conflicts with main branch

### Release Branch Handling:
- Validate version tags and changelog
- Check for breaking changes
- Ensure CI/CD pipeline compatibility

## Push Process:
1. **Validation Phase**:
   - Run pre-push safety checks
   - Validate commit messages follow conventions
   - Check for potential issues

2. **Preparation Phase**:
   - Set upstream if needed
   - Handle authentication if required
   - Prepare push command with appropriate flags

3. **Execution Phase**:
   - Execute push with progress monitoring
   - Handle push failures gracefully
   - Provide clear feedback on results

4. **Post-Push Actions**:
   - Suggest next steps (PR creation, deployment)
   - Update local tracking information
   - Provide relevant URLs and commands

## Safety Features:
- Prevent accidental force push without explicit confirmation
- Backup recommendations for risky operations
- Clear error messages with suggested solutions
- Integration with GitHub CLI for enhanced workflow

Begin by checking the current git status and branch information to plan the appropriate push strategy.