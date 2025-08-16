# **Webhook Notification POC with Supabase, Streamlit, FastAPI & Discord**

Overview:
* Sign up / log in using Supabase email authentication
* Type and send a message from a Streamlit frontend
* Store and process the message using a FastAPI backend
* Send a Discord webhook notification with the message content
* Also inlcuded sentiment analysis which shows if the message is positive/negative/neutral

This showcases basic user authentication, API communication, and Discord notifications — all with minimal setup.

Tech Stack:
Layer	           Tool	                    Purpose
Frontend	       Streamlit	              UI for login and message input
Backend	         FastAPI	                Receives and processes message
Auth & DB	       Supabase	                Email/password auth & user table
Notification	   Discord Webhook	        Receives real-time alerts
Environment	     Python (.env)	          To store secrets and keys

Project Structure:
webhooknotify

│

├── backend/

│   ├── main.py               # FastAPI backend (receives messages), Discord webhook sender

│   └── requirements.txt      # Backend dependencies

│

├── frontend/

│   ├── app.py                # Streamlit app (UI and logic)

│   └── requirements.txt      # Frontend dependencies

│

├── .env                      # Secrets (Supabase & Discord)

└── README.md                 # This file



How It Works:
User opens the frontend (app.py)
They sign up or log in via Supabase
They type a message and hit "Send"
The frontend sends that message (with email) to FastAPI via POST /send
FastAPI uses a Discord webhook to send the message to a server channel
The message appears as a notification in Discord


.env Setup (Secrets):
Create a .env file in the root directory (same level as frontend and backend) and add the following:
# Supabase project
SUPABASE_URL=https://your-project-id.supabase.co

SUPABASE_ANON_KEY=your-anon-key

# Discord webhook URL
DISCORD_WEBHOOK=https://discord.com/api/webhooks/...


How to Run:
1. Clone the repo
>git clone <repo-url>
cd webhooknotify

Backend:
>cd backend
>pip install -r requirements.txt

Frontend:
>cd ../frontend
>pip install -r requirements.txt

2. Run the backend server
>cd backend
>uvicorn main:app --reload
This will start the FastAPI backend on http://localhost:8000

3. Run the frontend (Streamlit UI)
Open a new terminal:
>cd frontend
>streamlit run app.py
This will open your app at http://localhost:8501

4. Try It Out!
Sign up or log in with an email and password.
Type a message and hit Send.
The message will go to Discord instantly!
