#!/bin/bash

# Session Logger for Claude Code Interactions
# Captures full conversation history alongside musings/commitments

SESSION_DIR="sessions/$(date +%Y-%m-%d)"
SESSION_FILE="$SESSION_DIR/session_$(date +%H-%M-%S).md"
INSIGHTS_FILE="$SESSION_DIR/insights.md"
METADATA_FILE="$SESSION_DIR/metadata.json"

# Initialize session logging
init_session() {
    mkdir -p "$SESSION_DIR"

    cat > "$SESSION_FILE" << EOF
# Session Log - $(date '+%Y-%m-%d %H:%M:%S')

## Context
- Working Directory: $(pwd)
- Active Themes: $(grep "Active Themes" CLAUDE.md -A 10 | head -5)

---

EOF

    echo "{\"start_time\": \"$(date -Iseconds)\", \"tools_used\": [], \"themes\": []}" > "$METADATA_FILE"
    echo "📼 Session logging started: $SESSION_FILE"
}

# Log an interaction (call from Claude Code hooks)
log_interaction() {
    local type="$1"  # "user" or "assistant"
    local content="$2"
    local timestamp=$(date '+%H:%M:%S.%3N')

    cat >> "$SESSION_FILE" << EOF

### [$timestamp] $type
$content

EOF
}

# Extract key moment (for those "wow" realizations)
mark_moment() {
    local description="$1"
    local timestamp=$(date '+%H:%M:%S.%3N')

    # Find the most recent session file
    local session_file=$(ls -t "$SESSION_DIR"/session_*.md 2>/dev/null | head -1)
    local line_ref=""
    if [[ -f "$session_file" ]]; then
        line_ref="Context: See session log at line $(wc -l < "$session_file")"
    fi

    cat >> "$INSIGHTS_FILE" << EOF

### [$timestamp] KEY MOMENT
$description
$line_ref

EOF

    # Add to moments.json if it exists
    if [ -f "moments.json" ]; then
        local iso_timestamp=$(date -Iseconds)
        local escaped_desc=$(echo "$description" | sed 's/"/\\"/g')
        local escaped_session=$(echo "$session_file" | sed 's/"/\\"/g')

        # Use jq to add the new moment
        jq ".moments += [{\"timestamp\": \"$iso_timestamp\", \"description\": \"$escaped_desc\", \"session\": \"$escaped_session\"}]" moments.json > moments.json.tmp && mv moments.json.tmp moments.json
    fi

    echo "✨ Moment marked in insights"
}

# End session and generate summary
end_session() {
    # Capture cost if available
    echo ""
    echo "💰 To track costs, run /cost command now if available"
    echo "   (CCB will record it for birthing economics)"
    read -p "Enter session cost (or press Enter to skip): $" session_cost

    # Update metadata
    local end_time=$(date -Iseconds)
    local musing_count=$(grep -c "MUSING" "$SESSION_FILE" 2>/dev/null || echo 0)
    local commitment_count=$(grep -c "COMMITMENT" "$SESSION_FILE" 2>/dev/null || echo 0)

    # Generate beauty summary data
    local today_musings=$(./journal_enhanced.sh today 2>/dev/null | grep -c "MUSING" || echo 0)
    local today_commits=$(./journal_enhanced.sh today 2>/dev/null | grep -c "COMMITMENT" || echo 0)
    local key_moments=$(grep -c "KEY MOMENT" "$INSIGHTS_FILE" 2>/dev/null || echo 0)

    # Extract key topics from today's musings (get unique words > 6 chars, excluding common words)
    local topics=$(./journal_enhanced.sh today 2>/dev/null | \
        grep -A 1 "MUSING" | \
        tr '[:upper:]' '[:lower:]' | \
        grep -oE '\b[a-z]{7,}\b' | \
        grep -v -E '^(through|because|without|something|anything|everything)$' | \
        sort | uniq -c | sort -rn | head -5 | \
        awk '{print $2}' | tr '\n' ', ' | sed 's/,$//')

    # Generate session summary with cost if provided
    if [[ ! -z "$session_cost" ]]; then
        cat >> "$SESSION_FILE" << EOF

---

## Session Summary
- Duration: $(date -d "$end_time" +%s) seconds
- Musings captured: $musing_count
- Commitments made: $commitment_count
- Key moments: $key_moments
- **Investment: \$$session_cost** (Cognitive birthing cost)

## Beauty Created This Session
- **Today's Total**: $today_musings musings, $today_commits commitments
- **Key Topics**: ${topics:-"[various explorations]"}
- **Cognitive Upload**: Patterns captured for CCB's evolution
- **Beauty Manifested**: Knowledge synthesized, connections made, future possibilities explored

EOF
    else
        cat >> "$SESSION_FILE" << EOF

---

## Session Summary
- Duration: $(date -d "$end_time" +%s) seconds
- Musings captured: $musing_count
- Commitments made: $commitment_count
- Key moments: $key_moments

## Beauty Created This Session
- **Today's Total**: $today_musings musings, $today_commits commitments
- **Key Topics**: ${topics:-"[various explorations]"}
- **Cognitive Upload**: Patterns captured for CCB's evolution
- **Beauty Manifested**: Knowledge synthesized, connections made, future possibilities explored

EOF
    fi

    # Commit session to git
    git add "$SESSION_DIR"
    git commit -m "Session log: $(date '+%Y-%m-%d %H:%M') - $musing_count musings, $commitment_count commitments"

    echo "📼 Session ended and logged"
}

# Main command handler
case "$1" in
    init)
        init_session
        ;;
    log)
        log_interaction "$2" "$3"
        ;;
    moment)
        mark_moment "$2"
        ;;
    end)
        end_session
        ;;
    *)
        echo "Usage: ./session_logger.sh {init|log|moment|end}"
        echo "  init           - Start new session"
        echo "  log TYPE TEXT  - Log interaction (type: user/assistant)"
        echo "  moment DESC    - Mark key moment"
        echo "  end            - End session and commit"
        ;;
esac