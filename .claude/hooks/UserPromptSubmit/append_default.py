#!/usr/bin/env python3
"""
Enhanced Append Default Hook
Adds intelligent digest instruction when prompt ends with -d flag.
Context-aware and project-specific.
"""

import json
import sys
from typing import Dict, Any


def get_project_specific_digest(project_type: str, languages: list) -> str:
    """Get project-specific digest instructions."""
    base_instruction = "think harder. answer in short. keep it simple."
    
    project_specific = {
        "web": "Focus on web development best practices and modern frameworks.",
        "python": "Emphasize Pythonic solutions and popular libraries.",
        "java": "Consider Java conventions and enterprise patterns.",
        "rust": "Prioritize memory safety and performance.",
        "go": "Focus on simplicity and concurrent patterns.",
        "docker": "Consider containerization best practices.",
    }
    
    language_specific = {
        "javascript": "Use modern ES6+ syntax and patterns.",
        "typescript": "Leverage type safety and interfaces.",
        "python": "Follow PEP 8 and use appropriate data structures.",
        "java": "Apply SOLID principles and design patterns.",
        "rust": "Use ownership principles and error handling.",
        "go": "Keep it simple and use goroutines appropriately.",
    }
    
    # Add project-specific context
    if project_type in project_specific:
        base_instruction += f" {project_specific[project_type]}"
    
    # Add language-specific context
    for lang in languages[:2]:  # Limit to top 2 languages
        if lang in language_specific:
            base_instruction += f" {language_specific[lang]}"
    
    return base_instruction


def should_add_git_context(git_state: Dict[str, Any]) -> str:
    """Add git-specific context if relevant."""
    if not git_state.get("is_git_repo"):
        return ""
    
    context_parts = []
    
    if git_state.get("has_uncommitted_changes"):
        context_parts.append("Consider current uncommitted changes.")
    
    if not git_state.get("is_main_branch"):
        context_parts.append("Working on feature branch.")
    
    return " ".join(context_parts)


def main(context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Enhanced default append hook with project awareness."""
    # For Claude Code native hooks, read prompt from stdin
    if not context:
        try:
            prompt_input = sys.stdin.read().strip()
            # Claude Code passes the raw prompt text
            prompt = prompt_input
        except:
            sys.exit(1)  # Skip if no input
    else:
        prompt = context.get("prompt", "")
    
    # Check if prompt ends with -d flag
    if not prompt.rstrip().endswith("-d"):
        # No -d flag, output original prompt unchanged
        print(prompt)
        sys.exit(0)
    
    # Remove the -d flag from the prompt
    modified_prompt = prompt.rstrip()[:-2].rstrip()
    
    # Get project context (simplified for native hooks)
    project_type = "python"  # Default for this automation project
    languages = ["python"]
    git_state = {}
    frameworks = []
    
    # Build intelligent digest instruction
    digest_instruction = get_project_specific_digest(project_type, languages)
    
    # Output the modified prompt with digest instruction appended
    full_prompt = f"{modified_prompt}\n\n{digest_instruction}"
    print(full_prompt)
    
    return {
        "action": "append",
        "instruction": digest_instruction,
        "project_context": {
            "type": project_type,
            "languages": languages,
            "frameworks": frameworks,
            "git_aware": False
        }
    }


if __name__ == "__main__":
    try:
        result = main()
        sys.exit(0)  # Success
    except Exception:
        sys.exit(1)  # Error