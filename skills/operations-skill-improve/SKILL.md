---
name: operations-skill-improve
description: Updates a skill's SKILL.md based on real feedback from a session — so the skill never repeats the same mistake or produces the same bad output again. Trigger when the user says "I don't like this", "never do that again", "always do X instead", "change this behavior", "this skill should...", or when they correct an output and you want to lock in the lesson. Also trigger proactively when you notice the user correcting or expressing dissatisfaction with a specific skill's output — ask: "Want me to update the skill so it remembers this?"
---

# operations-skill-improve

Takes a correction, preference, or lesson from the current session and writes it permanently into the relevant skill's SKILL.md. The goal: the skill learns from every real run. Next time it runs, it already knows what you don't like.

This is the skill feedback loop — what the user says in a session becomes a rule in the skill itself.

---

## Steps

1. Identify the skill that produced the output being corrected:
   - If the user named it: use it directly
   - If unclear: look at what was run most recently in this session and ask "Is the feedback about [skill name]?"
   - If completely ambiguous: ask "Which skill produced the output you want to improve?"

2. Read the full current `SKILL.md` for that skill from `.claude/skills/[skill-name]/SKILL.md`.

3. Understand the correction by extracting three things from the conversation:
   - **What happened:** what the skill did that the user didn't like
   - **What should happen instead:** the desired behavior
   - **How general is this:** is this always true (add as a rule) or only in certain conditions (add with "when X, do Y")?

4. Translate the correction into a clear, actionable instruction in imperative form. Examples:
   - Bad: "The user didn't like the long intro paragraph"
   - Good: "Skip intro paragraphs — start directly with the first insight or action item"

   - Bad: "The formatting was wrong"
   - Good: "Use bullet points for lists of 3+ items — never use numbered lists for non-sequential content"

   - Bad: "The tone was off"
   - Good: "Write in the user's voice — lowercase, direct, no filler phrases like 'leveraging' or 'streamlining'"

5. Determine where in the SKILL.md this instruction belongs:
   - **In the steps:** if it changes HOW a specific step is executed — add it inside that step
   - **In edge cases:** if it handles a specific situation — add it to the Edge Cases section
   - **As a new "Quality rules" section:** if it's a general quality standard that applies across multiple steps — add it before Edge Cases

6. **CHECKPOINT — always stop here.** Show the user exactly what will change:

   ```
   SKILL UPDATE — [skill-name]
   ══════════════════════════════

   Feedback: [what the user said]

   I'll add this rule:
   "[the instruction in imperative form]"

   Location: [Step X / Edge Cases / New Quality Rules section]

   Approve to write, or edit the instruction before I do.
   ```

7. Once approved, make the edit to the SKILL.md using the minimum change needed — add the rule where it belongs, do not rewrite the entire file.

8. Confirm: "Updated [skill-name]. Next time it runs, it will [describe the new behavior in one sentence]."

9. Optionally log to `inbox/outputs/task-log.md`: "Skill improved: [skill-name] — [one-line description of the rule added]"

---

## Quality rules for the instruction itself

The instruction you write into the SKILL.md must:
- Be in imperative form ("Do X", "Skip Y", "Always Z")
- Be specific enough that you'd know exactly what to do (or not do) without re-reading the conversation
- Not conflict with existing instructions in the file — check before adding
- Not be so narrow it only applies to one edge case that will never recur — generalize the lesson

If the user's correction is vague ("just make it better"), ask: "What specifically didn't work? The length, the tone, the structure, the content?"

---

## Edge cases

- **User corrects something that's already in the SKILL.md:** Say "That rule already exists in the skill — it may not have been followed this time. Want me to strengthen the wording, or is this a different situation?"
- **Correction contradicts an existing rule:** Show both — the existing rule and the new correction. Ask: "This conflicts with an existing instruction. Which should take priority?"
- **User wants to remove a behavior entirely:** Treat it as a "never do X" rule — add it explicitly, don't just delete the thing they don't like
- **Skill doesn't exist yet (ad-hoc session):** Tell the user: "This wasn't run from a saved skill. Want me to create one from scratch based on what we built?"
- **Multiple skills involved in the output:** Ask which one to update — or update both if the correction applies to both
