#!/usr/bin/env python3
"""
Flag Dispatcher Hook
Central flag processing system for shortcut commands like -ut, -debug, etc.
This hook processes flags and modifies prompts accordingly before passing to other hooks.
"""

import sys
import re
import os
from typing import Dict, List, Tuple, Any


class FlagProcessor:
    """Processes command flags and generates appropriate prompt modifications."""
    
    def __init__(self):
        self.flags = {
            # User requested flags
            '-ut': {
                'description': 'Ultra Think mode - deep analysis with comprehensive reasoning',
                'conflicts': ['-quick'],
                'append': '\n\nUSE ULTRA THINK MODE: Analyze this problem deeply. Consider all possible approaches, edge cases, and implications. Provide comprehensive reasoning for your solution.'
            },
            '-debug': {
                'description': 'Debug mode - systematic error analysis and troubleshooting',
                'conflicts': ['-quick'],
                'append': '\n\nDEBUG MODE ACTIVATED: Systematically analyze the error information above. Find the root cause, provide debugging steps, and suggest concrete solutions.'
            },
            
            # Additional recommended flags
            '-quick': {
                'description': 'Quick mode - brief, concise answers only',
                'conflicts': ['-ut', '-debug', '-explain'],
                'append': '\n\nQUICK MODE: Provide only brief, essential information. No detailed explanations.'
            },
            '-explain': {
                'description': 'Explain mode - detailed explanations and teaching',
                'conflicts': ['-quick', '-code'],
                'append': '\n\nEXPLAIN MODE: Provide detailed explanations, break down concepts, and teach the underlying principles.'
            },
            '-code': {
                'description': 'Code mode - focus on implementation with minimal explanation',
                'conflicts': ['-explain'],
                'append': '\n\nCODE FOCUS MODE: Provide working code implementations with minimal explanations. Focus on practical solutions.'
            },
            '-review': {
                'description': 'Review mode - code review with best practices',
                'conflicts': [],
                'append': '\n\nCODE REVIEW MODE: Analyze code quality, suggest improvements, check for best practices, and identify potential issues.'
            },
            '-secure': {
                'description': 'Security mode - focus on security implications',
                'conflicts': [],
                'append': '\n\nSECURITY MODE: Analyze security implications, identify vulnerabilities, and provide security best practices.'
            },
            '-optimize': {
                'description': 'Optimization mode - performance and efficiency focus',
                'conflicts': [],
                'append': '\n\nOPTIMIZATION MODE: Focus on performance improvements, efficiency gains, and resource optimization.'
            },
            '-refactor': {
                'description': 'Refactor mode - code restructuring suggestions',
                'conflicts': [],
                'append': '\n\nREFACTOR MODE: Suggest code improvements, better structure, and maintainability enhancements.'
            },
            '-test': {
                'description': 'Test mode - testing strategies and implementation',
                'conflicts': [],
                'append': '\n\nTEST MODE: Focus on testing strategies, test implementation, and quality assurance approaches.'
            }
        }
    
    def detect_flags(self, prompt: str) -> List[str]:
        """Detect all flags present in the prompt."""
        detected = []
        for flag in self.flags.keys():
            if flag in prompt:
                detected.append(flag)
        return detected
    
    def check_conflicts(self, flags: List[str]) -> List[str]:
        """Check for conflicting flags and return conflicts found."""
        conflicts = []
        for flag in flags:
            flag_conflicts = self.flags[flag].get('conflicts', [])
            for conflict in flag_conflicts:
                if conflict in flags:
                    conflicts.append(f"{flag} conflicts with {conflict}")
        return conflicts
    
    def process_flags(self, prompt: str) -> Tuple[str, List[str], Dict[str, Any]]:
        """
        Process flags in prompt and return modified prompt with metadata.
        
        Returns:
            Tuple of (modified_prompt, detected_flags, processing_info)
        """
        detected_flags = self.detect_flags(prompt)
        
        if not detected_flags:
            return prompt, [], {'action': 'none', 'reason': 'no_flags_detected'}
        
        # Check for conflicts
        conflicts = self.check_conflicts(detected_flags)
        if conflicts:
            # In case of conflicts, prioritize based on order of appearance
            # Keep the first flag found, remove conflicting ones
            resolved_flags = []
            for flag in detected_flags:
                flag_conflicts = self.flags[flag].get('conflicts', [])
                if not any(conflict in resolved_flags for conflict in flag_conflicts):
                    resolved_flags.append(flag)
            
            processing_info = {
                'action': 'conflict_resolution',
                'conflicts_found': conflicts,
                'original_flags': detected_flags,
                'resolved_flags': resolved_flags
            }
            detected_flags = resolved_flags
        else:
            processing_info = {
                'action': 'processed',
                'conflicts_found': [],
                'flags_processed': detected_flags
            }
        
        # Remove flags from prompt
        cleaned_prompt = prompt
        for flag in self.flags.keys():
            cleaned_prompt = cleaned_prompt.replace(flag, '')
        
        # Clean up extra whitespace
        cleaned_prompt = ' '.join(cleaned_prompt.split())
        
        # Append flag-specific instructions
        append_text = ""
        for flag in detected_flags:
            append_text += self.flags[flag]['append']
        
        modified_prompt = cleaned_prompt + append_text
        
        return modified_prompt, detected_flags, processing_info


def main():
    """Main hook entry point for Claude Code native hooks."""
    try:
        # Read prompt from stdin
        prompt_input = sys.stdin.read().strip()
        
        if not prompt_input:
            sys.exit(1)  # No input, skip processing
        
        # Process flags
        processor = FlagProcessor()
        modified_prompt, flags_used, processing_info = processor.process_flags(prompt_input)
        
        # Output modified prompt
        print(modified_prompt)
        
        # For debugging (only if debug environment variable is set)
        if os.getenv('CLAUDE_HOOK_DEBUG'):
            debug_info = {
                'hook': 'flag_dispatcher',
                'flags_detected': flags_used,
                'processing_info': processing_info,
                'original_length': len(prompt_input),
                'modified_length': len(modified_prompt)
            }
            print(f"<!-- DEBUG: {debug_info} -->", file=sys.stderr)
        
        sys.exit(0)  # Success
        
    except Exception as e:
        # In case of error, output original prompt unchanged
        try:
            prompt_input = sys.stdin.read().strip()
            print(prompt_input)
        except:
            pass
        
        if os.getenv('CLAUDE_HOOK_DEBUG'):
            print(f"flag_dispatcher error: {e}", file=sys.stderr)
        
        sys.exit(1)  # Error


if __name__ == "__main__":
    main()