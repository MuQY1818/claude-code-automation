#!/usr/bin/env python3
"""
Enhanced Append Explain Hook
Adds intelligent explanation requests based on prompt analysis and context.
"""

import json
import sys
import re
from typing import Dict, Any, List


def detect_explanation_triggers(prompt: str) -> List[str]:
    """Detect what type of explanations might be needed."""
    triggers = []
    
    # Code-related explanation triggers
    if re.search(r'\b(function|class|method|algorithm|implementation)\b', prompt.lower()):
        triggers.append("code_structure")
    
    # Concept explanation triggers
    if re.search(r'\b(how|why|what|explain|understand|concept)\b', prompt.lower()):
        triggers.append("concept")
    
    # Process explanation triggers
    if re.search(r'\b(steps|process|workflow|procedure)\b', prompt.lower()):
        triggers.append("process")
    
    # Error/debugging explanation triggers
    if re.search(r'\b(error|bug|debug|fix|issue|problem)\b', prompt.lower()):
        triggers.append("troubleshooting")
    
    return triggers


def get_context_aware_explanation(context: Dict[str, Any], triggers: List[str]) -> str:
    """Generate context-aware explanation requests."""
    project_type = context.get("project_type", "generic")
    languages = context.get("languages", [])
    frameworks = context.get("frameworks", [])
    
    explanations = []
    
    # Base explanation request
    if "concept" in triggers:
        explanations.append("Explain the underlying concepts")
    
    if "code_structure" in triggers:
        if languages:
            lang_list = ", ".join(languages[:2])
            explanations.append(f"Explain the code structure using {lang_list} best practices")
        else:
            explanations.append("Explain the code structure and design patterns")
    
    if "process" in triggers:
        explanations.append("Break down the process step-by-step")
    
    if "troubleshooting" in triggers:
        explanations.append("Explain common pitfalls and debugging approaches")
    
    # Add project-specific context
    if project_type == "web" and frameworks:
        explanations.append(f"Consider {frameworks[0]} specific patterns")
    elif project_type == "python":
        explanations.append("Include Pythonic approaches and standard library usage")
    elif project_type == "java":
        explanations.append("Consider enterprise patterns and Spring framework conventions")
    
    # Add learning context
    if not explanations:
        explanations.append("Provide clear explanations for better understanding")
    
    return ". ".join(explanations) + "."


def should_add_explanation_request(prompt: str, context: Dict[str, Any]) -> bool:
    """Determine if explanation request should be added."""
    # Skip if user explicitly asks for brief answers
    brief_indicators = [
        "briefly", "quick", "short", "simple", "just tell me",
        "one word", "yes/no", "true/false"
    ]
    
    if any(indicator in prompt.lower() for indicator in brief_indicators):
        return False
    
    # Skip if prompt already contains explanation requests
    existing_explanations = [
        "explain", "describe", "elaborate", "detail",
        "break down", "walk through", "show me how"
    ]
    
    if any(exp in prompt.lower() for exp in existing_explanations):
        return False
    
    # Add explanation for learning scenarios
    learning_indicators = [
        "learn", "understand", "new to", "beginner",
        "first time", "how does", "what is"
    ]
    
    return any(indicator in prompt.lower() for indicator in learning_indicators)


def main(context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Enhanced explanation append hook."""
    # For Claude Code native hooks, read prompt from stdin
    if not context:
        try:
            prompt_input = sys.stdin.read().strip()
            prompt = prompt_input
        except:
            sys.exit(1)  # Skip if no input
    else:
        prompt = context.get("prompt", "")
    
    # Check if we should add explanation
    simplified_context = {"prompt": prompt, "project_type": "python", "languages": ["python"], "frameworks": []}
    if not should_add_explanation_request(prompt, simplified_context):
        print(prompt)  # Output unchanged prompt
        sys.exit(0)
    
    # Detect what types of explanations are needed
    triggers = detect_explanation_triggers(prompt)
    
    # Generate context-aware explanation request
    explanation_request = get_context_aware_explanation(simplified_context, triggers)
    
    # Format the explanation request
    full_request = f"\n\nPlease also: {explanation_request}"
    
    # Output modified prompt with explanation request
    modified_prompt = f"{prompt}{full_request}"
    print(modified_prompt)
    
    return {
        "action": "append",
        "explanation_request": explanation_request,
        "triggers": triggers,
        "context_used": {
            "project_type": "python",
            "languages": ["python"],
            "frameworks": []
        }
    }


if __name__ == "__main__":
    try:
        result = main()
        sys.exit(0)  # Success
    except Exception:
        sys.exit(1)  # Error