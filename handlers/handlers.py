"""
Main handlers for skill-squared operations
Core business logic for create, add_command, sync, and validate operations
"""

import os
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from .templates import TemplateManager
from .validators import SkillValidator
from .sync import SkillSync


def create_skill(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new skill project structure

    Args:
        payload: Dictionary containing:
            - skill_name: str (kebab-case name)
            - skill_description: str
            - author_name: str
            - author_email: str
            - github_user: str
            - target_dir: str (optional, defaults to current directory)
            - version: str (optional, defaults to '0.1.0')

    Returns:
        Dictionary with:
            - success: bool
            - message: str
            - data: dict with created_files list
    """
    try:
        # Extract parameters
        skill_name = payload.get('skill_name', '').strip()
        skill_description = payload.get('skill_description', '').strip()
        author_name = payload.get('author_name', '').strip()
        author_email = payload.get('author_email', '').strip()
        github_user = payload.get('github_user', '').strip()
        target_dir = payload.get('target_dir', os.getcwd())
        version = payload.get('version', '0.1.0')

        # Validate inputs
        if not skill_name:
            return {'success': False, 'error': 'skill_name is required'}
        if not skill_description:
            return {'success': False, 'error': 'skill_description is required'}
        if not author_name:
            return {'success': False, 'error': 'author_name is required'}
        if not author_email:
            return {'success': False, 'error': 'author_email is required'}
        if not github_user:
            return {'success': False, 'error': 'github_user is required'}

        # Validate skill_name format (kebab-case)
        if not all(c.islower() or c.isdigit() or c == '-' for c in skill_name):
            return {'success': False, 'error': 'skill_name must be in kebab-case (lowercase with hyphens)'}

        # Create skill directory
        skill_path = Path(target_dir) / skill_name
        if skill_path.exists():
            return {'success': False, 'error': f'Directory already exists: {skill_path}'}

        skill_path.mkdir(parents=True, exist_ok=False)

        # Prepare template context
        context = {
            'skill_name': skill_name,
            'skill_description': skill_description,
            'author_name': author_name,
            'author_email': author_email,
            'github_user': github_user,
            'version': version
        }

        # Initialize template manager
        template_manager = TemplateManager()

        created_files = []

        # Create directory structure
        directories = [
            '.claude-plugin',
            '.claude/commands',
            'skills',
            'handlers',
            'templates/skill',
            'templates/command',
            'config',
            'docs'
        ]

        for dir_name in directories:
            dir_path = skill_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)

        # Create files from templates
        file_templates = {
            '.claude-plugin/marketplace.json': 'skill/marketplace.json.template',
            '.claude-plugin/plugin.json': 'skill/plugin.json.template',
            f'skills/{skill_name}.md': 'skill/skill.md.template',
            'README.md': 'skill/README.md.template',
            '.claude/CLAUDE.md': 'skill/CLAUDE.md.template',
            'install.sh': 'skill/install.sh.template'
        }

        for file_path, template_name in file_templates.items():
            full_path = skill_path / file_path
            try:
                rendered = template_manager.render(template_name, context)
                full_path.write_text(rendered, encoding='utf-8')
                created_files.append(str(file_path))
            except FileNotFoundError:
                return {
                    'success': False,
                    'error': f'Template not found: {template_name}'
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Failed to create {file_path}: {str(e)}'
                }

        # Create additional files (not from templates)

        # .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/

# Virtual environments
venv/
ENV/
env/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Claude Code
.claude/settings.local.json
.claude/plans/

# Testing
.pytest_cache/
.coverage
htmlcov/
"""
        (skill_path / '.gitignore').write_text(gitignore_content, encoding='utf-8')
        created_files.append('.gitignore')

        # LICENSE
        license_content = f"""MIT License

Copyright (c) {datetime.now().year} {author_name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        (skill_path / 'LICENSE').write_text(license_content, encoding='utf-8')
        created_files.append('LICENSE')

        # Make install.sh executable
        install_sh = skill_path / 'install.sh'
        install_sh.chmod(install_sh.stat().st_mode | 0o111)

        return {
            'success': True,
            'message': f'Successfully created skill: {skill_name}',
            'data': {
                'skill_name': skill_name,
                'skill_path': str(skill_path),
                'created_files': created_files
            }
        }

    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }


def add_command(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a slash command to an existing skill

    Args:
        payload: Dictionary containing:
            - skill_dir: str (path to skill directory)
            - command_name: str (kebab-case name)
            - command_description: str
            - command_instructions: str (optional)

    Returns:
        Dictionary with:
            - success: bool
            - message: str
            - data: dict with command info
    """
    try:
        # Extract parameters
        skill_dir = payload.get('skill_dir', '').strip()
        command_name = payload.get('command_name', '').strip()
        command_description = payload.get('command_description', '').strip()
        command_instructions = payload.get('command_instructions', '').strip()

        # Validate inputs
        if not skill_dir:
            return {'success': False, 'error': 'skill_dir is required'}
        if not command_name:
            return {'success': False, 'error': 'command_name is required'}
        if not command_description:
            return {'success': False, 'error': 'command_description is required'}

        # Validate skill directory exists
        skill_path = Path(skill_dir)
        if not skill_path.exists():
            return {'success': False, 'error': f'Skill directory not found: {skill_dir}'}

        # Validate command_name format (kebab-case)
        if not all(c.islower() or c.isdigit() or c == '-' for c in command_name):
            return {'success': False, 'error': 'command_name must be in kebab-case (lowercase with hyphens)'}

        # Check if commands directory exists
        commands_dir = skill_path / '.claude' / 'commands'
        if not commands_dir.exists():
            commands_dir.mkdir(parents=True, exist_ok=True)

        # Check if command already exists
        command_file = commands_dir / f'{command_name}.md'
        if command_file.exists():
            return {'success': False, 'error': f'Command already exists: {command_name}'}

        # Create command content with frontmatter
        if not command_instructions:
            command_instructions = f"Use the skill to handle {command_name} requests."

        command_content = f"""---
description: {command_description}
---

# {command_name.replace('-', ' ').title()}

{command_instructions}

## Usage

This command should:

1. Process the user's request
2. Perform necessary operations
3. Return results to the user

## Example

**User request**:
```
[Example request]
```

**Expected behavior**:
```
[Expected behavior description]
```
"""

        # Write command file
        command_file.write_text(command_content, encoding='utf-8')

        # Update plugin.json to include the new command
        plugin_json_path = skill_path / '.claude-plugin' / 'plugin.json'
        if plugin_json_path.exists():
            try:
                with open(plugin_json_path, 'r', encoding='utf-8') as f:
                    plugin_data = json.load(f)

                # Add command to commands array
                if 'commands' not in plugin_data:
                    plugin_data['commands'] = []

                plugin_data['commands'].append(f'./.claude/commands/{command_name}.md')

                # Write back
                with open(plugin_json_path, 'w', encoding='utf-8') as f:
                    json.dump(plugin_data, f, indent=2, ensure_ascii=False)

            except Exception as e:
                # Command file was created, but updating plugin.json failed
                return {
                    'success': True,
                    'message': f'Command created but failed to update plugin.json: {str(e)}',
                    'data': {
                        'command_name': command_name,
                        'command_file': str(command_file.relative_to(skill_path)),
                        'warning': 'Manually update plugin.json to register this command'
                    }
                }

        return {
            'success': True,
            'message': f'Successfully added command: {command_name}',
            'data': {
                'command_name': command_name,
                'command_file': str(command_file.relative_to(skill_path)),
                'description': command_description
            }
        }

    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }


