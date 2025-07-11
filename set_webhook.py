import requests

BOT_TOKEN = "7801292141:AAEzpCBio2BgOEFk575NurAwGaTfeaqC33U"
RAILWAY_URL = "https://web-production-f3f69.up.railway.app/telegram"

response = requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    params={"url": RAILWAY_URL}
)

print(response.json())
