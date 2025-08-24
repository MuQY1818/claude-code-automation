#!/usr/bin/env python3
"""
Context Manager for Claude Code Automation
Detects project context and provides smart automation decisions.
"""

import os
import json
import subprocess
from typing import Dict, Any, Optional, List
from pathlib import Path


class ContextManager:
    """Manages project context and environment detection."""
    
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self._context_cache = {}
    
    def get_project_context(self) -> Dict[str, Any]:
        """Get comprehensive project context."""
        if self._context_cache:
            return self._context_cache
            
        context = {
            "project_type": self._detect_project_type(),
            "git_state": self._get_git_state(),
            "languages": self._detect_languages(),
            "frameworks": self._detect_frameworks(),
            "tools": self._detect_tools(),
            "project_root": str(self.project_root),
        }
        
        self._context_cache = context
        return context
    
    def _detect_project_type(self) -> str:
        """Detect the primary project type."""
        indicators = {
            "web": ["package.json", "yarn.lock", "webpack.config.js"],
            "python": ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile"],
            "java": ["pom.xml", "build.gradle", "gradlew"],
            "rust": ["Cargo.toml"],
            "go": ["go.mod", "go.sum"],
            "docker": ["Dockerfile", "docker-compose.yml"],
        }
        
        for proj_type, files in indicators.items():
            if any((self.project_root / file).exists() for file in files):
                return proj_type
        return "generic"
    
    def _get_git_state(self) -> Dict[str, Any]:
        """Get current git repository state."""
        try:
            # Check if it's a git repo
            subprocess.run(["git", "rev-parse", "--git-dir"], 
                         capture_output=True, check=True, cwd=self.project_root)
            
            # Get current branch
            branch_result = subprocess.run(["git", "branch", "--show-current"], 
                                         capture_output=True, text=True, cwd=self.project_root)
            current_branch = branch_result.stdout.strip()
            
            # Check for uncommitted changes
            status_result = subprocess.run(["git", "status", "--porcelain"], 
                                         capture_output=True, text=True, cwd=self.project_root)
            has_changes = bool(status_result.stdout.strip())
            
            return {
                "is_git_repo": True,
                "current_branch": current_branch,
                "has_uncommitted_changes": has_changes,
                "is_main_branch": current_branch in ["main", "master"],
            }
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {"is_git_repo": False}
    
    def _detect_languages(self) -> List[str]:
        """Detect programming languages used in the project."""
        extensions = {
            ".py": "python", ".js": "javascript", ".ts": "typescript",
            ".java": "java", ".rs": "rust", ".go": "go",
            ".cpp": "cpp", ".c": "c", ".cs": "csharp",
            ".rb": "ruby", ".php": "php", ".swift": "swift",
        }
        
        detected = set()
        for file_path in self.project_root.rglob("*"):
            if file_path.suffix in extensions:
                detected.add(extensions[file_path.suffix])
                
        return list(detected)
    
    def _detect_frameworks(self) -> List[str]:
        """Detect frameworks and libraries in use."""
        frameworks = []
        
        # Check package.json for JS frameworks
        package_json = self.project_root / "package.json"
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                    
                    framework_indicators = {
                        "react": "react", "vue": "vue", "angular": "angular",
                        "express": "express", "fastify": "fastify",
                        "next": "next.js", "nuxt": "nuxt.js",
                    }
                    
                    for dep, framework in framework_indicators.items():
                        if dep in deps:
                            frameworks.append(framework)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Check requirements.txt for Python frameworks
        requirements = self.project_root / "requirements.txt"
        if requirements.exists():
            try:
                with open(requirements) as f:
                    content = f.read().lower()
                    python_frameworks = {
                        "django": "django", "flask": "flask", "fastapi": "fastapi",
                        "streamlit": "streamlit", "gradio": "gradio",
                    }
                    
                    for indicator, framework in python_frameworks.items():
                        if indicator in content:
                            frameworks.append(framework)
            except IOError:
                pass
                
        return frameworks
    
    def _detect_tools(self) -> Dict[str, bool]:
        """Detect development tools and their availability."""
        tools = {}
        
        # Check for common tools
        tool_commands = {
            "git": ["git", "--version"],
            "docker": ["docker", "--version"],
            "npm": ["npm", "--version"],
            "yarn": ["yarn", "--version"],
            "pip": ["pip", "--version"],
        }
        
        for tool, cmd in tool_commands.items():
            try:
                subprocess.run(cmd, capture_output=True, check=True)
                tools[tool] = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                tools[tool] = False
        
        return tools
    
    def should_run_hook(self, hook_name: str, conditions: Dict[str, Any]) -> bool:
        """Determine if a hook should run based on context conditions."""
        context = self.get_project_context()
        
        for condition, expected in conditions.items():
            if condition == "project_type":
                if context["project_type"] != expected:
                    return False
            elif condition == "git_repo":
                if context["git_state"]["is_git_repo"] != expected:
                    return False
            elif condition == "has_changes":
                if context["git_state"].get("has_uncommitted_changes", False) != expected:
                    return False
            elif condition == "language":
                if expected not in context["languages"]:
                    return False
            elif condition == "framework":
                if expected not in context["frameworks"]:
                    return False
        
        return True