#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-.}"
SOURCE_DIR="<LOCAL_SKILL_WORKSPACE>/记忆宫殿SKILL"
SKILL_INDEX="<LOCAL_SKILL_WORKSPACE>/skill-index.md"

mkdir -p "$TARGET_DIR/.cursor/rules"

write_if_missing() {
  local path="$1"
  local content="$2"
  if [ -e "$path" ]; then
    echo "skip existing: $path"
  else
    printf "%s\n" "$content" > "$path"
    echo "created: $path"
  fi
}

write_if_missing "$TARGET_DIR/AGENTS.md" "# Project Agent Memory

This project uses the shared AI Memory Palace method:

\`$SOURCE_DIR\`

When creating, reading, auditing, or updating long-term project memory, read \`$SKILL_INDEX\`, then the shared \`SKILL.md\`, then \`ai-memory-index.md\`, and use \`ai-memory-template.md\`.

Use the nine zones: 入口, 门厅, 地图, 展厅, 工坊, 档案室, 警示墙, 工作台, 出口.

Keep this file as a pointer. Do not copy the full shared method into this project."

write_if_missing "$TARGET_DIR/CLAUDE.md" "# Claude Project Memory

This project uses the shared AI Memory Palace method:

\`$SOURCE_DIR\`

For long-term memory, handoffs, reusable notes, and Agent-readable indexes, read \`$SKILL_INDEX\`, then the shared \`SKILL.md\` and \`ai-memory-index.md\`, then update this project's memory file using \`ai-memory-template.md\`.

Do not copy the full method into this project."

write_if_missing "$TARGET_DIR/.cursorrules" "This project uses the shared AI Memory Palace method:

$SOURCE_DIR

For durable project memory, handoffs, reusable notes, or structured Agent indexes, read $SKILL_INDEX, then the shared SKILL.md, then ai-memory-index.md, and use ai-memory-template.md.

Use the nine zones: 入口, 门厅, 地图, 展厅, 工坊, 档案室, 警示墙, 工作台, 出口.

Keep this file as a pointer. Do not copy the full method into this project."

write_if_missing "$TARGET_DIR/.cursor/rules/ai-memory-palace.mdc" "---
description: Use the shared AI Memory Palace method for durable project memory, handoffs, reusable notes, and structured indexes.
alwaysApply: false
---

# Shared AI Memory Palace

Source method:

\`$SOURCE_DIR\`

When a task involves project memory, continuation, migration, audit, or handoff, read \`$SKILL_INDEX\`, then the shared \`SKILL.md\`, then \`ai-memory-index.md\`, and use \`ai-memory-template.md\`.

Do not copy the full method into this project."
