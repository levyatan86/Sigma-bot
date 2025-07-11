import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_notion_card(pair, direction, entry, sl, tp1, tp2, score, emotion, notes):
    url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "Trade Pair": { "title": [{ "text": { "content": pair } }] },
            "Direction": { "select": { "name": direction.lower() } },
            "Entry Price": { "number": float(entry) },
            "Stop Loss": { "number": float(sl) },
            "Take Profit(s)": { "rich_text": [{ "text": { "content": f"TP1: {tp1}, TP2: {tp2}" } }] },
            "Radar Score": { "number": float(score) },
            "Emotion Tag": { "select": { "name": emotion } },
            "Notes": { "rich_text": [{ "text": { "content": notes } }] },
            "Timestamp": { "date": { "start": datetime.utcnow().isoformat() } },
            "Strategy Status": { "select": { "name": "Playbook" } }
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        print("❌ Notion card creation failed:", response.text)
    else:
        print("✅ Notion card created successfully.")
