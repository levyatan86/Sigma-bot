import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.DEBUG
)

import logging
import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Dictionary to store alerts
price_alerts = {}

async def set_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper()
        price = float(context.args[1])

        user_id = update.effective_user.id
        if user_id not in price_alerts:
            price_alerts[user_id] = {}
        price_alerts[user_id][symbol] = price

        await update.message.reply_text(f"✅ Alert set for {symbol} at ${price:.2f}")
    except Exception as e:
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
    except Exception:
        await update.message.reply_text("❌ Usage: /removealert SYMBOL")

async def show_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    alerts = price_alerts.get(user_id, {})
    if not alerts:
        await update.message.reply_text("🔕 No active alerts.")
        return

    msg = "🔔 Your alerts:\n"
    for symbol, price in alerts.items():
        msg += f"• {symbol}: ${price:.2f}\n"

    await update.message.reply_text(msg)

# Import or define your sheet-logging function here
# from your_logging_module import log_trade_to_sheet
# Global dictionary to store price alerts
price_alerts = {}  # Format: {user_id: {"XRP": 2.36135, "BTC": 110000}}

token = "7801292141:AAEzpCBio2BgOEFk575NurAwGaTfeaqC33U"  # Replace with your actual token

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("👋 Sigma is online!")

    # Second message explaining next steps
    await update.message.reply_text("Use /log to log a trade or /status to check bot health.")
    

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Sigma is running smoothly!")

async def log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    parts = context.args
    if len(parts) < 10:
        return await update.message.reply_text(
            "⚠️ Usage:\n"
            "/log <PAIR> <DIRECTION> <ENTRY> <SL> <TP1> <TP2> <SESSION> <NOTES> <EMOTION> <SCORE>\n"
            "Example:\n"
            "/log BTC/USDT long 30000 29500 31000 32000 NY MF_spike 8.5"
        )

    # ...rest of your parsing logic here...

    try:
        pair      = parts[0]
        direction = parts[1].lower()
        entry     = float(parts[2])
        sl        = float(parts[3])
        tp1       = float(parts[4])
        tp2       = float(parts[5])
        session   = parts[6]
        notes     = parts[7]
        emotion   = parts[8]
        score     = float(parts[9])
    except ValueError as e:
        logger.error("Numeric parse error: %s", e)
        return await update.message.reply_text(f"❌ Numeric parse error: {e}")
    except Exception as e:
        logger.exception("Unexpected error parsing arguments")
        return await update.message.reply_text(f"❌ Error parsing arguments: {e}")

    # Confirmation message
    await update.message.reply_text(
        f"📘 Trade logged:\n"
        f"Pair: {pair}\n"
        f"Direction: {direction}\n"
        f"Entry: {entry}\n"
        f"SL: {sl}\n"
        f"TP1: {tp1}\n"
        f"TP2: {tp2}\n"
        f"Session: {session}\n"
        f"Notes: {notes}\n"
        f"Emotion: {emotion}\n"
        f"Score: {score}"
    )

    # Log to sheet
    try:
        log_trade_to_sheet(
            pair=pair,
            direction=direction,
            entry=entry,
            stop_loss=sl,
            tp1=tp1,
            tp2=tp2,
            session=session,
            notes=notes,
            emotion=emotion,
            score=score
        )
        await update.message.reply_text("✅ Successfully logged to sheet.")
    except Exception as e:
        logger.error("Failed to log to sheet: %s", e)
        await update.message.reply_text(f"❌ Failed to log to sheet: {e}")

def main():
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("log", log))
    app.add_handler(CommandHandler("alert", set_alert))
    app.add_handler(CommandHandler("removealert", remove_alert))
    app.add_handler(CommandHandler("alerts", show_alerts))

    logger.info("🚀 Sigma bot initialized...")

    # Start background price watcher
    import asyncio
    asyncio.create_task(price_watcher(app))

async def price_watcher(app):
    await asyncio.sleep(5)  # Delay before starting
    while True:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "https://api.coingecko.com/api/v3/simple/price",
                    params={
                        "ids": "bitcoin,ripple,ethereum",
                        "vs_currencies": "usd"
                    }
                )
                data = response.json()
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
                print(f"⚠️ Price watcher error: {e}")

        await asyncio.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
