#!/usr/bin/env python3
"""
Hook Dispatcher for Claude Code Automation
Centralized hook management with priority-based execution and conditional logic.
"""

import json
import sys
import importlib.util
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from .context_manager import ContextManager


class HookType(Enum):
    """Types of hooks available in the system."""
    USER_PROMPT_SUBMIT = "UserPromptSubmit"
    PRE_COMMAND = "PreCommand"
    POST_COMMAND = "PostCommand"
    ON_FILE_CHANGE = "OnFileChange"
    ON_GIT_ACTION = "OnGitAction"


@dataclass
class HookConfig:
    """Configuration for a single hook."""
    name: str
    type: HookType
    priority: int = 50  # 0-100, higher = runs earlier
    enabled: bool = True
    conditions: Dict[str, Any] = None
    script_path: Optional[str] = None
    function_name: str = "main"
    description: str = ""


class HookDispatcher:
    """Centralized hook dispatcher with smart execution logic."""
    
    def __init__(self, claude_dir: Optional[str] = None):
        self.claude_dir = Path(claude_dir) if claude_dir else Path.cwd() / ".claude"
        self.context_manager = ContextManager()
        self.hooks: Dict[HookType, List[HookConfig]] = {hook_type: [] for hook_type in HookType}
        self._load_hooks()
    
    def _load_hooks(self):
        """Load all hooks from configuration and script files."""
        hooks_config_path = self.claude_dir / "settings" / "hooks.json"
        
        if hooks_config_path.exists():
            try:
                with open(hooks_config_path) as f:
                    config = json.load(f)
                    self._parse_hooks_config(config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading hooks config: {e}", file=sys.stderr)
        
        # Auto-discover hooks from directories
        self._auto_discover_hooks()
    
    def _parse_hooks_config(self, config: Dict[str, Any]):
        """Parse hooks configuration from JSON."""
        for hook_type_str, hook_list in config.get("hooks", {}).items():
            try:
                hook_type = HookType(hook_type_str)
            except ValueError:
                print(f"Unknown hook type: {hook_type_str}", file=sys.stderr)
                continue
                
            for hook_config in hook_list:
                if isinstance(hook_config, dict):
                    hook = HookConfig(
                        name=hook_config.get("name", "unnamed"),
                        type=hook_type,
                        priority=hook_config.get("priority", 50),
                        enabled=hook_config.get("enabled", True),
                        conditions=hook_config.get("conditions", {}),
                        script_path=hook_config.get("script_path"),
                        function_name=hook_config.get("function_name", "main"),
                        description=hook_config.get("description", "")
                    )
                    self.hooks[hook_type].append(hook)
    
    def _auto_discover_hooks(self):
        """Auto-discover hooks from standard directories."""
        hook_dirs = {
            HookType.USER_PROMPT_SUBMIT: "hooks/UserPromptSubmit",
            HookType.PRE_COMMAND: "hooks/pre_command",
            HookType.POST_COMMAND: "hooks/post_command",
            HookType.ON_FILE_CHANGE: "hooks/file_change",
            HookType.ON_GIT_ACTION: "hooks/git_action",
        }
        
        for hook_type, dir_path in hook_dirs.items():
            hook_dir = self.claude_dir / dir_path
            if not hook_dir.exists():
                continue
                
            for script_file in hook_dir.glob("*.py"):
                # Skip if already configured
                if any(hook.script_path == str(script_file) for hook in self.hooks[hook_type]):
                    continue
                    
                hook_name = script_file.stem
                hook = HookConfig(
                    name=hook_name,
                    type=hook_type,
                    script_path=str(script_file),
                    description=f"Auto-discovered hook: {hook_name}"
                )
                self.hooks[hook_type].append(hook)
    
    def execute_hooks(self, hook_type: HookType, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute all enabled hooks of a specific type."""
        if context is None:
            context = {}
            
        # Add project context
        context.update(self.context_manager.get_project_context())
        
        # Get applicable hooks and sort by priority
        applicable_hooks = [
            hook for hook in self.hooks[hook_type]
            if hook.enabled and self._should_run_hook(hook, context)
        ]
        applicable_hooks.sort(key=lambda h: h.priority, reverse=True)
        
        results = {}
        for hook in applicable_hooks:
            try:
                result = self._execute_single_hook(hook, context)
                results[hook.name] = result
                
                # Allow hooks to modify context for subsequent hooks
                if isinstance(result, dict):
                    context.update(result)
                    
            except Exception as e:
                print(f"Error executing hook {hook.name}: {e}", file=sys.stderr)
                results[hook.name] = {"error": str(e)}
        
        return results
    
    def _should_run_hook(self, hook: HookConfig, context: Dict[str, Any]) -> bool:
        """Determine if a hook should run based on its conditions."""
        if not hook.conditions:
            return True
            
        return self.context_manager.should_run_hook(hook.name, hook.conditions)
    
    def _execute_single_hook(self, hook: HookConfig, context: Dict[str, Any]) -> Any:
        """Execute a single hook script."""
        if not hook.script_path or not Path(hook.script_path).exists():
            return {"error": f"Script not found: {hook.script_path}"}
        
        # Load the hook script
        spec = importlib.util.spec_from_file_location(hook.name, hook.script_path)
        if not spec or not spec.loader:
            return {"error": f"Could not load script: {hook.script_path}"}
        
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            return {"error": f"Error loading module: {e}"}
        
        # Execute the hook function
        hook_function = getattr(module, hook.function_name, None)
        if not hook_function or not callable(hook_function):
            return {"error": f"Function {hook.function_name} not found or not callable"}
        
        try:
            return hook_function(context)
        except Exception as e:
            return {"error": f"Hook execution failed: {e}"}
    
    def register_hook(self, hook_config: HookConfig):
        """Register a new hook programmatically."""
        self.hooks[hook_config.type].append(hook_config)
    
    def list_hooks(self, hook_type: Optional[HookType] = None) -> List[HookConfig]:
        """List all registered hooks, optionally filtered by type."""
        if hook_type:
            return self.hooks[hook_type].copy()
        
        all_hooks = []
        for hooks_list in self.hooks.values():
            all_hooks.extend(hooks_list)
        return all_hooks
    
    def enable_hook(self, hook_name: str, enabled: bool = True):
        """Enable or disable a hook by name."""
        for hooks_list in self.hooks.values():
            for hook in hooks_list:
                if hook.name == hook_name:
                    hook.enabled = enabled
                    return True
        return False


def main():
    """CLI interface for testing hook dispatcher."""
    if len(sys.argv) < 2:
        print("Usage: hook_dispatcher.py <hook_type> [context_json]")
        sys.exit(1)
    
    try:
        hook_type = HookType(sys.argv[1])
    except ValueError:
        print(f"Invalid hook type: {sys.argv[1]}")
        print(f"Available types: {[t.value for t in HookType]}")
        sys.exit(1)
    
    context = {}
    if len(sys.argv) > 2:
        try:
            context = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(f"Invalid JSON context: {e}")
            sys.exit(1)
    
    dispatcher = HookDispatcher()
    results = dispatcher.execute_hooks(hook_type, context)
    
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()