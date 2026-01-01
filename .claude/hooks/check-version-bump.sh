#!/bin/bash
#
# Pre-commit hook to enforce version bumping for plugin changes.
# Blocks git commit/push if functional plugin files are staged without version bumps.
#

set -e

# Read hook input from stdin
input=$(cat)

# Extract the command being run
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# Only check git commit and git push commands
if [[ ! "$command" =~ ^git\ (commit|push) ]]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# For push: warn but don't block (user may have already committed with version)
if [[ "$command" =~ ^git\ push ]]; then
  exit 0
fi

# For commit: check if functional changes require version bump
# Get list of staged files
staged_files=$(git diff --cached --name-only 2>/dev/null || echo "")

if [[ -z "$staged_files" ]]; then
  exit 0
fi

# Patterns for functional plugin files (require version bump)
functional_patterns=(
  "plugins/.*/skills/"
  "plugins/.*/commands/"
  "plugins/.*/agents/"
  "plugins/.*/hooks/"
  "plugins/.*/lib/"
  "plugins/.*\.py$"
  "plugins/.*\.sh$"
  "plugins/.*\.js$"
  "plugins/.*\.ts$"
)

# Patterns for non-functional files (skip version check)
skip_patterns=(
  "docs/"
  "README"
  "CLAUDE\.md"
  "\.md$"
  "\.txt$"
)

# Check which plugins have functional changes
declare -A plugins_with_changes

while IFS= read -r file; do
  [[ -z "$file" ]] && continue

  # Skip non-functional files
  skip=false
  for pattern in "${skip_patterns[@]}"; do
    if [[ "$file" =~ $pattern ]]; then
      skip=true
      break
    fi
  done
  $skip && continue

  # Check if file is a functional plugin file
  for pattern in "${functional_patterns[@]}"; do
    if [[ "$file" =~ $pattern ]]; then
      # Extract plugin name from path
      plugin=$(echo "$file" | sed -n 's|plugins/\([^/]*\)/.*|\1|p')
      if [[ -n "$plugin" ]]; then
        plugins_with_changes["$plugin"]=1
      fi
      break
    fi
  done
done <<< "$staged_files"

# If no functional plugin changes, allow commit
if [[ ${#plugins_with_changes[@]} -eq 0 ]]; then
  exit 0
fi

# Check if version files are staged for affected plugins
missing_versions=()

for plugin in "${!plugins_with_changes[@]}"; do
  version_file="plugins/$plugin/.claude-plugin/plugin.json"
  if ! echo "$staged_files" | grep -q "^$version_file$"; then
    missing_versions+=("$plugin")
  fi
done

# If all affected plugins have version files staged, allow commit
if [[ ${#missing_versions[@]} -eq 0 ]]; then
  exit 0
fi

# Block commit and report missing version bumps
echo "" >&2
echo "VERSION BUMP REQUIRED" >&2
echo "=====================" >&2
echo "" >&2
echo "Functional changes detected in the following plugins without version bumps:" >&2
echo "" >&2
for plugin in "${missing_versions[@]}"; do
  echo "  - $plugin" >&2
  echo "    Update: plugins/$plugin/.claude-plugin/plugin.json" >&2
done
echo "" >&2
echo "Please bump the version field in each plugin.json before committing." >&2
echo "See CLAUDE.md 'Version Management' section for guidelines." >&2
echo "" >&2

# Exit code 2 = blocking error for Claude Code hooks
exit 2
