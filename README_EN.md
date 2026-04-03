# crush.skill

> ex-skill says: I would go back to that summer for you ten thousand times.
> crush.skill asks: in that summer, did they ever really like you back?

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-green.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude-Code-orange.svg)](https://claude.ai/code)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-purple.svg)](https://openclaw.ai)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-lightgrey.svg)](https://agentskills.dev)

*Inspired by [ex-skill](https://github.com/therealXiaomanChu/ex-skill)*

[Installation](#installation) · [Usage](#usage) · [Examples](#examples) · [Installation Guide](INSTALL.md) · [中文](README.md)

---

You are not together yet. But you have already started thinking twice before sending a message.

You remember the exact tone of their "maybe next time" — and how it sounded completely different from "wish you were here." You are not sure if they think about you too. You just want to know whether this situationship is worth continuing.

Feed your chat history to an AI. Not to win them over. To see clearly.

---

## What it does

**Diagnostic report**: Feed in your chat logs. The AI applies Bayesian tags to each message, then outputs a progression score, attachment style diagnosis, psychological environment analysis, and specific next-step scripts.

**Simulation mode**: The AI fully replicates their texting style, response rhythm, and phrasing. Rehearse your next conversation before it happens.

**Memory engine**: Every memory carries three Bayesian tags — prior confidence, time decay, and emotional intensity. The AI remembers and forgets the way a human brain does.

---

## Bayesian Memory Engine

Every message in the chat log is automatically tagged with three values:

| Tag | Meaning | Example |
|---|---|---|
| **Prior Confidence P(H)** | How strongly does this reflect their core attitude? | "I don't want a relationship" → 0.9; "maybe sometime" → 0.2 |
| **Time Decay λ** | How quickly does this memory lose relevance? | Late-night vulnerable conversation → low decay; daily check-in → high decay |
| **Emotional Intensity E** | Emotional weight | Jealousy / flirting → +0.8; cold withdrawal → -0.8 |

Dynamic activation weight: **W_t = P(H) × e^(-λΔt) × (1 + |E|)**

| Weight | Interpretation |
|---|---|
| W_t > 1.0 | Real signal. Act on it. |
| W_t 0.5–1.0 | Ambiguous. Keep observing. |
| W_t < 0.5 | Stop projecting. |

---

## Installation

### Claude Code

```bash
# Global install (recommended)
git clone https://github.com/NatalieCao323/crush-skill ~/.claude/skills/crush
cd ~/.claude/skills/crush && pip install -r requirements.txt

# Launch
claude
```

Type `/create-crush` to begin.

### OpenClaw

**Option A: Install via ClawHub (recommended)**

```bash
openclaw skills install crush
```

Restart OpenClaw and enable crush.skill in the Skills panel.

**Option B: Manual install**

```bash
git clone https://github.com/NatalieCao323/crush-skill ~/.openclaw/skills/crush
pip install -r ~/.openclaw/skills/crush/requirements.txt
```

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "load": {
      "extraDirs": ["~/.openclaw/skills"]
    }
  }
}
```

Restart OpenClaw and enable crush.skill in the Skills panel.

> **OpenClaw notes**:
> - Requires `python3` in PATH. The skill auto-detects on load.
> - macOS users can install `Pillow` and `piexif` via one-click in the Skills UI.
> - In sandbox mode, install `python3` inside the container via `agents.defaults.sandbox.docker.setupCommand`.
> - OpenClaw uses `{baseDir}` to reference the skill directory (Claude Code uses `${CLAUDE_SKILL_DIR}`).

---

## Usage

### Create a crush profile

```
/create-crush
```

The AI will ask three questions, then guide you through uploading your chat logs. Supported formats:

| Platform | Export method | Format |
|---|---|---|
| WeChat (Windows) | [WeChatMsg](https://github.com/LC044/WeChatMsg) | TXT / HTML |
| WeChat (macOS) | Manual copy-paste | Plain text |
| QQ | Built-in export | TXT |
| Manual | Paste directly | Plain text |

Minimal format (paste directly):
```
Alex: wish you were here
Me: I miss you too
Alex: oh, just asking haha
```

### Commands

| Command | Description |
|---|---|
| `/create-crush` | Create a new crush profile |
| `/{slug}` | Simulation mode: AI mimics their texting style |
| `/{slug}-report` | Analyst mode: full diagnostic report + action plan |
| `/list-crushes` | List all profiles |
| `/update-crush {slug}` | Upload new chat logs and update the profile |
| `/versions {slug}` | View version history |
| `/rollback {slug} {id}` | Roll back to a previous version |
| `/delete-crush {slug}` | Delete a profile |
| `/wake-up {slug}` | You are over it. Delete the profile. |

---

## Examples

### Example 1: The Avoidant

**Context**: Two months of frequent texting, but every attempt to meet in person gets deflected. Uploaded WeChat logs (847 messages).

**Diagnostic report**:

```
Bayesian Progression Score: 3.2 / 10

Attachment style: Avoidant (confidence: 82%)
Evidence: Three dinner invitations declined with "been really busy lately,"
but initiated late-night conversations on the same days.

Psychological environment:
  Primary: Options Maximizer (extracting emotional value with no intention to progress)
  Secondary: Pursuit-Withdrawal Loop (user leads pursuit; subject cycles between
             engagement and withdrawal to maintain the dynamic)

Risk flag:
  Pursuit-withdrawal cycle has completed 4 iterations.
  Continued pursuit will reinforce the existing power asymmetry.

Recommendation 1:
  Action: Stop initiating contact for 10 days.
  Rationale: You are the pursuing party. In their cost-benefit calculation, you are
             low-cost and always available. Withdrawal resets the calculation.
  Script: Send nothing. If they reach out, reply briefly, ask no questions, end the
          conversation first.

Recommendation 2:
  Action: The next time they say "maybe next time," return the initiative.
  Script: "Sure, you pick the time — I'll check if I'm free."
          Then do not follow up.
```

**Simulation mode**:

```
You: Still awake?
Alex (AI): Yeah, you?
You: Just got out of the shower
Alex (AI): Oh
(The AI accurately reproduced their minimal response pattern,
 helping you see the dynamic clearly)
```

---

### Example 2: Post-Trauma Withdrawal

**Context**: Deep, vulnerable conversations, but they go cold for three days every time you ask "what are we."

**Diagnostic report**:

```
Bayesian Progression Score: 5.8 / 10

Attachment style: Fearful-Avoidant (confidence: 79%)
Evidence: Voluntarily shared personal vulnerabilities (activation weight: 1.42),
but response latency increased from 10 minutes to 4 hours after user expressed
clear romantic interest.

Psychological environment:
  Primary: Post-Trauma Withdrawal (intimacy triggers a defensive response)
  Secondary: Genuine Ambivalence (real uncertainty, not strategic avoidance)

Recommendation:
  Action: Stop asking "what are we." Reframe the conversation.
  Script: "I don't need an answer right now. I just want you to know
          I'm not going anywhere."
  Then change the subject. Do not wait for a response.
```

---

### Example 3: Mutual Standoff

**Context**: Mutual jealousy, high-frequency contact, but neither person makes a move.

**Diagnostic report**:

```
Bayesian Progression Score: 7.1 / 10

Attachment style: Secure (confidence: 71%)
Evidence: Direct emotional expression, no avoidance behavior, clear positive
responses to user's affection.

Psychological environment:
  Primary: Mutual Approach-Avoidance (both waiting for the other to go first)

Recommendation:
  Action: Say it directly.
  Script: "I've realized I like you. What about you?"
  Rationale: Secure attachment types respond well to directness.
             Continued ambiguity only erodes the connection.
```

---

### Example 4: Three "Maybe Next Times"

**Context**: They have said "maybe next time" three times in a row.

```
Bayesian cumulative weight across three deflections: W_t = 0.08

This is not a scheduling conflict. This is a choice.

Someone who genuinely wants to see you will pair "maybe next time"
with a specific alternative time.

Recommendation: Stop initiating plans. Observe whether they propose
a meeting within 30 days. If not, you have your answer.
```

---

### Example 5: Photo Timeline Analysis

**Context**: They shared photos over several months. You want to understand their activity patterns.

```
Photos analyzed: 23
Date range: 2024-01-15 to 2024-03-20

Timeline:
  2024-01-15  GPS: Coffee shop, Jing'an District, Shanghai  [Monday 14:32]
  2024-02-03  GPS: Gym, Chaoyang District, Beijing          [Saturday 09:15]
  2024-03-01  GPS: Restaurant, Pudong, Shanghai             [Friday 19:44]

Pattern: Weekdays in Shanghai. Occasional weekends in Beijing.
         Consistent gym habit on Saturday mornings.
```

---

## File structure

```
crush.skill/
  SKILL.md              Skill entry file (Claude Code + OpenClaw)
  README.md             Documentation (Chinese)
  README_EN.md          This file (English)
  INSTALL.md            Detailed installation guide
  requirements.txt      Python dependencies
  LICENSE               MIT license
  prompts/
    intake.md           Three-question intake script
    memory_builder.md   Bayesian memory document template
    memory_analyzer.md  Memory pattern analysis
    persona_builder.md  Five-layer persona construction template
    persona_analyzer.md Attachment style + 10-scenario psychological diagnosis
    bayesian_analysis.md Bayesian tagging instructions
    merger.md           Merge and generate final SKILL.md
    correction_handler.md User correction + evolution mode
  tools/
    wechat_parser.py    WeChat log parser (TXT / HTML / JSON)
    qq_parser.py        QQ log parser
    social_parser.py    Social media text parser
    photo_analyzer.py   Photo EXIF + GPS timeline analysis
    bayesian_tagger.py  Bayesian tagging engine
    skill_writer.py     Skill file management
    version_manager.py  Version snapshots + rollback
```

---

## Privacy

All data is processed locally. Chat logs, photos, and personal information are never uploaded to any external server. Generated skill files are stored entirely on your device.

This project is intended solely for personal emotional analysis and conversation practice. It must not be used to harass, stalk, or violate the privacy of others.

---

## Credits

Inspired by [ex-skill](https://github.com/therealXiaomanChu/ex-skill) by therealXiaomanChu.

---

MIT License
