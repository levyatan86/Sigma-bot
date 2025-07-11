from notion_logger import create_notion_card

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Your Google Sheet ID
SHEET_ID = "1SzKXtIOWXX_u02FQyUTK1GauQZt3qXzvWnXUoxWlJM8"

def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1
    return sheet

def log_trade_to_sheet(pair, direction, entry, sl, tp1, tp2, session, notes, emotion, score):
    sheet = get_sheet()
    
    try:
        score_float = float(score)
        flag = "✅ Playbook Candidate" if score_float >= 7.0 else ""
    except:
        score_float = ""
        flag = ""

    row = [
        pair,
        direction,
        entry,
        sl,
        tp1,
        tp2,
        session,
        notes,
        emotion,
        score,
        flag
    ]
    sheet.append_row(row)
    if flag == "✅ Playbook Candidate":
        print("📤 Sending to Notion...")
        create_notion_card(pair, direction, entry, sl, tp1, tp2, score, emotion, notes)

