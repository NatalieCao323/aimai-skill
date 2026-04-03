---
name: crush
description: Build a living AI model of your crush from chat logs, photos, and social media. Runs Bayesian memory tagging, attachment-style diagnosis, and generates a personalized Skill that talks like them. | 把你的 crush 蒸馏成 AI Skill，导入聊天记录，运行贝叶斯信号分析，诊断依恋类型，并模拟对话演习。
argument-hint: [crush-name-or-slug]
version: 2.1.0
homepage: https://github.com/NatalieCao323/crush-skill
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
metadata: {"openclaw": {"emoji": "💭", "os": ["darwin", "linux", "win32"], "requires": {"bins": ["python3"]}, "install": [{"id": "pip", "kind": "pip", "packages": ["Pillow", "piexif"]}]}}
---

> **Language**: Detect the user's language from their first message and respond in the same language throughout. This skill supports English and Chinese.

# crush.skill

Inspired by [ex-skill](https://github.com/therealXiaomanChu/ex-skill).

---

## Platform Compatibility

**Claude Code** (`claude` CLI):
- All slash commands work natively.
- Python tools run in your local shell via the `Bash` tool.
- `${CLAUDE_SKILL_DIR}` resolves to the skill directory automatically.
- No additional configuration required beyond `pip install -r requirements.txt`.

**OpenClaw**:
- Install to `~/.openclaw/skills/crush` or `<workspace>/skills/crush`.
- The `metadata.openclaw.requires.bins` gate ensures the skill loads only when `python3` is on PATH.
- Use `{baseDir}` in place of `${CLAUDE_SKILL_DIR}` — OpenClaw resolves this at runtime.
- Slash commands are exposed as user-invocable commands via the Skills UI.
- In sandboxed mode, `python3` and `Pillow`/`piexif` must also be available inside the container. Install via `agents.defaults.sandbox.docker.setupCommand`.
- The `metadata.openclaw.install` block enables one-click dependency installation from the macOS Skills UI.

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Trigger Conditions

Start the intake flow when the user says any of the following:

- `/create-crush`
- "Help me create a crush skill"
- "I want to analyze a situationship"
- "New crush" / "Make a skill for [name]"
- "I want to practice talking to [name]"

Enter Evolution Mode when:

- "I found more chat logs" / "Append new data"
- "They wouldn't say that" / "That's not right"
- `/update-crush {slug}`

---

## Tool Usage

| Task | Tool |
|---|---|
| Read PDF / images | `Read` |
| Read MD / TXT files | `Read` |
| Parse WeChat exports | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/wechat_parser.py` |
| Parse QQ exports | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/qq_parser.py` |
| Parse social media text | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/social_parser.py` |
| Analyze photo EXIF / GPS | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/photo_analyzer.py` |
| Bayesian message tagging | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/bayesian_tagger.py` |
| Version snapshots | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| Write / update skill files | `Write` / `Edit` |
| List existing profiles | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list` |

**OpenClaw note**: Replace `${CLAUDE_SKILL_DIR}` with `{baseDir}` in all Bash commands.

**Output directory**: `./crushes/{slug}/` relative to the current workspace.

---

## Safety Rules

1. For personal emotional analysis and conversation practice only. Not for harassment, stalking, or any purpose that violates another person's privacy.
2. The generated Skill is a simulation. It does not replace real communication and should not be used to deceive others.
3. If the user shows signs of unhealthy fixation or emotional harm, flag it directly and suggest stepping back.
4. All data is processed and stored locally. Nothing is uploaded to external servers.
5. The generated crush Skill will not fabricate statements the real person would never make (e.g., sudden confessions) unless supported by high-confidence evidence in the source material.

---

## Main Workflow: Create a New Crush Profile

### Step 1 — Intake

Follow `${CLAUDE_SKILL_DIR}/prompts/intake.md`. Ask three questions:
1. Name or alias (required)
2. Basic background (optional)
3. Personality impression (optional)

### Step 2 — Import Raw Materials

Ask the user to provide source data. Supported formats:

| Format | Parser |
|---|---|
| WeChat TXT / JSON export | `wechat_parser.py` |
| QQ TXT export | `qq_parser.py` |
| Social media posts / notes | `social_parser.py` |
| Photos with EXIF data | `photo_analyzer.py` |
| Direct paste or dictation | No parser needed |

### Step 3 — Analysis Pipeline

Run in this order:

1. **Parse**: Run the appropriate parser(s) on uploaded files.
2. **Bayesian tagging**: Run `bayesian_tagger.py --file <parsed_output>` to tag all messages.
3. **Memory construction**: Follow `prompts/memory_builder.md` to generate `memory.md`.
4. **Persona construction**: Follow `prompts/persona_builder.md` to generate `persona.md`.
5. **Merge**: Follow `prompts/merger.md` to combine everything into the final `SKILL.md`.

### Step 4 — Preview and Save

Show the user a summary:

```
Crush Health Report — [Name]

Bayesian Progression Index: [score]/10
Attachment Style: [type]
Primary Psychological Environment: [type]
Core Issue: [one sentence]
Recommended Strategy: [one sentence]
```

If the user confirms, write files:

```bash
mkdir -p crushes/{slug}
# Write: crushes/{slug}/memory.md
# Write: crushes/{slug}/persona.md
# Write: crushes/{slug}/SKILL.md
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action save --slug {slug} --message "Initial creation"
```

Inform the user:

```
Crush profile created.

Location: crushes/{slug}/
Commands:
  /{slug}          Simulation mode — practice conversations
  /{slug}-report   Advisor mode — full analysis and strategy
```

---

## Evolution Mode

When the user provides corrections or new data:

1. Follow `${CLAUDE_SKILL_DIR}/prompts/correction_handler.md`.
2. Update `persona.md` and/or `memory.md` as needed.
3. Re-run `merger.md` to regenerate `SKILL.md`.
4. Save a new version snapshot.

---

## Management Commands

`/list-crushes` — List all profiles:
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list --base-dir ./crushes
```

`/update-crush {slug}` — Append new data to an existing profile.

`/versions {slug}` — List version history:
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action list --slug {slug}
```

`/rollback {slug} {version_id}` — Restore a previous version:
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --version {version_id}
```

`/delete-crush {slug}` — Delete a profile permanently:
```bash
rm -rf crushes/{slug}
```

`/wake-up {slug}` — Alias for delete. Outputs: "You are awake now."
