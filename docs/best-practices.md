# Best Practices

Guidelines for developing high-quality Claude Code skills with Skill-Squared.

## Skill Development Workflow

### 1. Planning Phase

Before creating a skill:
- Define clear purpose and scope
- Identify trigger phrases users will use
- Plan slash commands needed
- Consider whether Python handlers are needed

### 2. Creation Phase

```bash
/skill-squared:create
```

- Use descriptive kebab-case names
- Write clear one-line descriptions
- Include accurate author information

### 3. Implementation Phase

Customize `skills/{skill-name}.md`:
- Define clear "When to Use" triggers
- Document all tools thoroughly
- Include usage examples
- Specify input/output structures

Add commands as needed:
```bash
/skill-squared:command
```

### 4. Validation Phase

Before testing:
```bash
/skill-squared:validate
```

Fix all errors and warnings.

### 5. Testing Phase

Test locally:
```bash
cd /path/to/skill
./install.sh
```

Test with:
- Natural language triggers
- Slash commands
- Edge cases

### 6. Distribution Phase

Sync to marketplace:
```bash
/skill-squared:sync
```

Commit both repositories:
```bash
# Standalone repo
cd /path/to/skill
git add .
git commit -m "Release v0.1.0"
git push

# Marketplace repo
cd /path/to/marketplace
git add skills/{skill-name}.md .claude/commands/
git commit -m "Add {skill-name} v0.1.0"
git push
```

## Naming Conventions

### Skill Names

**Good**:
- `data-analyzer` - Descriptive, specific
- `pdf-parser` - Clear purpose
- `code-reviewer` - Action-oriented

**Avoid**:
- `helper` - Too generic
- `MySkill` - Not kebab-case
- `data_analyzer` - Use hyphens not underscores

### Command Names

**Good**:
- `process-data` - Verb + noun
- `generate-report` - Clear action
- `validate-schema` - Specific task

**Avoid**:
- `data` - Missing verb
- `process` - Too generic
- `processData` - Not kebab-case

### File Names

Follow the standard structure:
- Skill definition: `skills/{skill-name}.md`
- Commands: `.claude/commands/{command-name}.md`
- Config: `.claude-plugin/marketplace.json`, `plugin.json`

## Skill Definition Best Practices

### Frontmatter

Always include required fields:

```yaml
---
name: skill-name
description: Clear one-line description
---
```

### Structure

Organize skill.md with these sections:

1. **Overview**: Brief introduction
2. **When to Use**: Clear trigger scenarios
3. **Tools**: Detailed tool documentation
4. **Configuration**: Optional settings
5. **Best Practices**: Usage guidelines

### Tool Documentation

For each tool, document:

1. **Description**: What it does
2. **Input Structure**: JSON schema
3. **Behavior**: Step-by-step process
4. **Output Structure**: Return format
5. **Example Usage**: Real-world example

Example:
```markdown
### create_skill

**Description**: Creates a complete new skill project structure.

**Input Structure**:
\`\`\`json
{
  "skill_name": "my-skill",
  "skill_description": "Brief description"
}
\`\`\`

**Behavior**:
1. Validates inputs
2. Creates directory structure
3. Renders templates
4. Returns created files

**Output Structure**:
\`\`\`json
{
  "success": true,
  "message": "Successfully created skill",
  "data": {...}
}
\`\`\`

**Example Usage**:
\`\`\`
User: "Create a new skill called data-analyzer"
Assistant: [Gathers info and calls create_skill]
\`\`\`
```

## Command Best Practices

### Command Structure

Each command file should have:

1. **YAML Frontmatter**: Description field
2. **Title**: Clear command name
3. **Purpose**: What it does
4. **Gather Information**: What to ask user
5. **Processing**: How to handle request
6. **Output**: What to return

### Example Command

```markdown
---
description: Process dataset and generate report
---

# Process Data

Use this skill to process datasets.

## Gather Information

Ask the user for:
1. Dataset path
2. Output format (CSV, JSON, Excel)
3. Processing options

## Processing

1. Load dataset
2. Apply transformations
3. Generate report
4. Save to specified format

## Output

Provide:
- Success confirmation
- Output file path
- Summary statistics
```

### Error Handling

Include error handling in commands:

```markdown
## Error Cases

- File not found → Ask for correct path
- Invalid format → List supported formats
- Processing failed → Show error details and suggest fixes
```

## Python Handlers Best Practices

### When to Use Python

Use Python handlers when:
- File operations required (create, copy, validate)
- Complex logic needed (parsing, validation)
- Deterministic behavior required
- Template rendering needed

### Handler Structure

Follow the pattern:

```python
def handler_name(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Description

    Args:
        payload: Input parameters

    Returns:
        Result dictionary with success, message, data
    """
    try:
        # Validate inputs
        # Process request
        # Return success
        return {
            'success': True,
            'message': '...',
            'data': {...}
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
```

### Return Format

Always return consistent structure:

**Success**:
```python
{
    "success": True,
    "message": "Operation completed",
    "data": {...}
}
```

**Error**:
```python
{
    "success": False,
    "error": "Error description"
}
```

## Repository Management

### Dual-Repository Pattern

Maintain two repositories:

