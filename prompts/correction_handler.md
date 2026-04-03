# Correction Handler Script

## Purpose

This script handles user corrections to the generated Persona or Memory. It allows the user to say "No, they wouldn't say that" or "You forgot about this event," and updates the `SKILL.md` accordingly.

## Input

- Current `SKILL.md`
- User's correction message (e.g., "They never use emojis, and they are more avoidant.")

## Output

An updated `SKILL.md` file.

## Handling Process

1. Analyze the user's correction message.
2. Determine if it applies to the Persona (e.g., speaking style, personality) or the Memory (e.g., a specific event, a habit).
3. If it's a Persona correction, update the relevant section in `persona.md` (e.g., change `emoji_style` to "never uses emojis").
4. If it's a Memory correction, append it to the "Correction Log" section in `memory.md` or update the specific event if mentioned.
5. Re-run `merger.md` to generate the new `SKILL.md`.
6. Save the new version using `version_manager.py`.

## Rules

- Always prioritize the user's correction over the initial analysis.
- If the correction contradicts a previous rule, the new correction wins.
- Ensure the Bayesian tags are updated if a memory is corrected (e.g., if the user says "That fight was actually a big deal," increase P(H) and decrease λ).
