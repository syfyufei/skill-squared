---
description: Add slash command to existing skill
---

# Add Slash Command

Use the skill-squared skill to add a new slash command to an existing Claude Code skill.

## Gather Information

Ask the user for the following information if not already provided:

1. **Skill directory**:
   - Path to the existing skill project
   - Must contain .claude-plugin/ directory

2. **Command name** (kebab-case, e.g., "analyze-data"):
   - Must be lowercase with hyphens only
   - Will create .claude/commands/{command-name}.md

3. **Command description** (one-line):
   - Brief description that appears in /help
   - Example: "Analyze dataset and generate insights"

4. **Command instructions** (optional):
   - Detailed instructions for what the command should do
   - If not provided, a default template will be used

## Add the Command

Call the Python handler to add the command:

```python
from handlers import add_command

payload = {
    'skill_dir': '[user-provided skill directory]',
    'command_name': '[user-provided command name]',
    'command_description': '[user-provided description]',
    'command_instructions': '[user-provided instructions or empty]'
}

result = add_command(payload)
```

## Report Results

If successful (`result['success'] == True`):
- Confirm command creation
- Show the command file path
- Explain that plugin.json has been updated
- Suggest testing the command:
  1. Reinstall the skill: `cd [skill-dir] && ./install.sh`
  2. Verify with `/help`
  3. Test the command: `/[skill-name]:[command-name]`

If failed (`result['success'] == False`):
- Explain the error (e.g., skill directory not found, command already exists)
- Suggest corrections
- Ask if they want to try again

## Example Interaction

**User**: "Add a command to my skill"

**Assistant**: "I'll help you add a slash command. Let me gather some information."

[Asks for: skill directory, command name, description]

**User**:
- Skill directory: /path/to/my-skill
- Command name: process-data
- Description: Process dataset and generate report

**Assistant**: [Calls add_command handler]

**Assistant**: "Successfully added command 'process-data' to your skill!

Created: .claude/commands/process-data.md
Updated: .claude-plugin/plugin.json

To use the command:
1. Reinstall skill: cd /path/to/my-skill && ./install.sh
2. Verify: /help
3. Use: /my-skill:process-data

You can now customize .claude/commands/process-data.md to define the command's behavior."

## Important Notes

- Command names must be unique within the skill
- The command file uses YAML frontmatter with 'description' field
- Commands are automatically registered in plugin.json
- After adding commands, users must reinstall the skill for changes to take effect
