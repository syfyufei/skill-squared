---
description: Sync skill from standalone to marketplace
---

# Sync Skill to Marketplace

Use the skill-squared skill to synchronize a skill from its standalone repository to a marketplace repository (following the dual-repository pattern).

## Gather Information

Ask the user for the following information if not already provided:

1. **Source directory** (standalone skill repository):
   - Path to the standalone skill project
   - Example: /path/to/my-skill

2. **Target directory** (marketplace repository):
   - Path to the marketplace repository
   - Example: /path/to/my-marketplace

3. **Skill name**:
   - Name of the skill to sync
   - Must match the skill's directory/file naming

4. **Dry run** (optional, default: false):
   - If true, show what would be synced without actually copying
   - Useful for previewing changes

## Explain What Will Be Synced

Before syncing, explain to the user that the following will be copied:
- `skills/{skill_name}.md` - The skill definition file
- `.claude/commands/` - All slash command files

The sync operation will:
- Create backups of existing files (with timestamp)
- Copy files from source to target
- Preserve file permissions
- Report all changes made

## Perform the Sync

Call the Python handler to sync the skill:

```python
from handlers import sync_skill

payload = {
    'source_dir': '[user-provided source directory]',
    'target_dir': '[user-provided target directory]',
    'skill_name': '[user-provided skill name]',
    'dry_run': [user-provided or False]
}

result = sync_skill(payload)
```

## Report Results

If successful (`result['success'] == True`):
- Show number of files synced
- List all copied files
- List any backup files created
- Remind user to:
  1. Commit changes to the marketplace repository
  2. Push to GitHub if applicable
  3. Test marketplace installation

If dry run mode:
- Clearly indicate this was a preview
- Show what would be synced
- Ask if they want to proceed with actual sync

If failed (`result['success'] == False`):
- Explain the error (e.g., directory not found)
- Show any partial results
- Suggest corrections

## Example Interaction

**User**: "Sync my skill to the marketplace"

**Assistant**: "I'll help you sync your skill. Let me gather some information."

[Asks for: source directory, target directory, skill name]

**User**:
- Source: /Users/me/skills/my-skill
- Target: /Users/me/adrian-marketplace
- Skill: my-skill

**Assistant**: [Calls sync_skill handler]

**Assistant**: "Successfully synced my-skill to marketplace!

Synced 6 files:
- skills/my-skill.md
- .claude/commands/process.md
- .claude/commands/analyze.md
- .claude/commands/export.md
- .claude/commands/validate.md
- .claude/commands/help.md

Backups created:
- skills/my-skill.md.backup.20250304_143022
- .claude/commands/process.md.backup.20250304_143022

Next steps:
1. cd /Users/me/adrian-marketplace
2. git add skills/my-skill.md .claude/commands/
3. git commit -m 'Update my-skill'
4. git push

Your marketplace is now up to date!"

## Safety Features

- **Backup enabled**: Existing files are backed up before overwriting
- **Dry run mode**: Preview changes without modifying files
- **Error recovery**: Partial syncs are reported with details
- **Timestamp backups**: Each backup has a unique timestamp

## Important Notes

- Only syncs skill definition and commands (not entire repository)
- Backups are created in the same directory with `.backup.{timestamp}` suffix
- Users should commit and push marketplace changes after syncing
- Dry run mode is recommended for first-time sync to preview changes
