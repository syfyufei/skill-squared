---
name: skill-squared
description: A skill for managing and maintaining Claude Code skills - create projects, add commands, sync to marketplaces, and validate structure
---

# Skill-Squared

A meta-skill for developing and maintaining Claude Code skills. Provides tools for creating new skills, adding commands, syncing to marketplaces, and validating structure.

## Overview

Skill-Squared provides four core capabilities:

1. **Create**: Generate complete skill project structures with templates
2. **Command**: Add slash commands to existing skills
3. **Sync**: Synchronize skills from standalone repos to marketplaces
4. **Validate**: Check skill structure and configuration compliance

This skill follows the dual-repository pattern: skills are developed in standalone repositories and then synced to marketplace monorepos for distribution.

## When to Use This Skill

Trigger this skill when the user requests:

### Creating Skills
- "Create a new skill"
- "Generate a skill project"
- "Set up a new Claude Code skill"
- "I want to make a skill for [purpose]"

### Adding Commands
- "Add a command to my skill"
- "Create a slash command"
- "Add /command-name to [skill]"
- "I need a new command for [purpose]"

### Syncing Skills
- "Sync my skill to the marketplace"
- "Update the marketplace with my skill"
- "Copy skill to marketplace"
- "Publish skill changes"

### Validating Skills
- "Validate my skill"
- "Check if my skill is configured correctly"
- "Is my skill structure valid?"
- "Verify skill configuration"

## Tools

### create_skill

**Description**: Creates a complete new skill project structure with all necessary files and configuration.

**Python Handler**: `handlers.create_skill(payload)`

**Input Structure**:
```json
{
  "skill_name": "my-skill",
  "skill_description": "Brief description of what the skill does",
  "author_name": "Your Name",
  "author_email": "your.email@example.com",
  "github_user": "yourusername",
  "target_dir": "/path/to/create/skill",
  "version": "0.1.0"
}
```

**Behavior**:
1. Validates all inputs (skill_name must be kebab-case)
2. Creates skill directory structure
3. Renders templates with provided context
4. Creates .gitignore and LICENSE files
5. Makes install.sh executable
6. Returns list of all created files

**Output Structure**:
```json
{
  "success": true,
  "message": "Successfully created skill: my-skill",
  "data": {
    "skill_name": "my-skill",
    "skill_path": "/full/path/to/my-skill",
    "created_files": ["file1", "file2", "..."]
  }
}
```

**Error Cases**:
- Missing required fields
- Invalid skill_name format (must be kebab-case)
- Directory already exists
- Template not found

**Example Usage**:
```
User: "Create a new skill called data-analyzer that helps analyze datasets"
Assistant: [Gathers: author name, email, GitHub username]
Assistant: [Calls create_skill with payload]
Assistant: "Successfully created skill 'data-analyzer' at /path/to/data-analyzer!"
```

---

### add_command

**Description**: Adds a new slash command to an existing skill project.

**Python Handler**: `handlers.add_command(payload)`

**Input Structure**:
```json
{
  "skill_dir": "/path/to/skill",
  "command_name": "process-data",
  "command_description": "Process dataset and generate report",
  "command_instructions": "Optional detailed instructions"
}
```

**Behavior**:
1. Validates skill directory exists
2. Validates command_name format (kebab-case)
3. Checks command doesn't already exist
4. Creates .claude/commands/ directory if needed
5. Generates command file with YAML frontmatter
6. Updates plugin.json to register command
7. Returns command info

**Output Structure**:
```json
{
  "success": true,
  "message": "Successfully added command: process-data",
  "data": {
    "command_name": "process-data",
    "command_file": ".claude/commands/process-data.md",
    "description": "Process dataset and generate report"
  }
}
```

**Example Usage**:
```
User: "Add a command called process-data to my data-analyzer skill"
Assistant: [Gathers: skill directory]
Assistant: [Calls add_command with payload]
Assistant: "Successfully added command 'process-data'! Remember to reinstall the skill."
```

---

### sync_skill

**Description**: Synchronizes skill files from standalone repository to marketplace repository.

**Python Handler**: `handlers.sync_skill(payload)`

**Input Structure**:
```json
{
  "source_dir": "/path/to/standalone/skill",
  "target_dir": "/path/to/marketplace",
  "skill_name": "my-skill",
  "dry_run": false
}
```

**Behavior**:
1. Validates source and target directories exist
2. Identifies files to sync (skills/{skill_name}.md and .claude/commands/)
3. Creates backups of existing files (with timestamps)
4. Copies files from source to target
5. Returns list of copied files and backups

**Example Usage**:
```
User: "Sync my data-analyzer skill to adrian-marketplace"
Assistant: [Gathers: source dir, target dir]
Assistant: [Calls sync_skill]
Assistant: "Successfully synced! Don't forget to commit the marketplace changes."
```

---

### validate_skill

**Description**: Validates skill structure, configuration files, and compliance with best practices.

**Python Handler**: `handlers.validate_skill(payload)`

**Input Structure**:
```json
{
  "skill_dir": "/path/to/skill",
  "skill_name": "my-skill"
}
```

Note: `skill_name` is optional - will be auto-detected if not provided.

**Behavior**:
1. Auto-detects skill name if not provided
2. Checks for required files
3. Validates JSON syntax in configuration files
4. Validates YAML frontmatter in skill.md
5. Checks file permissions (install.sh executable)
6. Validates slash commands
7. Returns errors, warnings, and info messages

**Example Usage**:
```
User: "Validate my skill to make sure it's configured correctly"
Assistant: [Gathers: skill directory]
Assistant: [Calls validate_skill]
Assistant: [Presents results organized by ERRORS/WARNINGS/INFO]
Assistant: "Validation passed! Your skill is ready to use."
```

## Configuration

Skill-Squared uses `config/config.json` for configuration:

- **validation**: Rules for required files, frontmatter fields, executable files
- **sync**: Backup settings, files to sync patterns
- **templates**: Template directory locations, variable patterns
- **defaults**: Default values for author info, version, license

## Template System

Templates use simple variable substitution:
- `{{variable}}` - Variable substitution
- `{{#if variable}}...{{/if}}` - Conditional blocks

Available variables:
- `skill_name`, `skill_display_name`, `skill_description`
- `author_name`, `author_email`, `github_user`
- `repository_url`, `version`, `timestamp`

## Best Practices

### Skill Development Workflow

1. **Create** skill with `/skill-squared:create`
2. **Customize** skills/{skill-name}.md with your skill logic
3. **Add commands** with `/skill-squared:command`
4. **Validate** structure with `/skill-squared:validate`
5. **Test** installation locally: ./install.sh
6. **Sync** to marketplace with `/skill-squared:sync`

### Architecture Pattern

Skill-Squared follows the **Dual-Repository Pattern**:

1. **Standalone Skills**: Complete skill implementation, independent git repository
2. **Marketplace Monorepo**: Collection of skills, synced from standalone repos

---

*Skill-Squared v0.1.0 - A skill for developing skills*
