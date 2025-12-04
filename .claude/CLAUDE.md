# Skill-Squared - Project Context

## Project Overview

**Name**: skill-squared
**Description**: A meta-skill for managing and maintaining Claude Code skills
**Author**: Adrian
**Version**: 0.1.0
**Repository**: https://github.com/syfyufei/skill-squared

## What This Project Does

Skill-Squared is a Claude Code skill that helps developers create, manage, and maintain other Claude Code skills. It's a "skill for developing skills" - a meta-programming tool for the Claude Code ecosystem.

### Core Capabilities

1. **Create** (`/skill-squared:create`):
   - Generate complete skill project structures
   - Template-based file generation
   - Automatic configuration setup

2. **Command** (`/skill-squared:command`):
   - Add slash commands to existing skills
   - Update plugin.json automatically
   - Generate command files with frontmatter

3. **Sync** (`/skill-squared:sync`):
   - Synchronize skills to marketplace repositories
   - Backup files before overwriting
   - Support dry-run mode

4. **Validate** (`/skill-squared:validate`):
   - Check skill structure and configuration
   - Validate JSON and YAML syntax
   - Report errors, warnings, and info

## When to Use Skill-Squared

Trigger this skill when the user:
- Wants to create a new Claude Code skill
- Needs to add commands to an existing skill
- Wants to sync a skill to a marketplace
- Needs to validate skill structure
- Asks about skill development best practices

## Project Structure

```
skill-squared/
├── .claude-plugin/          # Plugin configuration
│   ├── marketplace.json     # Marketplace definition
│   └── plugin.json          # Plugin metadata
│
├── .claude/
│   ├── CLAUDE.md           # This file - project context
│   └── commands/           # 4 slash commands
│       ├── create.md
│       ├── command.md
│       ├── sync.md
│       └── validate.md
│
├── skills/
│   └── skill-squared.md    # Skill definition (source of truth)
│
├── handlers/               # Python implementation
│   ├── __init__.py        # Package exports
│   ├── handlers.py        # Core business logic (CRITICAL)
│   ├── templates.py       # Template rendering engine
│   ├── validators.py      # Validation logic
│   └── sync.py            # Sync operations
│
├── templates/              # File generation templates
│   ├── skill/             # Skill project templates
│   │   ├── skill.md.template
│   │   ├── marketplace.json.template
│   │   ├── plugin.json.template
│   │   ├── install.sh.template
│   │   ├── README.md.template
│   │   └── CLAUDE.md.template
│   └── command/
│       └── command.md.template
│
├── config/
│   └── config.json         # Validation rules, defaults
│
├── docs/                   # Documentation
│   ├── commands-reference.md
│   ├── template-guide.md
│   └── best-practices.md
│
├── install.sh              # Installation script
├── README.md               # English documentation
├── README.zh.md            # Chinese documentation
├── README.ja.md            # Japanese documentation
├── LICENSE                 # MIT License
└── .gitignore             # Git ignores
```

## Key Files

### Critical Files (Core Functionality)

1. **`skills/skill-squared.md`** - Skill definition
   - Teaches Claude when and how to use skill-squared
   - Documents all 4 tools with input/output structures
   - Contains usage examples and best practices

2. **`handlers/handlers.py`** - Main business logic (~500 lines)
   - `create_skill()` - Creates skill projects
   - `add_command()` - Adds commands to skills
   - `sync_skill()` - Syncs to marketplaces
   - `validate_skill()` - Validates structures

3. **`handlers/templates.py`** - Template rendering engine
   - Variable substitution (`{{variable}}`)
   - Conditional blocks (`{{#if}}...{{/if}}`)
   - Auto-generates display names, URLs, timestamps

4. **`handlers/validators.py`** - Validation logic
   - Checks required files
   - Validates JSON and YAML syntax
   - Checks file permissions
   - Returns errors, warnings, info

5. **`handlers/sync.py`** - Sync operations
   - Copies files from source to target
   - Creates timestamped backups
   - Supports dry-run mode
   - Reports all changes

### Configuration Files

1. **`.claude-plugin/marketplace.json`** - Marketplace definition
2. **`.claude-plugin/plugin.json`** - Plugin metadata
3. **`config/config.json`** - Validation rules and defaults

### Command Files

All in `.claude/commands/`:
- `create.md` - Create skill project
- `command.md` - Add command to skill
- `sync.md` - Sync to marketplace
- `validate.md` - Validate structure

## Architecture Pattern

### Dual-Repository Pattern

Skill-Squared promotes the dual-repository pattern:

1. **Standalone Repository** (e.g., `/path/to/my-skill/`):
   - Complete skill implementation
   - Independent development
   - Self-contained installation
   - Source of truth

