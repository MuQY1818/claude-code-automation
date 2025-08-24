#!/usr/bin/env python3
"""
Command Registry for Claude Code Automation
Advanced command management with categories, validation, and chaining.
"""

import json
import sys
import subprocess
from typing import Dict, Any, List, Optional, Callable, Union
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

from .context_manager import ContextManager
from .hook_dispatcher import HookDispatcher, HookType


class CommandCategory(Enum):
    """Categories for organizing commands."""
    GIT = "git"
    ANALYSIS = "analysis"
    DEVELOPMENT = "development"
    DEPLOYMENT = "deployment"
    SECURITY = "security"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    UTILITY = "utility"


@dataclass
class CommandParameter:
    """Definition for a command parameter."""
    name: str
    type: type = str
    required: bool = True
    default: Any = None
    description: str = ""
    choices: Optional[List[Any]] = None
    validation_pattern: Optional[str] = None


@dataclass
class CommandDefinition:
    """Complete definition of a command."""
    name: str
    category: CommandCategory
    description: str
    parameters: List[CommandParameter] = field(default_factory=list)
    script_path: Optional[str] = None
    command_template: Optional[str] = None
    requires_git: bool = False
    requires_tools: List[str] = field(default_factory=list)
    pre_hooks: List[str] = field(default_factory=list)
    post_hooks: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)


