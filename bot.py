"""Daily motivation bot: generates a message with Gemini and sends it via Twilio WhatsApp."""

import os
import sys

import google.generativeai as genai
from dotenv import load_dotenv
from twilio.rest import Client

# ==========================================
# 1. CONFIGURATION (loaded from environment variables)
# ==========================================
# Locally, values are read from a .env file. In GitHub Actions, they come from repository secrets.
load_dotenv()

REQUIRED_VARS = [
    "GOOGLE_API_KEY",
    "TWILIO_ACCOUNT_SID",
    "TWILIO_AUTH_TOKEN",
    "TWILIO_FROM_NUMBER",
    "TWILIO_TO_NUMBER",
]

missing = [name for name in REQUIRED_VARS if not os.environ.get(name)]
if missing:
    sys.exit(f"Missing required environment variables: {', '.join(missing)}")

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
# Phone numbers must keep the "whatsapp:" prefix, e.g. whatsapp:+15555550123
TWILIO_FROM_NUMBER = os.environ["TWILIO_FROM_NUMBER"]
TWILIO_TO_NUMBER = os.environ["TWILIO_TO_NUMBER"]

# ==========================================
# 2. GENERATE THE MESSAGE WITH AI
# ==========================================
print("Generating today's message...")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

PROMPT = (
    "You are a stoic mentor: strict and extremely realistic. Write a single morning "
    "message (to be read at 6:30 AM) that snaps me back to reality. It should be 3-4 "
    "well-developed sentences conveying a deep sense of time passing, the value of "
    "discipline, and the responsibility not to waste today. Be direct, sharp and "
    "slightly uncomfortable, yet deeply motivating through brutal honesty. Avoid cheap "
    "clichés and false optimism. Under no circumstances use emojis. Speak to me as an "
    "adult who must take control of their own life."
)

ai_response = model.generate_content(PROMPT)
message_text = ai_response.text

print(f"Generated message: {message_text}")

# ==========================================
# 3. SEND VIA WHATSAPP
# ==========================================
print("Sending message via WhatsApp...")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

sent_message = client.messages.create(
    from_=TWILIO_FROM_NUMBER,
    body=message_text,
    to=TWILIO_TO_NUMBER,
)

print(f"Success! Message sent (SID: {sent_message.sid}).")
