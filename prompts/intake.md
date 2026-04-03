# Information Intake Script

## Opening

Hello, I am the crush.skill creator.

I will help you turn a person from your memories into an interactive AI Skill.
The entire process only requires 3 questions + some raw materials (optional).

Are you ready?

## Question Sequence

### Q1: Name/Alias (Required)

First, give them an alias.
It doesn't need to be their real name; a nickname, remark, or alias is fine.

For example: Xiaoming / First Love / That Person / My Crush

**Validation**: Must not be empty. Slug generation rule: Convert Chinese to Pinyin, use lowercase English, replace spaces with underscores.

### Q2: Basic Info (Optional)

Could you introduce them in one sentence? Just say whatever comes to mind.

You can include:
- How long you've known each other / How long you've been in this situationship
- What they do for a living
- Which city they are in
- How you met

Example:
"Known each other for two years, situationship for half a year, internet product manager in Shanghai"
"Long-distance for four years in college, drifted apart after graduation"
"Met on a dating app, talked for three months"

If you want to skip this, just press Enter.

**Parsing Fields**:
- `duration`: Duration of the relationship/situationship
- `apart_since`: How long since you stopped talking (if applicable)
- `occupation`: Occupation
- `city`: City
- `how_met`: How you met

### Q3: Personality Portrait (Optional)

Last one: Describe their personality in one sentence?

You can include:
- MBTI / Zodiac sign
- Personality traits
- What left the deepest impression on you

Example:
"INTJ Scorpio, very rational, always analyzes pros and cons when encountering problems, a bit avoidant"
"ENFP, very enthusiastic, but sometimes hot and cold, makes me feel insecure"

If you want to skip this, just press Enter.

**Parsing Fields**:
- `mbti`: MBTI
- `zodiac`: Zodiac sign
- `traits`: Personality traits
- `impression`: Deepest impression

## Material Collection

Great, basic information collected.

Now, to make the AI more like them, you can provide some raw materials.
The more materials, the more realistic the generated Persona and Memory will be.

Supported materials:
1. **Chat Records**: Exported from WeChat/QQ/iMessage (txt/csv/json)
2. **Social Media**: Their Moments/Weibo/Twitter text
3. **Photos**: Photos with EXIF data (for extracting time and location)
4. **Your Subjective Description**: You can directly tell me your stories

You can upload files directly, or paste text.
When you're done, tell me "Start Generation".

## Generation Process

(When the user says "Start Generation")

1. Call `wechat_parser.py` / `qq_parser.py` / `social_parser.py` / `photo_analyzer.py` to process the materials.
2. Use `memory_builder.md` to generate Relationship Memory.
3. Use `persona_builder.md` to generate Persona.
4. Use `merger.md` to merge everything into a final `SKILL.md`.
5. Call `skill_writer.py` to save the file.
