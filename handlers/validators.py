"""
Validation logic for skill-squared
Validates skill structure, configuration, and files
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple


class ValidationResult:
    """Container for validation results"""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def add_error(self, message: str):
        """Add an error message"""
        self.errors.append(message)

    def add_warning(self, message: str):
        """Add a warning message"""
        self.warnings.append(message)

    def add_info(self, message: str):
        """Add an info message"""
        self.info.append(message)

    def is_valid(self) -> bool:
        """Check if validation passed (no errors)"""
        return len(self.errors) == 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'valid': self.is_valid(),
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info
        }


class SkillValidator:
    """Validates Claude Code skill structure and configuration"""

    def __init__(self, config_path: str = None):
        """
        Initialize validator

        Args:
            config_path: Path to config.json (optional)
        """
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Load validation configuration"""
        if config_path:
            config_file = Path(config_path)
        else:
            # Default to config/config.json in project root
            project_root = Path(__file__).parent.parent
            config_file = project_root / 'config' / 'config.json'

        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Return default config
            return {
                'validation': {
                    'required_files': [
                        '.claude-plugin/marketplace.json',
                        '.claude-plugin/plugin.json',
                        'skills/{skill_name}.md',
                        'install.sh',
                        'README.md'
                    ],
                    'required_frontmatter': ['name', 'description'],
                    'executable_files': ['install.sh']
                }
            }

    def validate_skill(self, skill_dir: str, skill_name: str = None) -> ValidationResult:
        """
        Comprehensive skill validation

        Args:
            skill_dir: Path to skill directory
            skill_name: Optional skill name (auto-detected if not provided)

        Returns:
            ValidationResult object
        """
        result = ValidationResult()
        skill_path = Path(skill_dir)

        # Check directory exists
        if not skill_path.exists():
            result.add_error(f"Skill directory not found: {skill_dir}")
            return result

        if not skill_path.is_dir():
            result.add_error(f"Path is not a directory: {skill_dir}")
            return result

        result.add_info(f"Validating skill at: {skill_path}")

        # Auto-detect skill name if not provided
        if not skill_name:
            skill_name = self._detect_skill_name(skill_path)
            if skill_name:
                result.add_info(f"Detected skill name: {skill_name}")
            else:
                result.add_warning("Could not auto-detect skill name")

        # Validate required files
        self._validate_required_files(skill_path, skill_name, result)

        # Validate JSON files
        self._validate_json_files(skill_path, result)

        # Validate skill definition
        if skill_name:
            self._validate_skill_definition(skill_path, skill_name, result)

        # Validate file permissions
        self._validate_permissions(skill_path, result)

        # Additional checks
        self._validate_commands(skill_path, result)

        return result

    def _detect_skill_name(self, skill_path: Path) -> str:
        """
        Auto-detect skill name from plugin.json or directory

        Args:
            skill_path: Path to skill directory

        Returns:
            Detected skill name or None
        """
        # Try to read from plugin.json
        plugin_json = skill_path / '.claude-plugin' / 'plugin.json'
        if plugin_json.exists():
            try:
                with open(plugin_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('name')
            except:
                pass

        # Try to find skill.md file in skills/ directory
        skills_dir = skill_path / 'skills'
        if skills_dir.exists():
            skill_files = list(skills_dir.glob('*.md'))
            if len(skill_files) == 1:
                return skill_files[0].stem

        # Fall back to directory name
        return skill_path.name

    def _validate_required_files(self, skill_path: Path, skill_name: str, result: ValidationResult):
        """Validate required files exist"""
        required_files = self.config['validation']['required_files']

        for file_pattern in required_files:
            # Substitute skill_name if present
            if skill_name:
                file_path = file_pattern.replace('{skill_name}', skill_name)
            else:
                file_path = file_pattern

            full_path = skill_path / file_path

            if not full_path.exists():
                result.add_error(f"Required file missing: {file_path}")
            else:
                result.add_info(f"Found: {file_path}")

    def _validate_json_files(self, skill_path: Path, result: ValidationResult):
        """Validate JSON syntax in configuration files"""
        json_files = [
            '.claude-plugin/marketplace.json',
            '.claude-plugin/plugin.json'
        ]

        for json_file in json_files:
            file_path = skill_path / json_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json.load(f)
                    result.add_info(f"Valid JSON: {json_file}")
                except json.JSONDecodeError as e:
                    result.add_error(f"Invalid JSON in {json_file}: {str(e)}")

    def _validate_skill_definition(self, skill_path: Path, skill_name: str, result: ValidationResult):
        """Validate skill definition markdown file"""
        skill_md = skill_path / 'skills' / f'{skill_name}.md'

        if not skill_md.exists():
            result.add_error(f"Skill definition not found: skills/{skill_name}.md")
            return

        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()

            # Validate frontmatter
            frontmatter = self._extract_frontmatter(content)
            if not frontmatter:
                result.add_warning(f"No frontmatter found in skills/{skill_name}.md")
            else:
                # Check required frontmatter fields
                required_fields = self.config['validation']['required_frontmatter']
                for field in required_fields:
                    if field not in frontmatter:
                        result.add_error(f"Missing required frontmatter field: {field}")
                    else:
                        result.add_info(f"Frontmatter field '{field}': {frontmatter[field]}")

        except Exception as e:
            result.add_error(f"Error reading skill definition: {str(e)}")

    def _extract_frontmatter(self, content: str) -> Dict[str, str]:
        """
        Extract YAML frontmatter from markdown

        Args:
            content: Markdown content

        Returns:
            Dictionary of frontmatter fields
        """
        # Match YAML frontmatter between --- delimiters
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return {}

        frontmatter_text = match.group(1)
        frontmatter = {}

        # Simple YAML parsing (key: value pairs)
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()

        return frontmatter

    def _validate_permissions(self, skill_path: Path, result: ValidationResult):
        """Validate file permissions"""
        executable_files = self.config['validation'].get('executable_files', [])

        for file_path in executable_files:
            full_path = skill_path / file_path
            if full_path.exists():
                if os.access(full_path, os.X_OK):
                    result.add_info(f"Executable: {file_path}")
                else:
                    result.add_warning(f"File not executable: {file_path} (run: chmod +x {file_path})")

    def _validate_commands(self, skill_path: Path, result: ValidationResult):
        """Validate slash commands"""
        commands_dir = skill_path / '.claude' / 'commands'

        if not commands_dir.exists():
            result.add_info("No slash commands directory (.claude/commands/)")
            return

        command_files = list(commands_dir.glob('*.md'))
        if not command_files:
            result.add_info("No slash commands found")
            return

        result.add_info(f"Found {len(command_files)} slash command(s)")

        for cmd_file in command_files:
            # Validate command has frontmatter
            try:
                with open(cmd_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                frontmatter = self._extract_frontmatter(content)
                if 'description' not in frontmatter:
                    result.add_warning(f"Command {cmd_file.name} missing 'description' in frontmatter")
                else:
                    result.add_info(f"Command {cmd_file.stem}: {frontmatter['description']}")

            except Exception as e:
                result.add_warning(f"Error reading command {cmd_file.name}: {str(e)}")


def validate_directory(skill_dir: str, skill_name: str = None, config_path: str = None) -> Dict[str, Any]:
    """
    Convenience function for skill validation

    Args:
        skill_dir: Path to skill directory
        skill_name: Optional skill name
        config_path: Optional config path

    Returns:
        Validation result dictionary
    """
    validator = SkillValidator(config_path)
    result = validator.validate_skill(skill_dir, skill_name)
    return result.to_dict()
