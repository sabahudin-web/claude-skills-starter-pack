#!/bin/bash
# voice-detect.sh
# Fires on every UserPromptSubmit.
# Reads the user's prompt, detects voice/dictation patterns,
# and injects a mandatory instruction to run operations-prompt-master.

# Read JSON input from stdin
input=$(cat 2>/dev/null || echo "")

# Extract prompt text — try common field names
prompt=$(echo "$input" | jq -r '.prompt // .message // .content // ""' 2>/dev/null || echo "")

# If we couldn't extract the prompt, exit silently — don't break the session
if [ -z "$prompt" ]; then
  exit 0
fi

# Skip: structured/numbered input (>200 chars AND has 2+ numbered list items)
# This prevents false positives on plan-mode input, long CLI prompts, and numbered instructions
char_count=${#prompt}
has_numbered_list=$(echo "$prompt" | grep -cE '^[[:space:]]*[0-9]+\.' 2>/dev/null || echo "0")
if [ "$has_numbered_list" -gt 1 ] && [ "$char_count" -gt 200 ]; then
  exit 0
fi

# Count words and sentences
word_count=$(echo "$prompt" | wc -w | tr -d ' ')
sentence_count=$(echo "$prompt" | grep -oE '[.!?]+' | wc -l | tr -d ' ')

# Detect filler words and voice markers
has_filler=$(echo "$prompt" | grep -icE '\b(so basically|you know|like I said|kind of|let'\''s|gonna|wanna|okay so|I think that|that thing|you know what I mean|basically|I mean|right so|so like|and then|but like)\b' 2>/dev/null || echo "0")

# Detect self-corrections (dash or comma followed by restart)
has_correction=$(echo "$prompt" | grep -icE '(—|, but |, so |, and |I think|I had |I was)' 2>/dev/null || echo "0")

# Detect vague verbs
has_vague=$(echo "$prompt" | grep -icE '\b(make something|do something|some stuff|that thing|this thing|whatever|kind of like|sort of)\b' 2>/dev/null || echo "0")

# Voice detected if:
# - Has filler words, OR
# - Long message (>30 words, >3 sentences) with corrections, OR
# - Has vague verbs, OR
# - Very long AND many sentences (but NOT structured numbered input — already gated above)
voice_detected=0

if [ "$has_filler" -gt 0 ]; then
  voice_detected=1
fi

if [ "$has_correction" -gt 1 ] && [ "$word_count" -gt 30 ]; then
  voice_detected=1
fi

if [ "$has_vague" -gt 0 ]; then
  voice_detected=1
fi

if [ "$sentence_count" -gt 4 ] && [ "$word_count" -gt 40 ]; then
  voice_detected=1
fi

if [ "$voice_detected" -eq 1 ]; then
  cat <<'INJECT'

[VOICE INPUT DETECTED — RUN PROMPT MASTER BEFORE ANYTHING ELSE]
The user's message contains voice/dictation patterns (filler words, run-on sentences, self-corrections, or vague intent).

You MUST follow these steps in order — no exceptions:
1. DO NOT execute, plan, or respond from the raw input
2. Silently run `operations-prompt-master` on the raw input right now
3. Present the cleaned prompt in a code block
4. Ask exactly: "Would you like me to run this?"
5. Wait for explicit confirmation before proceeding
6. On confirmation — execute from the CLEAN prompt, not the original

This is a mandatory interception. Do not skip it.
[END VOICE DETECT]
INJECT
fi

exit 0
