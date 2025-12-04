---
description: Validate skill structure and configuration
---

# Validate Skill

Use the skill-squared skill to validate a Claude Code skill's structure, configuration, and compliance with best practices.

## Gather Information

Ask the user for the following information if not already provided:

1. **Skill directory**:
   - Path to the skill project to validate
   - Example: /path/to/my-skill

2. **Skill name** (optional):
   - If not provided, will be auto-detected from plugin.json or directory name
   - Useful for explicit validation

## Perform Validation

Call the Python handler to validate the skill:

```python
from handlers import validate_skill

payload = {
    'skill_dir': '[user-provided skill directory]',
    'skill_name': '[user-provided or None for auto-detect]'
}

result = validate_skill(payload)
```

## Report Results

The validation checks for:

### Errors (Must Fix)
- Missing required files
- Invalid JSON syntax in configuration files
- Missing required frontmatter fields
- Structural issues

### Warnings (Should Fix)
- Non-executable install.sh
- Missing command descriptions
- Incomplete documentation

### Info (Good to Know)
- Files found and validated
- Detected skill name
- Command count
- Frontmatter values

## Present Results Clearly

Organize the output by category:

**ERRORS** (Red/Critical):
- List each error with clear description
- Provide fix suggestions
- Example: "Required file missing: .claude-plugin/marketplace.json"

**WARNINGS** (Yellow/Advisory):
- List each warning
- Explain why it matters
- Provide fix command if applicable
- Example: "File not executable: install.sh (run: chmod +x install.sh)"

**INFO** (Green/Success):
- List positive findings
- Show detected values
- Example: "Found: skills/my-skill.md"

**SUMMARY**:
- Overall result: PASSED or FAILED
- Count of errors, warnings, info
- Next steps based on results

## Example Interaction

**User**: "Validate my skill"

**Assistant**: "I'll validate your skill structure. What's the skill directory?"

**User**: "/Users/me/skills/my-awesome-skill"

**Assistant**: [Calls validate_skill handler]

**Assistant**: "Validation Results for my-awesome-skill

INFO:
✓ Validating skill at: /Users/me/skills/my-awesome-skill
✓ Detected skill name: my-awesome-skill
✓ Found: .claude-plugin/marketplace.json
✓ Found: .claude-plugin/plugin.json
✓ Found: skills/my-awesome-skill.md
✓ Found: install.sh
✓ Found: README.md
✓ Valid JSON: .claude-plugin/marketplace.json
✓ Valid JSON: .claude-plugin/plugin.json
✓ Frontmatter field 'name': my-awesome-skill
✓ Frontmatter field 'description': An awesome skill for Claude Code
✓ Executable: install.sh
✓ Found 4 slash command(s)
✓ Command process: Process data and generate insights
✓ Command analyze: Analyze results
✓ Command export: Export to various formats
✓ Command help: Show usage help

WARNINGS:
⚠ No warnings

ERRORS:
✗ No errors

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESULT: ✅ VALIDATION PASSED

Your skill structure is valid and ready to use!

Next steps:
1. Test installation: cd /Users/me/skills/my-awesome-skill && ./install.sh
2. Verify commands: /help
3. Test functionality with natural language or slash commands"

## Example with Errors

**Assistant**: "Validation Results for broken-skill

INFO:
✓ Validating skill at: /Users/me/skills/broken-skill
✓ Detected skill name: broken-skill

ERRORS:
✗ Required file missing: .claude-plugin/marketplace.json
✗ Required file missing: skills/broken-skill.md
✗ Invalid JSON in .claude-plugin/plugin.json: Expecting ',' delimiter: line 8 column 3 (char 145)

WARNINGS:
⚠ File not executable: install.sh (run: chmod +x install.sh)
⚠ No slash commands directory (.claude/commands/)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESULT: ❌ VALIDATION FAILED (3 errors, 2 warnings)

Please fix the errors above before using this skill.

Suggested fixes:
1. Create .claude-plugin/marketplace.json (use /skill-squared:create for template)
2. Create skills/broken-skill.md with proper frontmatter
3. Fix JSON syntax in .claude-plugin/plugin.json
4. Make install.sh executable: chmod +x install.sh
5. Add slash commands if needed: /skill-squared:command"

## What Validation Checks

1. **Required Files**:
   - .claude-plugin/marketplace.json
   - .claude-plugin/plugin.json
   - skills/{skill_name}.md
   - install.sh
   - README.md

2. **JSON Syntax**:
   - Valid JSON in marketplace.json
   - Valid JSON in plugin.json

3. **Skill Definition**:
   - YAML frontmatter present
   - Required fields: name, description

4. **Permissions**:
   - install.sh is executable

5. **Commands**:
   - Command files have 'description' in frontmatter
   - Command count

## Important Notes

- Validation is non-destructive (read-only)
- Auto-detects skill name if not provided
- Suggests specific fixes for each error
- Helps ensure compatibility with Claude Code plugin system
