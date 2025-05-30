# DistrictX Discord Bot

This bot manages school and contributor data for the DistrictX website via Discord slash commands.

## Setup

1. Copy `.env.example` to `.env` and fill in your tokens and repo info.
2. Install dependencies:
   ```
   pip install discord.py python-dotenv requests
   ```
3. Run the bot:
   ```
   python bot.py
   ```

## Commands

- `/addschool` — Add a new school
- `/editschool` — Edit a school
- `/deleteschool` — Delete a school
- `/addcontributor` — Add a contributor
- `/removecontributor` — Remove a contributor
- `/listcontributors` — List contributors
- `/listschools` — List schools

The bot updates `schools.json` and `contributors.json` in your GitHub repo. 