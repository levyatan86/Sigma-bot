
import logging
import os
import asyncio
import httpx
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
from sheets_integration import log_trade_to_sheet

load_dotenv()
token = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global price alert storage
price_alerts = {}

# Telegram commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Sigma is online!")
    await update.message.reply_text("Use /log to log a trade or /status to check bot health.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Sigma is running smoothly!")

async def log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parts = context.args
    if len(parts) < 10:
        return await update.message.reply_text(
            "⚠️ Usage:\n"
            "/log <PAIR> <DIRECTION> <ENTRY> <SL> <TP1> <TP2> <SESSION> <NOTES> <EMOTION> <SCORE>\n"
            "Example:\n"
            "/log BTC/USDT long 30000 29500 31000 32000 NY MF_spike confident 8.5"
        )
    try:
        pair, direction = parts[0], parts[1].lower()
        entry, sl, tp1, tp2 = map(float, parts[2:6])
        session, notes, emotion, score = parts[6], parts[7], parts[8], float(parts[9])
    except Exception as e:
        logger.exception("Error parsing arguments")
        return await update.message.reply_text(f"❌ Error parsing arguments: {e}")

    try:
        log_trade_to_sheet(pair, direction, entry, sl, tp1, tp2, session, notes, emotion, score)
        await update.message.reply_text("✅ Successfully logged to sheet.")
    except Exception as e:
        logger.error("Failed to log to sheet: %s", e)
        await update.message.reply_text(f"❌ Failed to log to sheet: {e}")

async def set_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper()
        price = float(context.args[1])
        user_id = update.effective_user.id
        price_alerts.setdefault(user_id, {})[symbol] = price
        await update.message.reply_text(f"✅ Alert set for {symbol} at ${price:.2f}")
    except:
        await update.message.reply_text("❌ Usage: /alert SYMBOL PRICE")

async def remove_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper()
        user_id = update.effective_user.id
        if symbol in price_alerts.get(user_id, {}):
            del price_alerts[user_id][symbol]
            await update.message.reply_text(f"✅ Removed alert for {symbol}")
        else:
            await update.message.reply_text(f"⚠️ No alert set for {symbol}")
    except:
        await update.message.reply_text("❌ Usage: /removealert SYMBOL")

async def show_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    alerts = price_alerts.get(user_id, {})
    if not alerts:
        await update.message.reply_text("🔕 No active alerts.")
        return
    msg = "🔔 Your alerts:\n" + "\n".join([f"• {s}: ${p:.2f}" for s, p in alerts.items()])
    await update.message.reply_text(msg)

async def price_watcher(app):
    await asyncio.sleep(5)
    while True:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get("https://api.coingecko.com/api/v3/simple/price", params={
                    "ids": "bitcoin,ripple,ethereum",
                    "vs_currencies": "usd"
                })
                data = res.json()
                current_prices = {
                    "BTC": data["bitcoin"]["usd"],
                    "XRP": data["ripple"]["usd"],
                    "ETH": data["ethereum"]["usd"]
                }
                for user_id, alerts in list(price_alerts.items()):
                    for symbol, target_price in list(alerts.items()):
                        current = current_prices.get(symbol)
                        if current and current >= target_price:
                            await app.bot.send_message(
                                chat_id=user_id,
                                text=f"🚨 {symbol} has reached ${current:.5f} (target: ${target_price:.5f})"
                            )
                            del price_alerts[user_id][symbol]
        except Exception as e:
            logger.error(f"⚠️ Price watcher error: {e}")
        await asyncio.sleep(60)

async def main():
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("log", log))
    app.add_handler(CommandHandler("alert", set_alert))
    app.add_handler(CommandHandler("removealert", remove_alert))
    app.add_handler(CommandHandler("alerts", show_alerts))
    logger.info("🚀 Sigma bot initialized...")
    asyncio.create_task(price_watcher(app))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
