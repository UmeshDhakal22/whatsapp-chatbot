from fastapi import FastAPI, Query, Request, HTTPException
import requests
import json

app = FastAPI()
ACCESS_TOKEN = "EAATlgAY524cBO6KRr2fR0bsphIALT2TZB0ZA0fGqIiFTt0cdqcsAzXfOM1HvyzbPOjldHhDiqZCAE5lHCZCxOZB0YirZAEORBoNv1OeTieqf5bwsZB4zhxJZBveQQttXlJG6ZBZC9NBUDHglCVwGyacUtAgwp7DiznglZAvNyUYNOiDZAY1M1tHQsmFt0aZC4vSXHjZC4HeLQz7IJp5muAZARkpEYO1ZAj0aQ5BUQIljcyFUKhuGTosZD"
PHONE_NUMBER_ID = "631702670020212"
VERIFY_TOKEN = "my_secret"

@app.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        print("✅ Webhook verified.")
        return int(hub_challenge)
    print("❌ Webhook verification failed.")
    return {"error": "Invalid verification token"}

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or empty JSON body")

    for entry in body.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            messages = value.get("messages", [])
            for message in messages:
                try:
                    sender = message["from"]
                    text = message.get("text", {}).get("body", "")
                    if text:
                        send_message(sender, f"You said: {text}")
                except Exception as e:
                    print("⚠️ Error processing message:", e)
    return {"status": "ok"}

def send_message(recipient, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("❌ Failed to send message")