class CommandExecutor(ABC):
    """Abstract base class for command executors."""
    
    @abstractmethod
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the command with given parameters and context."""
        pass


class ScriptCommandExecutor(CommandExecutor):
    """Executor for script-based commands."""
    
    def __init__(self, script_path: str):
        self.script_path = Path(script_path)
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.script_path.exists():
            return {"success": False, "error": f"Script not found: {self.script_path}"}
        
        try:
            import os
            # Prepare environment with parameters and context
            env = dict(os.environ)
            for key, value in params.items():
                env[f"CLAUDE_PARAM_{key.upper()}"] = str(value)
            for key, value in context.items():
                if isinstance(value, (str, int, float, bool)):
                    env[f"CLAUDE_CONTEXT_{key.upper()}"] = str(value)
            
            result = subprocess.run(
                [sys.executable, str(self.script_path)],
                capture_output=True,
                text=True,
                env=env
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class TemplateCommandExecutor(CommandExecutor):
    """Executor for template-based commands."""
    
    def __init__(self, template: str):
        self.template = template
    
    def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Replace template variables
            command = self.template
            for key, value in params.items():
                command = command.replace(f"{{{key}}}", str(value))
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "command": command
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class CommandRegistry:
    """Registry for managing and executing commands."""
    
    def __init__(self, claude_dir: Optional[str] = None):
        self.claude_dir = Path(claude_dir) if claude_dir else Path.cwd() / ".claude"
        self.context_manager = ContextManager()
        self.hook_dispatcher = HookDispatcher(str(self.claude_dir))
        self.commands: Dict[str, CommandDefinition] = {}
        self.executors: Dict[str, CommandExecutor] = {}
        self._load_commands()
    
    def _load_commands(self):
        """Load commands from configuration files and auto-discover."""
        # Load from configuration
        commands_config = self.claude_dir / "settings" / "commands.json"
        if commands_config.exists():
            try:
                with open(commands_config) as f:
                    config = json.load(f)
                    self._parse_commands_config(config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading commands config: {e}", file=sys.stderr)
        
        # Auto-discover commands
        self._auto_discover_commands()
    
    def _parse_commands_config(self, config: Dict[str, Any]):
        """Parse commands from configuration."""
        for cmd_data in config.get("commands", []):
            try:
                # Parse parameters
                parameters = []
                for param_data in cmd_data.get("parameters", []):
                    param = CommandParameter(
                        name=param_data["name"],
                        type=eval(param_data.get("type", "str")),  # Note: In production, use safer evaluation
                        required=param_data.get("required", True),
                        default=param_data.get("default"),
                        description=param_data.get("description", ""),
                        choices=param_data.get("choices"),
                        validation_pattern=param_data.get("validation_pattern")
                    )
                    parameters.append(param)
                
                # Create command definition
                cmd_def = CommandDefinition(
                    name=cmd_data["name"],
                    category=CommandCategory(cmd_data.get("category", "utility")),
                    description=cmd_data.get("description", ""),
                    parameters=parameters,
                    script_path=cmd_data.get("script_path"),
                    command_template=cmd_data.get("command_template"),
                    requires_git=cmd_data.get("requires_git", False),
                    requires_tools=cmd_data.get("requires_tools", []),
                    pre_hooks=cmd_data.get("pre_hooks", []),
                    post_hooks=cmd_data.get("post_hooks", []),
                    examples=cmd_data.get("examples", []),
                    aliases=cmd_data.get("aliases", [])
                )
                
                self.register_command(cmd_def)
                
            except (KeyError, ValueError) as e:
                print(f"Error parsing command {cmd_data.get('name', 'unknown')}: {e}", file=sys.stderr)
    
    def _auto_discover_commands(self):
        """Auto-discover commands from directory structure."""
        commands_dir = self.claude_dir / "commands"
        if not commands_dir.exists():
            return
        
        for category_dir in commands_dir.iterdir():
            if not category_dir.is_dir():
                continue
            
            try:
                category = CommandCategory(category_dir.name)
            except ValueError:
                continue
            
            for cmd_file in category_dir.glob("*.py"):
                cmd_name = cmd_file.stem
                if cmd_name in self.commands:
                    continue  # Skip if already registered
                
                # Create basic command definition
                cmd_def = CommandDefinition(
                    name=cmd_name,
                    category=category,
                    description=f"Auto-discovered command: {cmd_name}",
                    script_path=str(cmd_file)
                )
                
                self.register_command(cmd_def)
    
    def register_command(self, command: CommandDefinition):
        """Register a command in the registry."""
        self.commands[command.name] = command
        
        # Register aliases
        for alias in command.aliases:
            self.commands[alias] = command
        
        # Create appropriate executor
        if command.script_path:
            self.executors[command.name] = ScriptCommandExecutor(command.script_path)
        elif command.command_template:
            self.executors[command.name] = TemplateCommandExecutor(command.command_template)
    
    def execute_command(self, command_name: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a command with given parameters."""
        if command_name not in self.commands:
            return {"success": False, "error": f"Unknown command: {command_name}"}
        
        command = self.commands[command_name]
        params = params or {}
        
        # Validate prerequisites
        validation_result = self._validate_command_prerequisites(command)
        if not validation_result["success"]:
            return validation_result
        
        # Validate parameters
        param_validation = self._validate_parameters(command, params)
        if not param_validation["success"]:
            return param_validation
        
        # Get context
        context = self.context_manager.get_project_context()
        context["command_name"] = command_name
        
        try:
            # Execute pre-hooks
            if command.pre_hooks:
                pre_hook_context = {"command": command_name, "params": params, **context}
                self.hook_dispatcher.execute_hooks(HookType.PRE_COMMAND, pre_hook_context)
            
            # Execute the command
            executor = self.executors.get(command_name)
            if not executor:
                return {"success": False, "error": "No executor found for command"}
            
            result = executor.execute(params, context)
            
            # Execute post-hooks
            if command.post_hooks:
                post_hook_context = {
                    "command": command_name,
                    "params": params,
                    "result": result,
                    **context
                }
                self.hook_dispatcher.execute_hooks(HookType.POST_COMMAND, post_hook_context)
            
            return result
            
        except Exception as e:
            return {"success": False, "error": f"Command execution failed: {e}"}
    
    def _validate_command_prerequisites(self, command: CommandDefinition) -> Dict[str, Any]:
        """Validate that command prerequisites are met."""
        context = self.context_manager.get_project_context()
        
        # Check git requirement
        if command.requires_git and not context["git_state"]["is_git_repo"]:
            return {"success": False, "error": "This command requires a git repository"}
        
        # Check required tools
        missing_tools = []
        for tool in command.requires_tools:
            if not context["tools"].get(tool, False):
                missing_tools.append(tool)
        
        if missing_tools:
            return {
                "success": False,
                "error": f"Missing required tools: {', '.join(missing_tools)}"
            }
        
        return {"success": True}
    
    def _validate_parameters(self, command: CommandDefinition, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate command parameters."""
        errors = []
        
        # Check required parameters
        for param in command.parameters:
            if param.required and param.name not in params:
                if param.default is not None:
                    params[param.name] = param.default
                else:
                    errors.append(f"Required parameter missing: {param.name}")
            
            # Validate parameter values
            if param.name in params:
                value = params[param.name]
                
                # Type validation
                if not isinstance(value, param.type):
                    try:
                        params[param.name] = param.type(value)
                    except (ValueError, TypeError):
                        errors.append(f"Parameter {param.name} must be of type {param.type.__name__}")
                
                # Choice validation
                if param.choices and params[param.name] not in param.choices:
                    errors.append(f"Parameter {param.name} must be one of: {param.choices}")
                
                # Pattern validation
                if param.validation_pattern:
                    import re
                    if not re.match(param.validation_pattern, str(params[param.name])):
                        errors.append(f"Parameter {param.name} doesn't match required pattern")
        
        if errors:
            return {"success": False, "error": "; ".join(errors)}
        
        return {"success": True}
    
    def list_commands(self, category: Optional[CommandCategory] = None) -> List[CommandDefinition]:
        """List all commands, optionally filtered by category."""
        commands = list(self.commands.values())
        
        # Remove duplicates (from aliases)
        unique_commands = {}
        for cmd in commands:
            if cmd.name not in unique_commands:
                unique_commands[cmd.name] = cmd
        
        commands = list(unique_commands.values())
        
        if category:
            commands = [cmd for cmd in commands if cmd.category == category]
        
        return sorted(commands, key=lambda c: (c.category.value, c.name))
    
    def get_command_help(self, command_name: str) -> Optional[str]:
        """Get help text for a command."""
        if command_name not in self.commands:
            return None
        
        command = self.commands[command_name]
        help_text = f"Command: {command.name}\n"
        help_text += f"Category: {command.category.value}\n"
        help_text += f"Description: {command.description}\n\n"
        
        if command.parameters:
            help_text += "Parameters:\n"
            for param in command.parameters:
                required_str = "required" if param.required else "optional"
                help_text += f"  {param.name} ({param.type.__name__}, {required_str})"
                if param.default is not None:
                    help_text += f", default: {param.default}"
                help_text += f"\n    {param.description}\n"
                if param.choices:
                    help_text += f"    Choices: {param.choices}\n"
        
        if command.examples:
            help_text += "\nExamples:\n"
            for example in command.examples:
                help_text += f"  {example}\n"
        
        if command.aliases:
            help_text += f"\nAliases: {', '.join(command.aliases)}\n"
        
        return help_text


def main():
    """CLI interface for command registry."""
    if len(sys.argv) < 2:
        print("Usage: command_registry.py <list|help|execute> [args...]")
        sys.exit(1)
    
    registry = CommandRegistry()
    action = sys.argv[1]
    
    if action == "list":
        category = None
        if len(sys.argv) > 2:
            try:
                category = CommandCategory(sys.argv[2])
            except ValueError:
                print(f"Invalid category: {sys.argv[2]}")
                sys.exit(1)
        
        commands = registry.list_commands(category)
        for cmd in commands:
            print(f"{cmd.name} ({cmd.category.value}): {cmd.description}")
    
    elif action == "help":
        if len(sys.argv) < 3:
            print("Usage: command_registry.py help <command_name>")
            sys.exit(1)
        
        help_text = registry.get_command_help(sys.argv[2])
        if help_text:
            print(help_text)
        else:
            print(f"Command not found: {sys.argv[2]}")
    
    elif action == "execute":
        if len(sys.argv) < 3:
            print("Usage: command_registry.py execute <command_name> [params_json]")
            sys.exit(1)
        
        params = {}
        if len(sys.argv) > 3:
            try:
                params = json.loads(sys.argv[3])
            except json.JSONDecodeError as e:
                print(f"Invalid JSON parameters: {e}")
                sys.exit(1)
        
        result = registry.execute_command(sys.argv[2], params)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)


if __name__ == "__main__":
    main()