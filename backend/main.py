from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import httpx
from datetime import datetime

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Allow frontend access
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    email: str
    content: str

# Send message to Discord
async def send_to_discord(user_email, message):
    content = f"*New Message from {user_email}*:\n{message}"
    async with httpx.AsyncClient() as client:
        response = await client.post(WEBHOOK_URL, json={"content": content})
        print("Discord response status:", response.status_code)
        print("Discord response body:", response.text)

@app.post("/send")
async def receive_message(data: Message):
    # Lookup user ID by email from users table
    try:
        print(f"Received message from {data.email}: {data.content}")

        user_response = supabase.table("users").select("id").eq("email", data.email).execute()
        print(f"user_response: {user_response}")
        user_id = user_response.data[0]["id"] if user_response.data else None
        if not user_id:
            print("User not found for email")
            return {"status": "User not found"}

    # Save message to messages table
        insert_response=supabase.table("messages").insert({
        "user_id": user_id,
        "email": data.email,
        "content": data.content,
        "created_at": datetime.utcnow().isoformat()
    }).execute()
        print(f"Insert response: {insert_response}")
        
        # Send message to Discord
        async with httpx.AsyncClient() as client:
            resp = await client.post(WEBHOOK_URL, json={"content": f"*New Message from {data.email}*:\n{data.content}"})
            print(f"Discord response status: {resp.status_code}, body: {await resp.aread()}")

        return {"status": "Message received!"}
    except Exception as e:
        print(f"Exception: {e}")
        return {"error": str(e)}

    """# Send to Discord
    await send_to_discord(data.email, data.content)

    return {"status": "Message received!"}"""

print("Webhook loaded:", WEBHOOK_URL)  # Add this temporarily
