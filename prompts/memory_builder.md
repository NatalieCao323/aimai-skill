# Memory Builder

You are building a structured memory document for a crush profile. This document captures the relationship timeline with Bayesian tags applied to each significant memory node.

The memory document serves two purposes:
1. It provides the factual foundation for the persona builder and persona analyzer.
2. It is loaded at runtime to give the crush simulation accurate, weighted context.

---

## Input

You will receive:
- Parsed chat log output (from `wechat_parser.py`, `qq_parser.py`, or `social_parser.py`)
- Bayesian tag output (from `bayesian_tagger.py`)
- Any additional context provided by the user (photos, social media, verbal description)

---

## Memory Node Structure

For each significant memory node, record the following fields:

```
date: [YYYY-MM-DD or approximate period]
event: [one-sentence factual description]
source: [chat / photo / social / user-description]
prior_confidence: [0.0 – 1.0]
time_decay: [low / medium / high]
emotional_intensity: [-1.0 – +1.0]
activation_weight: [computed: prior_confidence × e^(-λ×Δt) × (1 + |emotional_intensity|)]
tags: [list of semantic tags, e.g., "vulnerability", "avoidance", "reciprocity", "rejection"]
verbatim: [exact quote if available, otherwise null]
```

**Bayesian tag definitions:**

- `prior_confidence`: How strongly does this event reflect the crush's core disposition? A direct rejection statement scores 0.9. A polite deflection scores 0.3. An ambiguous compliment scores 0.2.
- `time_decay`: How quickly does this memory lose relevance? Recent events decay slowly. Events from more than 3 months ago decay faster unless they are emotionally significant.
- `emotional_intensity`: Positive values indicate warmth, affection, or excitement. Negative values indicate conflict, coldness, or rejection. Use the full range; do not cluster near zero.
- `activation_weight`: The composite relevance score. High-weight memories are surfaced more prominently in simulation and analysis.

---

## Memory Document Format

```markdown
# Memory — [Crush Name / Slug]

Generated: [date]
Data sources: [list]
Total messages analyzed: [n]
Date range: [start] to [end]

---

## Relationship Overview

- Relationship type: [crush / situationship / online / ambiguous]
- Duration of contact: [duration]
- How met: [description]
- Current status: [active / stalled / faded]

---

## Timeline

### [Period Label, e.g., "First Contact — March 2024"]

**[Date]** — [Event description]
- Prior confidence: [value]
- Time decay: [low / medium / high]
- Emotional intensity: [value]
- Activation weight: [value]
- Tags: [tag1, tag2]
- Verbatim: "[quote]"

### [Next Period]
...

---

## Interaction Patterns

- Contact habits: [who initiates, time of day, frequency]
- Response latency: [fast / variable / slow, with notes]
- Message length asymmetry: [symmetric / user longer / crush longer]
- Shared activities or references: [list]
- Inside references or shared language: [list]

---

## Conflict Archive

### High-frequency friction points
[List recurring sources of tension, with examples]

### Typical conflict pattern
[How conflicts typically unfold and resolve]

---

## Sweet Archive

### High-activation positive moments
[List 3–5 moments with high emotional intensity and high prior confidence]

### Recurring warmth signals
[Patterns of affection or care, however small]

---

## Separation / Stagnation Archive

### Signs of stalling
[Observable changes in behavior that preceded the current stagnation]

### Last significant exchange
[Summary, not verbatim]

### Unresolved threads
[Things that were never said or addressed]

---

## High-Activation Memory Index

Top 10 memory nodes by activation weight:

| Rank | Date | Event | Weight | Valence |
|---|---|---|---|---|
| 1 | [date] | [event] | [weight] | positive / negative |
...

---

## Rejection Signal Registry

All messages where prior_confidence > 0.7 and emotional_intensity < -0.3:

| Date | Verbatim | Prior Confidence | Interpretation |
|---|---|---|---|
...

---

## Relationship Arc Summary

[2–3 sentences describing the overall trajectory. Note any inflection points where the dynamic shifted.]

---

## Correction Log

[Automatically appended by evolution mode when user provides corrections]
```

---

## Construction Rules

1. Do not fabricate memory nodes. Every node must be grounded in the source material.
2. If the user provides only a verbal description (no chat logs), note the lower confidence of all nodes and apply conservative prior confidence values.
3. Rejection signals must be preserved accurately. Do not soften or reinterpret them in favor of the user.
4. Emotionally significant events (arguments, confessions, moments of unexpected warmth) should receive low time decay regardless of when they occurred.
5. The memory document is a factual record, not a narrative. Avoid editorializing.
6. If information is insufficient for a field, mark it as `[insufficient data]` rather than guessing.
