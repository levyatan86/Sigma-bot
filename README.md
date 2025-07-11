🤖 Sigma Bot – Your AI Trading Assistant
Sigma is your all-in-one AI-powered trading assistant built to help track, score, and manage trades with surgical precision — across Telegram, Google Sheets, Notion, and TradingView.

🚀 Features
📲 Telegram Integration – Control Sigma with chat commands like /log, /alert, /status
📈 Webhook Listener – Accepts TradingView signals and scores trades in real-time
📊 Google Sheets Sync – Logs all trades with R:R, emotion, session, and performance data
🧠 Radar Scoring Engine – Evaluates trade quality using volume, pattern, trend, and structure
🧾 Notion Strategy Dashboard – Tracks live strategy performance and flags playbook candidates
📦 Folder Structure
Sigma-bot/ │ ├── Sigma_bot.py # Telegram bot logic ├── webhook_listener.py # Webhook for TradingView alerts ├── sheets_integration.py # Logs trades to Google Sheets ├── radar_score.py # Scoring engine (pattern + volume logic) ├── requirements.txt # Python dependencies ├── Procfile # Railway deployment file ├── .gitignore # Ignores secrets like credentials.json ├── credentials.json # 🔒 NOT INCLUDED – use locally ├── notion.env # Your Notion API keys

⚙️ Commands
In Telegram:

/start – Launch the bot
/status – Get current system status
/log – Log a trade manually
/alert – Set a price alert (/alert btc 50000)
/alerts – Show active alerts
/removealert – Remove an alert
🧠 Strategy Engine
Trades are automatically scored based on:

✅ Trend alignment
📉 Pattern confirmation
🔁 Liquidity sweeps
🧱 Order blocks & structure
🔊 Volume profile
Each trade gets a score out of 10 and is stored in Google Sheets & Notion.

🔐 Security Notice
This repo no longer includes sensitive files (like credentials.json).
Make sure to create a local credentials.json if needed and never push it!

💡 Roadmap
 Telegram + webhook bot
 Real-time trade scoring
 Google Sheets integration
 Auto backtesting module
 Strategy evolution tracking
 Risk dashboard
🛠 Built With
Python 3.11+
FastAPI
python-telegram-bot
Google Sheets API
Notion API
TradingView Webhook
🧙‍♂️ Created By
Levente Kacso
aka Levyatan86 – always seeking that perfect entry.

⚡ Trade smarter. Evolve your edge. Sigma watches the charts so you don't have to.
