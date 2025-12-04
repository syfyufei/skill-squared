---
description: Create new skill project structure
---

# Create New Skill

Use the skill-squared skill to create a complete new Claude Code skill project.

## Gather Information

Ask the user for the following information if not already provided:

1. **Skill name** (kebab-case, e.g., "my-awesome-skill"):
   - Must be lowercase with hyphens only
   - Will be used for directory name and file names

2. **Skill description** (one-line description):
   - Clear, concise description of what the skill does
   - Will appear in marketplace listings

3. **Author name**:
   - Your full name

4. **Author email**:
   - Your email address

5. **GitHub username**:
   - Your GitHub username (for repository URL generation)

6. **Target directory** (optional, default: current directory):
   - Where to create the skill project directory

## Create the Skill

Call the Python handler to create the skill:

```python
from handlers import create_skill

payload = {
    'skill_name': '[user-provided skill name]',
    'skill_description': '[user-provided description]',
    'author_name': '[user-provided name]',
    'author_email': '[user-provided email]',
    'github_user': '[user-provided GitHub username]',
    'target_dir': '[user-provided or current directory]'
}

result = create_skill(payload)
```

## Report Results

If successful (`result['success'] == True`):
- Confirm skill creation
- List all created files
- Show the skill directory path
- Provide next steps:
  1. Navigate to the skill directory
  2. Customize the skill definition in `skills/{skill_name}.md`
  3. Add slash commands if needed
  4. Test installation with `./install.sh`
  5. Initialize git repository if desired

If failed (`result['success'] == False`):
- Explain the error
- Suggest corrections
- Ask if they want to try again

## Example Interaction

**User**: "Create a new skill"

**Assistant**: "I'll help you create a new skill. Let me gather some information."

[Asks for: skill name, description, author info, GitHub username]

**Assistant**: [Calls create_skill handler]

**Assistant**: "Successfully created skill 'my-awesome-skill' at /path/to/my-awesome-skill

Created files:
- .claude-plugin/marketplace.json
- .claude-plugin/plugin.json
- skills/my-awesome-skill.md
- install.sh (executable)
- README.md
- .claude/CLAUDE.md
- .gitignore
- LICENSE

Next steps:
1. cd /path/to/my-awesome-skill
2. Customize skills/my-awesome-skill.md with your skill logic
3. Add slash commands with /skill-squared:command
4. Test installation: ./install.sh"
