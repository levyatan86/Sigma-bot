# webhook_listener.py
from fastapi import FastAPI, Request
import uvicorn
import logging
import json
from datetime import datetime
from fastapi import FastAPI, Request
from telegram import Update
from sigma_bot import app as telegram_app, price_watcher  # ✅ Sigma Telegram bot + alert watcher
import asyncio

from sheets_integration import log_trade_to_sheet
from radar_score import score_trade

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# ✅ TradingView webhook stays exactly the same
@app.post("/webhook")
async def webhook_endpoint(request: Request):
    data = await request.json()
    logging.info(f"📡 Webhook received: {data}")

    if all(key in data for key in ["pair", "direction", "entry", "sl", "tp1"]):
        try:
            score, reasons = score_trade(data)
            log_trade_to_sheet(
                pair=data["pair"],
                direction=data["direction"],
                entry=float(data["entry"]),
                sl=float(data["sl"]),
                tp1=float(data["tp1"]),
                tp2=float(data.get("tp2", "")),
                session=data.get("session", "Unknown"),
                notes=data.get("notes", ""),
                emotion=data.get("emotion", "neutral"),
                score=str(score)
            )
            logging.info(f"✅ Trade scored {score}/10 based on: {', '.join(reasons)}")
        except Exception as e:
            logging.error(f"❌ Failed to log trade: {e}")
    else:
        with open("webhook_log.txt", "a") as f:
            f.write(f"{datetime.utcnow()} — RAW SIGNAL: {json.dumps(data)}\n")
        logging.info("ℹ️ Basic signal logged.")

    return {"status": "ok"}


# ✅ NEW: Telegram webhook endpoint
@app.post("/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.update_queue.put(update)
    return {"status": "ok"}


# ✅ NEW: Background price watcher
@app.on_event("startup")
async def start_telegram_and_watcher():
    asyncio.create_task(price_watcher(telegram_app))


# ✅ Launch FastAPI server on Railway
if __name__ == "__main__":
    print("🚀 Webhook server running at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
