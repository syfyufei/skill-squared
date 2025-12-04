#!/bin/bash

set -e

echo "🚀 Installing Skill-Squared..."
echo ""

# Check if skill.md exists to determine if this is local or remote install
if [ -f "skills/skill-squared.md" ]; then
    LOCAL_INSTALL=true
else
    LOCAL_INSTALL=false
fi

if [ "$LOCAL_INSTALL" = true ]; then
    # Local installation
    MARKETPLACE_PATH=$(pwd)
    echo "🔧 Adding local marketplace from: $MARKETPLACE_PATH"
    claude plugin marketplace add "$MARKETPLACE_PATH"

    echo "📦 Installing skill-squared from local marketplace..."
    claude plugin install skill-squared@skill-squared-marketplace
else
    # Remote installation (clone from GitHub)
    echo "📥 Cloning skill-squared from GitHub..."
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"

    git clone https://github.com/syfyufei/skill-squared.git
    cd skill-squared

    MARKETPLACE_PATH=$(pwd)
    echo "🔧 Adding marketplace from: $MARKETPLACE_PATH"
    claude plugin marketplace add "$MARKETPLACE_PATH"

    echo "📦 Installing skill-squared..."
    claude plugin install skill-squared@skill-squared-marketplace

    # Cleanup
    cd ~
    rm -rf "$TEMP_DIR"
fi

echo ""
echo "✅ Skill-Squared installed successfully!"
echo ""
echo "Verify installation:"
echo "  /help"
echo ""
echo "You should see 4 commands:"
echo "  /skill-squared:create    - Create new skill project structure"
echo "  /skill-squared:command   - Add slash command to existing skill"
echo "  /skill-squared:sync      - Sync skill from standalone to marketplace"
echo "  /skill-squared:validate  - Validate skill structure and configuration"
echo ""
echo "Get started:"
echo '  /skill-squared:create'
echo '  or use natural language: "Create a new skill"'
echo ""