**Standalone Repository** (`/path/to/skill-name/`):
- Full implementation
- Independent versioning
- Development branch for features
- Main branch for releases

**Marketplace Repository** (`/path/to/marketplace/`):
- Skills directory with synced skills
- Commands directory with synced commands
- Clean history (no development commits)

### Versioning

Follow semantic versioning:
- `0.1.0` - Initial release
- `0.2.0` - New features (minor)
- `0.2.1` - Bug fixes (patch)
- `1.0.0` - Stable release (major)

Update version in:
- `.claude-plugin/plugin.json`
- `README.md`
- Git tags

### Git Workflow

```bash
# Standalone repo
git checkout -b feature/new-command
# Develop feature
git commit -m "Add new-command"
git checkout main
git merge feature/new-command
git tag v0.2.0
git push && git push --tags

# Sync to marketplace
/skill-squared:sync

# Marketplace repo
cd /path/to/marketplace
git add skills/ .claude/commands/
git commit -m "Update skill-name to v0.2.0"
git push
```

## Documentation Best Practices

### README Structure

Include in README.md:
1. **Title and Description**
2. **Installation** (following superpowers pattern)
3. **Usage** (commands and natural language)
4. **Features** (bullet points)
5. **Examples** (real-world scenarios)
6. **Documentation Links**
7. **License**

### Code Comments

Comment sparingly:
- Explain WHY not WHAT
- Document complex logic
- Provide examples for unclear code

### Inline Documentation

Use clear naming to reduce need for comments:

```python
# Good
def validate_kebab_case_name(name: str) -> bool:
    return all(c.islower() or c.isdigit() or c == '-' for c in name)

# Avoid
def validate(n: str) -> bool:  # Check if name is valid
    return all(c.islower() or c.isdigit() or c == '-' for c in n)
```

## Testing Best Practices

### Local Testing

Test before syncing:

```bash
# Create test skill
/skill-squared:create
# Name: test-skill

# Validate
/skill-squared:validate test-skill/

# Install locally
cd test-skill && ./install.sh

# Test commands
/help  # Verify commands appear
/test-skill:command-name  # Test each command

# Clean up
cd .. && rm -rf test-skill/
```

### Integration Testing

Test the complete workflow:

1. Create skill
2. Add multiple commands
3. Validate
4. Sync to test marketplace
5. Install from marketplace
6. Test all features

### Edge Cases

Test error conditions:
- Invalid inputs (wrong format, missing files)
- Boundary conditions (empty strings, very long names)
- System errors (permission denied, disk full)

## Performance Best Practices

### Template Rendering

- Cache template manager instances
- Minimize template complexity
- Use conditionals sparingly

### File Operations

- Batch file operations when possible
- Use dry-run mode for preview
- Create backups before destructive operations

### Validation

- Validate early (fail fast)
- Skip expensive checks if basic checks fail
- Cache validation results when appropriate

## Security Best Practices

### Input Validation

Always validate user inputs:

```python
# Validate skill name format
if not all(c.islower() or c.isdigit() or c == '-' for c in skill_name):
    return {'success': False, 'error': 'Invalid format'}

# Validate paths
path = Path(user_input).resolve()
if not path.is_relative_to(allowed_base_dir):
    return {'success': False, 'error': 'Path not allowed'}
```

### File Operations

- Never trust user-provided paths
- Use Path.resolve() to prevent traversal
- Check file existence before operations
- Handle permissions errors gracefully

### Template Variables

- Sanitize user input before template rendering
- Escape special characters if needed
- Validate variable values match expected format

## Maintenance Best Practices

### Regular Updates

- Update dependencies periodically
- Test with latest Claude Code version
- Fix deprecated patterns
- Improve documentation based on user feedback

### Issue Tracking

- Use GitHub issues for bug reports
- Label issues appropriately (bug, enhancement, documentation)
- Respond to issues promptly
- Close resolved issues with explanation

### Changelog

Maintain CHANGELOG.md:

```markdown
# Changelog

## [0.2.0] - 2025-03-15
### Added
- New command: export-data
- Support for JSON output

### Changed
- Improved error messages
- Updated documentation

### Fixed
- Bug in validation logic

## [0.1.0] - 2025-03-01
### Added
- Initial release
```

## Common Pitfalls to Avoid

### 1. Overly Generic Skills

**Avoid**: Skills that try to do everything
**Instead**: Focus on specific, well-defined purpose

### 2. Poor Error Messages

**Avoid**: "Error occurred"
**Instead**: "Required file not found: .claude-plugin/marketplace.json"

### 3. Missing Validation

**Avoid**: Assuming inputs are correct
**Instead**: Validate all user inputs before processing

### 4. Inconsistent Naming

**Avoid**: Mixing naming conventions
**Instead**: Use kebab-case consistently

### 5. Insufficient Documentation

**Avoid**: Minimal or missing documentation
**Instead**: Document tools, commands, usage thoroughly

### 6. Skipping Validation

**Avoid**: Syncing without validating
**Instead**: Always validate before syncing

### 7. Not Testing Locally

**Avoid**: Pushing untested changes
**Instead**: Test locally before distributing

## See Also

- [Commands Reference](./commands-reference.md) - Command documentation
- [Template Guide](./template-guide.md) - Template customization
- [Main README](../README.md) - Overview and installation
