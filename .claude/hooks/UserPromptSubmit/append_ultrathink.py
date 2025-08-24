#!/usr/bin/env python3
"""
Enhanced Ultra Think Hook
Adds deep thinking prompts for complex problems with context awareness.
"""

import json
import sys
import re
from typing import Dict, Any, List


def analyze_problem_complexity(prompt: str) -> Dict[str, Any]:
    """Analyze the complexity and nature of the problem."""
    complexity_indicators = {
        "architectural": [
            "architecture", "design pattern", "system design",
            "scalability", "microservices", "distributed"
        ],
        "algorithmic": [
            "algorithm", "optimization", "performance", "complexity",
            "data structure", "efficient", "big o"
        ],
        "debugging": [
            "bug", "error", "debug", "issue", "problem", "failing",
            "not working", "broken", "fix"
        ],
        "integration": [
            "integrate", "connect", "api", "third party", "service",
            "database", "external"
        ],
        "security": [
            "security", "authentication", "authorization", "vulnerability",
            "secure", "encryption", "privacy"
        ],
        "refactoring": [
            "refactor", "improve", "optimize", "clean up", "restructure",
            "modernize", "legacy"
        ]
    }
    
    detected_types = []
    for category, indicators in complexity_indicators.items():
        if any(indicator in prompt.lower() for indicator in indicators):
            detected_types.append(category)
    
    # Assess overall complexity
    question_count = len(re.findall(r'\?', prompt))
    word_count = len(prompt.split())
    technical_terms = len(re.findall(r'\b(?:implement|configure|optimize|integrate|debug|refactor)\b', prompt.lower()))
    
    complexity_score = (
        len(detected_types) * 2 +
        min(question_count, 3) +
        (1 if word_count > 100 else 0) +
        technical_terms
    )
    
    return {
        "types": detected_types,
        "score": complexity_score,
        "is_complex": complexity_score >= 3
    }


def generate_thinking_prompts(problem_analysis: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
    """Generate appropriate thinking prompts based on problem analysis."""
    prompts = []
    problem_types = problem_analysis.get("types", [])
    project_type = context.get("project_type", "generic")
    languages = context.get("languages", [])
    
    # Base deep thinking prompt
    prompts.append("Think deeply about this problem")
    
    # Type-specific prompts
    if "architectural" in problem_types:
        prompts.append("Consider scalability, maintainability, and extensibility")
        if project_type == "web":
            prompts.append("Think about frontend/backend separation and API design")
        elif project_type == "python":
            prompts.append("Consider Python design patterns and package structure")
    
    if "algorithmic" in problem_types:
        prompts.append("Analyze time and space complexity implications")
        prompts.append("Consider edge cases and optimization opportunities")
    
    if "debugging" in problem_types:
        prompts.append("Think systematically about root cause analysis")
        prompts.append("Consider debugging strategies and tools")
    
    if "integration" in problem_types:
        prompts.append("Think about data flow, error handling, and API contracts")
        prompts.append("Consider backwards compatibility and versioning")
    
    if "security" in problem_types:
        prompts.append("Consider security implications and threat vectors")
        prompts.append("Think about authentication, authorization, and data protection")
    
    if "refactoring" in problem_types:
        prompts.append("Think about incremental changes and testing strategies")
        prompts.append("Consider code quality metrics and maintainability")
    
    # Language-specific considerations
    if "python" in languages:
        prompts.append("Consider Pythonic approaches and standard library solutions")
    if "javascript" in languages:
        prompts.append("Think about async/await patterns and modern JS features")
    if "typescript" in languages:
        prompts.append("Leverage type system for better code safety")
    
    # Project context considerations
    git_state = context.get("git_state", {})
    if git_state.get("has_uncommitted_changes"):
        prompts.append("Consider how this affects existing work in progress")
    
    return prompts


def should_apply_ultra_think(prompt: str, context: Dict[str, Any]) -> bool:
    """Determine if ultra think prompts should be applied."""
    # Don't apply to simple questions
    simple_patterns = [
        r'^\s*what\s+is\s+\w+\s*\??$',
        r'^\s*how\s+to\s+\w+\s*\??$',
        r'^\s*\w+\s*[+\-*/]\s*\w+\s*$',
        r'^\s*(yes|no)\s+or\s+(no|yes)\s*\??$'
    ]
    
    if any(re.match(pattern, prompt.lower()) for pattern in simple_patterns):
        return False
    
    # Don't apply if user asks for quick/brief answers
    quick_indicators = ["quick", "briefly", "short answer", "just tell me"]
    if any(indicator in prompt.lower() for indicator in quick_indicators):
        return False
    
    # Apply for complex problems
    problem_analysis = analyze_problem_complexity(prompt)
    return problem_analysis["is_complex"]


def main(context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Enhanced ultra think hook with problem analysis."""
    # For Claude Code native hooks, read prompt from stdin
    if not context:
        try:
            prompt_input = sys.stdin.read().strip()
            prompt = prompt_input
        except:
            sys.exit(1)  # Skip if no input
    else:
        prompt = context.get("prompt", "")
    
    # Check if ultra think should be applied
    simplified_context = {"prompt": prompt, "project_type": "python", "languages": ["python"]}
    if not should_apply_ultra_think(prompt, simplified_context):
        print(prompt)  # Output unchanged prompt
        sys.exit(0)
    
    # Analyze the problem
    problem_analysis = analyze_problem_complexity(prompt)
    
    # Generate thinking prompts (simplified for native hooks)
    thinking_prompts = generate_thinking_prompts(problem_analysis, simplified_context)
    
    # Format the ultra think request
    think_request = "\n\nDEEP THINKING REQUIRED:"
    for i, prompt_text in enumerate(thinking_prompts[:5], 1):  # Limit to 5 prompts
        think_request += f"\n{i}. {prompt_text}"
    
    think_request += "\n\nProvide a comprehensive, well-reasoned solution."
    
    # Output modified prompt with thinking request
    modified_prompt = f"{prompt}{think_request}"
    print(modified_prompt)
    
    return {
        "action": "append",
        "thinking_request": think_request,
        "problem_analysis": problem_analysis,
        "prompts_used": thinking_prompts,
        "context_applied": {
            "project_type": "python",
            "languages": ["python"],
            "complexity_score": problem_analysis["score"]
        }
    }


if __name__ == "__main__":
    try:
        result = main()
        sys.exit(0)  # Success
    except Exception:
        sys.exit(1)  # Error