#!/usr/bin/env python3
"""
Enhanced Answer In Short Hook
Appends concise response instruction based on context and prompt analysis.
"""

import json
import sys
import re
from typing import Dict, Any


def analyze_prompt_complexity(prompt: str) -> str:
    """Analyze prompt complexity to determine appropriate response style."""
    # Count question complexity indicators
    question_words = len(re.findall(r'\b(what|how|why|when|where|which|who)\b', prompt.lower()))
    sentences = len(re.findall(r'[.!?]+', prompt))
    words = len(prompt.split())
    
    # Simple question patterns
    simple_patterns = [
        r'^\s*what\s+is\s+\w+\s*\??$',  # "what is X?"
        r'^\s*how\s+to\s+\w+.*\??$',    # "how to X?"
        r'^\s*\w+\s*\+\s*\w+\s*$',      # "2 + 2"
    ]
    
    if any(re.match(pattern, prompt.lower()) for pattern in simple_patterns):
        return "ultra_short"
    elif question_words <= 1 and sentences <= 2 and words <= 20:
        return "short"
    elif question_words <= 3 and sentences <= 5 and words <= 50:
        return "moderate"
    else:
        return "detailed"


def should_apply_short_response(context: Dict[str, Any]) -> bool:
    """Determine if short response instruction should be applied."""
    prompt = context.get("prompt", "")
    
    # Don't apply to complex development tasks
    complex_indicators = [
        "implement", "create", "build", "develop", "design",
        "refactor", "optimize", "debug", "fix", "add feature"
    ]
    
    if any(indicator in prompt.lower() for indicator in complex_indicators):
        return False
    
    # Don't apply if user explicitly asks for detailed explanation
    detail_requests = [
        "explain in detail", "detailed explanation", "comprehensive",
        "step by step", "elaborate", "thorough"
    ]
    
    if any(request in prompt.lower() for request in detail_requests):
        return False
    
    return True


def main(context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Enhanced answer in short hook with context awareness."""
    # For Claude Code native hooks, read prompt from stdin
    if not context:
        try:
            prompt_input = sys.stdin.read().strip()
            prompt = prompt_input
        except:
            sys.exit(1)  # Skip if no input
    else:
        prompt = context.get("prompt", "")
    
    # Skip if not applicable
    if not should_apply_short_response({"prompt": prompt}):
        print(prompt)  # Output unchanged prompt
        sys.exit(0)
    
    # Analyze prompt complexity
    complexity = analyze_prompt_complexity(prompt)
    
    # Determine appropriate instruction
    instructions = {
        "ultra_short": "Answer in 1-3 words maximum.",
        "short": "Answer concisely in 1-2 sentences.",
        "moderate": "Keep response brief and focused.",
        "detailed": "Provide a focused but complete answer."
    }
    
    instruction = instructions.get(complexity, instructions["moderate"])
    
    # Add project context awareness (simplified for native hooks)
    project_type = "python"
    if project_type in ["web", "python", "java"]:
        instruction += f" Focus on {project_type}-specific solutions."
    
    # Output modified prompt with instruction
    modified_prompt = f"{prompt}\n\n{instruction}"
    print(modified_prompt)
    
    return {
        "action": "append",
        "instruction": instruction,
        "complexity": complexity,
        "project_context": project_type
    }


if __name__ == "__main__":
    try:
        result = main()
        sys.exit(0)  # Success
    except Exception:
        sys.exit(1)  # Error