def sync_skill(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sync skill from standalone repository to marketplace

    Args:
        payload: Dictionary containing:
            - source_dir: str (path to standalone skill directory)
            - target_dir: str (path to marketplace directory)
            - skill_name: str
            - dry_run: bool (optional, default False)

    Returns:
        Dictionary with:
            - success: bool
            - message: str
            - data: dict with sync results
    """
    try:
        # Extract parameters
        source_dir = payload.get('source_dir', '').strip()
        target_dir = payload.get('target_dir', '').strip()
        skill_name = payload.get('skill_name', '').strip()
        dry_run = payload.get('dry_run', False)

        # Validate inputs
        if not source_dir:
            return {'success': False, 'error': 'source_dir is required'}
        if not target_dir:
            return {'success': False, 'error': 'target_dir is required'}
        if not skill_name:
            return {'success': False, 'error': 'skill_name is required'}

        # Validate paths exist
        source_path = Path(source_dir)
        target_path = Path(target_dir)

        if not source_path.exists():
            return {'success': False, 'error': f'Source directory not found: {source_dir}'}
        if not target_path.exists():
            return {'success': False, 'error': f'Target directory not found: {target_dir}'}

        # Perform sync
        syncer = SkillSync()
        result = syncer.sync(source_dir, target_dir, skill_name, dry_run)

        if not result.is_success():
            return {
                'success': False,
                'error': 'Sync failed',
                'data': result.to_dict()
            }

        mode = 'DRY RUN' if dry_run else 'Synced'
        return {
            'success': True,
            'message': f'{mode}: {len(result.copied_files)} file(s) synced',
            'data': result.to_dict()
        }

    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }


def validate_skill(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate skill structure and configuration

    Args:
        payload: Dictionary containing:
            - skill_dir: str (path to skill directory)
            - skill_name: str (optional, auto-detected if not provided)

    Returns:
        Dictionary with:
            - success: bool (True if valid, False if errors found)
            - message: str
            - data: dict with validation results
    """
    try:
        # Extract parameters
        skill_dir = payload.get('skill_dir', '').strip()
        skill_name = payload.get('skill_name', '').strip() or None

        # Validate input
        if not skill_dir:
            return {'success': False, 'error': 'skill_dir is required'}

        # Perform validation
        validator = SkillValidator()
        result = validator.validate_skill(skill_dir, skill_name)

        validation_data = result.to_dict()

        if result.is_valid():
            return {
                'success': True,
                'message': 'Skill validation passed',
                'data': validation_data
            }
        else:
            return {
                'success': False,
                'message': f'Skill validation failed with {len(result.errors)} error(s)',
                'data': validation_data
            }

    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }


# Expose handlers for easy importing
__all__ = ['create_skill', 'add_command', 'sync_skill', 'validate_skill']
