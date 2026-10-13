import os
import time
import requests

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
raise RuntimeError("BOT_TOKEN Railway Variables ішінде орнатылмаған")

API = f"https://api.telegram.org/bot{TOKEN}"

def send(chat_id, text):
requests.post(
f"{API}/sendMessage",
json={"chat_id": chat_id, "text": text},
timeout=20
).raise_for_status()

def main():
offset = None
print("HysCheckOlymo іске қосылды")

while True:
    try:
        params = {"timeout": 25}
        if offset is not None:
            params["offset"] = offset

        data = requests.get(
            f"{API}/getUpdates",
            params=params,
            timeout=35
        ).json()

        for update in data.get("result", []):
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            chat = msg.get("chat", {})
            chat_id = chat.get("id")
            command = msg.get("text", "").split()[0].lower() if msg.get("text") else ""

            if not chat_id:
                continue

            if command in ("/start", "/help"):
                send(chat_id,
                     "Сәлем! 📊 HysCheckOlymo\n\n"
                     "/status — бот күйі\n"
                     "/about — бот туралы\n\n"
                     "Бұл нұсқа әзірге нақты нарық сигналдарын бермейді.")
            elif command == "/status":
                send(chat_id, "Бот Railway серверінде жұмыс істеп тұр ✅")
            elif command == "/about":
                send(chat_id,
                     "Бұл бот нарық деректерін бақылау және "
                     "техникалық талдауды үйренуге арналған. "
                     "Нақты сауда ашпайды және пайдаға кепілдік бермейді.")
    except Exception as e:
        print("Қате:", e)
        time.sleep(5)

if name == "main":
main()
