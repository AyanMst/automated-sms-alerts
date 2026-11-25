# Automated SMS Alerts

A small automation that generates a fresh motivational message with Google Gemini every morning and delivers it to your phone through Twilio (WhatsApp).

## Overview

Every day at a scheduled time, a GitHub Actions workflow runs a Python script. The script asks Gemini to write a short, direct stoic-style message and sends it to a configured phone number via the Twilio API. No server is required.

## How It Works

```
GitHub Actions (cron) -> bot.py -> Gemini API (generate text) -> Twilio API -> WhatsApp
```

1. The workflow in `.github/workflows/main.yml` triggers daily at 04:15 UTC (or manually via *Run workflow*).
2. `bot.py` loads its configuration from environment variables.
3. Gemini (`gemini-2.5-flash`) generates the message from a prompt.
4. Twilio delivers the message to the recipient.

## Tech Stack

- Python 3.10+
- Google Generative AI SDK (Gemini)
- Twilio Python SDK (WhatsApp messaging)
- python-dotenv
- GitHub Actions

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GOOGLE_API_KEY` | Gemini API key from Google AI Studio |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token |
| `TWILIO_FROM_NUMBER` | Sender, e.g. `whatsapp:+14155550100` (Twilio sandbox or approved number) |
| `TWILIO_TO_NUMBER` | Recipient, e.g. `whatsapp:+15555550123` |

Copy the template and fill in your own values:

```bash
cp .env.example .env
```

`.env` is git-ignored and must never be committed. For GitHub Actions, add the same five variables as repository secrets (*Settings -> Secrets and variables -> Actions*).

## Local Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit .env
python bot.py
```

Note: with the Twilio WhatsApp sandbox, the recipient must first join the sandbox by sending the join code to the sandbox number.
