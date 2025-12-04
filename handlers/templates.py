"""
Template rendering engine for skill-squared
Handles variable substitution and conditional logic
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


class TemplateManager:
    """Manages template rendering with variable substitution"""

    def __init__(self, template_base_dir: str = None):
        """
        Initialize template manager

        Args:
            template_base_dir: Base directory for templates (default: project root/templates)
        """
        if template_base_dir:
            self.template_dir = Path(template_base_dir)
        else:
            # Default to templates/ in project root
            project_root = Path(__file__).parent.parent
            self.template_dir = project_root / 'templates'

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render a template with the given context

        Args:
            template_name: Name of template file (e.g., 'skill/skill.md.template')
            context: Dictionary of variables to substitute

        Returns:
            Rendered template string

        Raises:
            FileNotFoundError: If template doesn't exist
        """
        template_path = self.template_dir / template_name

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # Enrich context with auto-generated values
        enriched_context = self._enrich_context(context)

        # Perform variable substitution
        rendered = self._substitute_variables(template_content, enriched_context)

        # Process conditionals
        rendered = self._process_conditionals(rendered, enriched_context)

        return rendered

    def _enrich_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add auto-generated variables to context

        Args:
            context: Original context dictionary

        Returns:
            Enriched context with additional variables
        """
        enriched = context.copy()

        # Auto-generate display name from skill_name
        if 'skill_name' in context and 'skill_display_name' not in context:
            enriched['skill_display_name'] = self._to_display_name(context['skill_name'])

        # Auto-generate command display name
        if 'command_name' in context and 'command_display_name' not in context:
            enriched['command_display_name'] = self._to_display_name(context['command_name'])

        # Auto-generate repository URL
        if 'github_user' in context and 'skill_name' in context and 'repository_url' not in context:
            enriched['repository_url'] = f"https://github.com/{context['github_user']}/{context['skill_name']}"

        # Add timestamp
        if 'timestamp' not in context:
            enriched['timestamp'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

        # Add default version
        if 'version' not in context:
            enriched['version'] = '0.1.0'

        return enriched

    def _to_display_name(self, kebab_name: str) -> str:
        """
        Convert kebab-case to Title Case

        Args:
            kebab_name: Name in kebab-case (e.g., 'my-skill')

        Returns:
            Title case name (e.g., 'My Skill')
        """
        return ' '.join(word.capitalize() for word in kebab_name.split('-'))

    def _substitute_variables(self, template: str, context: Dict[str, Any]) -> str:
        """
        Substitute {{variable}} patterns with context values

        Args:
            template: Template string
            context: Variables dictionary

        Returns:
            Template with variables substituted
        """
        def replacer(match):
            var_name = match.group(1)
            return str(context.get(var_name, f'{{{{missing:{var_name}}}}}'))

        # Match {{variable_name}} pattern
        return re.sub(r'\{\{(\w+)\}\}', replacer, template)

    def _process_conditionals(self, template: str, context: Dict[str, Any]) -> str:
        """
        Process {{#if condition}}...{{/if}} conditionals

        Args:
            template: Template string
            context: Variables dictionary

        Returns:
            Template with conditionals processed
        """
        # Process {{#if variable}}...{{else}}...{{/if}}
        def if_else_replacer(match):
            var_name = match.group(1)
            if_content = match.group(2)
            else_content = match.group(3) if match.group(3) else ''

            # Check if variable exists and is truthy
            if context.get(var_name):
                return if_content
            else:
                return else_content

        # Match {{#if var}}content{{else}}else_content{{/if}}
        template = re.sub(
            r'\{\{#if\s+(\w+)\}\}(.*?)\{\{else\}\}(.*?)\{\{/if\}\}',
            if_else_replacer,
            template,
            flags=re.DOTALL
        )

        # Process {{#if variable}}...{{/if}} (without else)
        def if_replacer(match):
            var_name = match.group(1)
            if_content = match.group(2)

            # Check if variable exists and is truthy
            if context.get(var_name):
                return if_content
            else:
                return ''

        # Match {{#if var}}content{{/if}}
        template = re.sub(
            r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}',
            if_replacer,
            template,
            flags=re.DOTALL
        )

        return template

    def list_templates(self, category: str = None) -> list:
        """
        List available templates

        Args:
            category: Optional category filter ('skill' or 'command')

        Returns:
            List of template paths
        """
        if category:
            search_dir = self.template_dir / category
        else:
            search_dir = self.template_dir

        if not search_dir.exists():
            return []

        return [
            str(p.relative_to(self.template_dir))
            for p in search_dir.rglob('*.template')
        ]


# Convenience function for quick rendering
def render_template(template_name: str, context: Dict[str, Any], template_dir: str = None) -> str:
    """
    Quick template rendering function

    Args:
        template_name: Name of template file
        context: Variables dictionary
        template_dir: Optional custom template directory

    Returns:
        Rendered template string
    """
    manager = TemplateManager(template_dir)
    return manager.render(template_name, context)