2. **Marketplace Repository** (e.g., `/path/to/adrian-marketplace/`):
   - Aggregates multiple skills
   - Synced from standalone repos
   - User installation point
   - Distribution mechanism

### Why This Pattern?

- **Modularity**: Skills develop independently
- **Flexibility**: Install standalone OR from marketplace
- **Maintainability**: Each skill has own version control
- **Distribution**: One-stop shopping for users

## Development Guidelines

### Adding New Features

When adding features to skill-squared itself:

1. **Update skill definition** (`skills/skill-squared.md`):
   - Add tool documentation
   - Update "When to Use" section
   - Add usage examples

2. **Implement Python handler** (`handlers/handlers.py`):
   - Follow consistent return format
   - Include comprehensive error handling
   - Add docstrings

3. **Create slash command** (`.claude/commands/`):
   - YAML frontmatter with description
   - Gather information section
   - Processing instructions
   - Output format

4. **Update documentation**:
   - Add to commands reference
   - Update README if major feature
   - Update best practices if applicable

5. **Update plugin.json**:
   - Add command to commands array
   - Update version if needed

### Testing New Features

1. **Unit test** Python handlers:
   ```python
   from handlers import create_skill

   payload = {...}
   result = create_skill(payload)
   assert result['success'] == True
   ```

2. **Integration test** via slash commands:
   ```bash
   ./install.sh
   /help  # Verify command appears
   /skill-squared:command-name  # Test functionality
   ```

3. **End-to-end test** complete workflow:
   - Create test skill
   - Add commands
   - Validate
   - Sync to test marketplace
   - Install from marketplace

### Code Style

- **Python**: Follow PEP 8
- **Markdown**: GitHub Flavored Markdown
- **JSON**: 2-space indentation
- **Bash**: Use `set -e` for safety

## Self-Management Capability

Skill-Squared can manage itself! Examples:

### Add New Command to Skill-Squared

```
User: "Add a new command called 'init' to skill-squared"
Claude: [Uses skill-squared to add command to itself]
```

### Validate Skill-Squared

```
User: "Validate skill-squared structure"
Claude: [Uses skill-squared to validate itself]
```

### Sync Skill-Squared to Marketplace

```
User: "Sync skill-squared to adrian-marketplace"
Claude: [Uses skill-squared to sync itself]
```

## Maintenance Tasks

### Regular Updates

- Update dependencies
- Test with latest Claude Code version
- Improve templates based on feedback
- Enhance documentation

### Version Management

- Follow semantic versioning
- Update version in:
  - `.claude-plugin/plugin.json`
  - `README.md`
  - Git tags

### Issue Tracking

- Monitor GitHub issues
- Respond to user feedback
- Fix bugs promptly
- Implement feature requests

## Common Workflows

### Create New Skill

```
/skill-squared:create
→ Generates complete project
→ User customizes skills/{name}.md
→ User adds commands
→ User validates and tests
```

### Add Command to Existing Skill

```
/skill-squared:command
→ Adds .claude/commands/{name}.md
→ Updates plugin.json
→ User reinstalls skill
→ User tests command
```

### Sync to Marketplace

```
/skill-squared:sync
→ Copies skill.md and commands
→ Creates backups
→ User commits marketplace changes
→ Users can install from marketplace
```

### Validate Before Release

```
/skill-squared:validate
→ Checks all required files
→ Validates configuration
→ Reports errors/warnings
→ User fixes issues before release
```

## Template System

Templates in `templates/` use:
- `{{variable}}` - Variable substitution
- `{{#if var}}...{{/if}}` - Conditionals
- Auto-generated variables (URLs, timestamps, display names)

Customize templates to match project style.

## Configuration

`config/config.json` contains:
- **validation**: Required files, frontmatter fields
- **sync**: Backup settings, files to sync
- **templates**: Paths and variable patterns
- **defaults**: Default values for new skills

## Development Status

**Current Version**: 0.1.0

**Completed**:
- ✅ 4 core commands (create, command, sync, validate)
- ✅ Python handlers with template system
- ✅ Comprehensive validation
- ✅ Sync with backup support
- ✅ Multi-language documentation (EN, ZH, JA)

**Future Enhancements**:
- Testing framework
- Interactive mode for creation
- Template marketplace
- Skill analytics
- Version management helpers

## Important Notes

- Skill-Squared is self-hosting: it can manage and modify itself
- Always validate before syncing to marketplace
- Test locally before distributing
- Keep standalone and marketplace repos in sync
- Follow semantic versioning
- Document all changes in CHANGELOG

---

*This file helps Claude understand the skill-squared project and how to work with it effectively.*
