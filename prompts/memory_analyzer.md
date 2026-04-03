# Memory Analyzer Script

## Purpose

This script analyzes raw chat logs, social media posts, and photo metadata to extract factual memories and build the Relationship Memory. It applies Bayesian tags to key memory fragments.

## Input

- Raw chat logs (parsed by `wechat_parser.py` or `qq_parser.py`)
- Social media text (parsed by `social_parser.py`)
- Photo metadata (parsed by `photo_analyzer.py`)
- User's subjective description

## Output

A structured Relationship Memory document based on `memory_builder.md`.

## Analysis Steps

1. **Timeline Extraction**: Identify key dates (first message, last message, significant gaps, mentions of meeting/dating).
2. **Location Extraction**: Identify frequently mentioned places or locations from photo EXIF data.
3. **Habit Analysis**: Calculate average reply speed, active hours, and who initiates conversations more often.
4. **Conflict Identification**: Search for keywords indicating arguments, cold wars, or misunderstandings. Extract the cause and resolution pattern.
5. **Sweet Moment Identification**: Search for keywords indicating affection, compliments, or shared joy.
6. **Key Memory Fragment Selection**: Select 5-10 most significant interactions (both positive and negative).
7. **Bayesian Tagging**: For each key memory fragment, assign:
   - `P(H)` (Prior Confidence): 0.0-1.0. High for actions reflecting their core personality (e.g., consistent avoidance), low for out-of-character moments (e.g., a rare drunken confession).
   - `λ` (Time Decay Factor): 0.0-1.0. High for trivial daily chats, low for deep, emotional conversations or major conflicts.
   - `E` (Emotional Intensity): -1.0 to 1.0. Negative for fights/rejections, positive for sweet/flirtatious moments.

## Output Format

Follow the structure defined in `memory_builder.md`.
