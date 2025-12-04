# Commands Reference

Complete reference for all Skill-Squared commands.

## Overview

Skill-Squared provides 4 slash commands for skill management:

1. `/skill-squared:create` - Create new skill project
2. `/skill-squared:command` - Add command to existing skill
3. `/skill-squared:sync` - Sync skill to marketplace
4. `/skill-squared:validate` - Validate skill structure

All commands can also be triggered via natural language.

---

## `/skill-squared:create`

**Description**: Create new skill project structure

**What it does**:
- Creates complete skill project directory
- Generates all configuration files
- Renders templates with your information
- Makes install.sh executable

**Prompts for**:
- Skill name (kebab-case, e.g., "data-analyzer")
- Skill description (one-line)
- Author name
- Author email
- GitHub username
- Target directory (optional, defaults to current directory)

**Creates**:
- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json`
- `skills/{skill-name}.md`
- `install.sh` (executable)
- `README.md`
- `.claude/CLAUDE.md`
- `.gitignore`
- `LICENSE`

**Example**:
```
/skill-squared:create

Skill name: data-analyzer
Description: Analyze datasets and generate insights
Author: John Doe
Email: john@example.com
GitHub: johndoe
Target: /Users/john/skills

✓ Created skill 'data-analyzer' at /Users/john/skills/data-analyzer
```

**Natural language**:
- "Create a new skill"
- "Generate a skill project called [name]"
- "Set up a new Claude Code skill"

---

## `/skill-squared:command`

**Description**: Add slash command to existing skill

**What it does**:
- Creates command file in `.claude/commands/`
- Adds YAML frontmatter with description
- Updates `plugin.json` to register command
- Provides next steps for testing

**Prompts for**:
- Skill directory (path to existing skill)
- Command name (kebab-case, e.g., "process-data")
- Command description (appears in /help)
- Command instructions (optional, detailed behavior)

**Creates**:
- `.claude/commands/{command-name}.md`
- Updates `.claude-plugin/plugin.json`

**Example**:
```
/skill-squared:command

Skill directory: /Users/john/skills/data-analyzer
Command name: process-data
Description: Process dataset and generate report
Instructions: [Enter detailed instructions]

✓ Added command 'process-data'
→ Reinstall skill to use: cd data-analyzer && ./install.sh
```

**Natural language**:
- "Add a command to my skill"
- "Create a slash command called [name]"
- "Add /command-name to [skill]"

---

## `/skill-squared:sync`

**Description**: Sync skill from standalone to marketplace

**What it does**:
- Copies skill definition and commands to marketplace
- Creates timestamped backups before overwriting
- Supports dry-run mode for preview
- Reports all synced files

**Prompts for**:
- Source directory (standalone skill repo)
- Target directory (marketplace repo)
- Skill name
- Dry run (optional, true/false)

**Syncs**:
- `skills/{skill-name}.md`
- `.claude/commands/` (all command files)

**Example**:
```
/skill-squared:sync

Source: /Users/john/skills/data-analyzer
Target: /Users/john/adrian-marketplace
Skill name: data-analyzer
Dry run: false

✓ Synced 4 files
  - skills/data-analyzer.md
  - .claude/commands/process.md
  - .claude/commands/analyze.md
  - .claude/commands/export.md

Backups created:
  - skills/data-analyzer.md.backup.20250304_143000

→ Remember to commit marketplace changes!
```

**Dry run mode**:
Set `dry_run: true` to preview changes without actually copying files.

**Natural language**:
- "Sync my skill to the marketplace"
- "Update marketplace with [skill]"
- "Publish skill changes"

---

## `/skill-squared:validate`

**Description**: Validate skill structure and configuration

**What it does**:
- Checks for required files
- Validates JSON syntax in config files
- Validates YAML frontmatter
- Checks file permissions
- Validates command structure
- Reports errors, warnings, and info

**Prompts for**:
- Skill directory
- Skill name (optional, auto-detected)

**Validates**:
- Required files exist
- JSON syntax (marketplace.json, plugin.json)
- Frontmatter fields (name, description)
- File permissions (install.sh executable)
- Command descriptions

**Example**:
```
/skill-squared:validate

Skill directory: /Users/john/skills/data-analyzer

INFO:
✓ Found: .claude-plugin/marketplace.json
✓ Found: .claude-plugin/plugin.json
✓ Found: skills/data-analyzer.md
✓ Valid JSON: marketplace.json
✓ Frontmatter field 'name': data-analyzer
✓ Executable: install.sh
✓ Found 3 commands

WARNINGS:
⚠ None

ERRORS:
✗ None

RESULT: ✅ VALIDATION PASSED
```

**Error example**:
```
ERRORS:
✗ Required file missing: .claude-plugin/marketplace.json
✗ Invalid JSON in plugin.json: line 8 column 3
✗ Missing frontmatter field: description

RESULT: ❌ VALIDATION FAILED (3 errors)
```

**Natural language**:
- "Validate my skill"
- "Check if my skill is configured correctly"
- "Verify skill structure"

---

## Command Comparison

| Command | Purpose | Creates Files | Updates Files | Read-Only |
|---------|---------|---------------|---------------|-----------|
| `create` | Initialize skill | Yes (12+) | No | No |
| `command` | Add slash command | Yes (1) | Yes (plugin.json) | No |
| `sync` | Copy to marketplace | Yes (copies) | Yes (overwrites) | No |
| `validate` | Check structure | No | No | Yes |

---

## Tips & Best Practices

### Daily Workflow

1. **Create**: Start with `/skill-squared:create`
2. **Customize**: Edit `skills/{skill-name}.md`
3. **Add commands**: Use `/skill-squared:command` as needed
4. **Validate**: Run `/skill-squared:validate` before syncing
5. **Sync**: Use `/skill-squared:sync` to publish

### Validation Before Sync

Always validate before syncing to marketplace:

```
/skill-squared:validate
# Fix any errors
/skill-squared:sync
```

### Dry Run First

Preview sync changes with dry run:

```
/skill-squared:sync
# When prompted: dry_run = true
# Review changes
# Run again with dry_run = false
```

### Testing Locally

Test skills before syncing:

```bash
cd /path/to/skill
./install.sh
/help  # Verify commands appear
# Test with natural language or slash commands
```

---

## See Also

- [Template Guide](./template-guide.md) - Customize templates
- [Best Practices](./best-practices.md) - Skill development guidelines
- [Main README](../README.md) - Overview and installation
