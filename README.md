# Skill-Squared

A meta-skill for managing and maintaining Claude Code skills - create projects, add commands, sync to marketplaces, and validate structure.

## Installation

In Claude Code, register the marketplace first:

```bash
/plugin marketplace add syfyufei/skill-squared
```

Then install the plugin from this marketplace:

```bash
/plugin install skill-squared@skill-squared-marketplace
```

### Verify Installation

Check that commands appear:

```bash
/help
```

```
# Should see 4 commands:
# /skill-squared:create - Create new skill project structure
# /skill-squared:command - Add slash command to existing skill
# /skill-squared:sync - Sync skill from standalone to marketplace
# /skill-squared:validate - Validate skill structure and configuration
```

## Usage

### Create New Skill

Create a complete skill project with all necessary files:

```bash
/skill-squared:create
```

Or use natural language:
```
"Create a new skill called data-analyzer"
```

**What it creates**:
- `.claude-plugin/` - Plugin configuration
- `skills/` - Skill definition
- `.claude/commands/` - Slash commands directory
- `handlers/`, `templates/`, `config/`, `docs/` - Supporting directories
- `install.sh`, `README.md`, `LICENSE`, `.gitignore`

### Add Command to Skill

Add a new slash command to an existing skill:

```bash
/skill-squared:command
```

Or use natural language:
```
"Add a command called process-data to my skill"
```

**What it does**:
- Creates `.claude/commands/{command-name}.md`
- Updates `plugin.json` to register the command
- Uses YAML frontmatter for command description

### Sync to Marketplace

Sync your skill from standalone repo to marketplace:

```bash
/skill-squared:sync
```

Or use natural language:
```
"Sync my data-analyzer skill to adrian-marketplace"
```

**What it syncs**:
- `skills/{skill-name}.md` - Skill definition
- `.claude/commands/` - All slash commands
- Creates backups before overwriting
- Supports dry-run mode

### Validate Skill

Validate skill structure and configuration:

```bash
/skill-squared:validate
```

Or use natural language:
```
"Validate my skill structure"
```

**What it checks**:
- Required files exist
- JSON syntax in configuration files
- YAML frontmatter in skill definition
- File permissions (install.sh executable)
- Command file structure

## Features

- **Complete Project Generation**: Creates fully-configured skill projects with templates
- **Command Management**: Easy slash command creation and registration
- **Marketplace Sync**: Synchronize skills to marketplace repositories
- **Validation**: Comprehensive structure and configuration validation
- **Template System**: Customizable templates with variable substitution
- **Dual-Repository Pattern**: Standalone development + marketplace distribution

## Architecture

Skill-Squared follows the **Dual-Repository Pattern**:

### Standalone Repository (Development)
- Full skill implementation
- Independent version control
- Self-contained installation
- Development and testing

### Marketplace Repository (Distribution)
- Aggregates multiple skills
- Copies skill.md and commands only
- One-stop installation for users
- Synced from standalone repos

## Workflow

1. **Create** skill: `/skill-squared:create`
2. **Customize** `skills/{skill-name}.md` with your skill logic
3. **Add commands**: `/skill-squared:command`
4. **Validate** structure: `/skill-squared:validate`
5. **Test** installation: `cd skill-name && ./install.sh`
6. **Sync** to marketplace: `/skill-squared:sync`
7. **Commit** and push both repositories

## Documentation

- **[Commands Reference](./docs/commands-reference.md)** - Complete command documentation
- **[Template Guide](./docs/template-guide.md)** - Template customization
- **[Best Practices](./docs/best-practices.md)** - Skill development guidelines

## Examples

### Creating a Data Analysis Skill

```
User: "Create a new skill called data-analyzer that helps analyze datasets"
Claude: [Gathers information and creates skill]
User: "Add a command called process to analyze data"
Claude: [Adds command to data-analyzer]
User: "Validate the skill"
Claude: [Validates structure - all checks pass]
User: "Test installation"
User: cd data-analyzer && ./install.sh
```

### Syncing to Marketplace

```
User: "Sync data-analyzer to adrian-marketplace"
Claude: [Syncs skill definition and commands]
Claude: "Successfully synced 4 files. Remember to commit the marketplace!"
User: cd ../adrian-marketplace && git add . && git commit -m "Update data-analyzer"
```

## Configuration

Skill-Squared uses `config/config.json` for:
- Validation rules (required files, frontmatter fields)
- Sync settings (backup, files to sync)
- Template paths and variables
- Default values

## Template System

Templates support:
- `{{variable}}` - Variable substitution
- `{{#if variable}}...{{/if}}` - Conditional blocks
- Auto-generated variables (repository_url, timestamp, display_name)

Available templates:
- `templates/skill/skill.md.template` - Skill definition
- `templates/skill/marketplace.json.template` - Marketplace config
- `templates/skill/plugin.json.template` - Plugin metadata
- `templates/skill/install.sh.template` - Installation script
- `templates/skill/README.md.template` - Documentation
- `templates/skill/CLAUDE.md.template` - Project context
- `templates/command/command.md.template` - Slash command

## Python Handlers

Skill-Squared uses Python for deterministic file operations:
- `handlers/handlers.py` - Core business logic (create, add_command, sync, validate)
- `handlers/templates.py` - Template rendering engine
- `handlers/validators.py` - Validation logic
- `handlers/sync.py` - Sync operations

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - see [LICENSE](./LICENSE) for details

---

**Version**: 0.1.0
**Author**: Adrian <syfyufei@gmail.com>
**Repository**: https://github.com/syfyufei/skill-squared

*A skill for developing skills*
