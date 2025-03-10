import os
import pickle
import base64
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText

# 🔹 Set up Google Gemini AI API Key (Ensure this is correct!)
GOOGLE_GEMINI_API_KEY = "enter your Gemini AI API key"  
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

# 🔹 Gmail API Scopes (Updated with gmail.send)
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send"
]

# ✅ Authenticate & get Gmail token
def authenticate_gmail():
    creds = None

    # Remove old token if permissions were incorrect
    if os.path.exists("token.pickle"):
        os.remove("token.pickle")

    # Authenticate with new scopes
    flow = InstalledAppFlow.from_client_secrets_file("/Users/krushiluchadadia/Downloads/client_secret_184004885695-55bohi8kitvcgg3olitd30mee986cksv.apps.googleusercontent.com.json", SCOPES)
    creds = flow.run_local_server(port=0)

    # Save token for future use
    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)

    return creds

# ✅ Generate AI-based Reply using Gemini API
def generate_ai_reply(subject, body):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")  # ✅ Fixed model name
        prompt = f"Generate a polite and professional reply to this email:\n\nSubject: {subject}\n\nMessage: {body}"
        
        response = model.generate_content(prompt)  # ✅ Corrected function call

        if response and hasattr(response, "text"):
            return response.text  # Extract AI-generated text
        else:
            return "I'm sorry, but I couldn't generate a response."

    except Exception as e:
        print(f"❌ AI Response Error: {e}")
        return "I'm currently unable to generate a response."

# ✅ Send an Email Reply
def send_email_reply(service, recipient_email, subject, message_body):
    try:
        message = MIMEText(message_body)
        message["to"] = recipient_email
        message["subject"] = f"Re: {subject}"
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        send_request = {"raw": encoded_message}
        service.users().messages().send(userId="me", body=send_request).execute()
        print(f"✅ Auto-reply sent to {recipient_email}")

    except HttpError as error:
        print(f"❌ Error sending reply: {error}")

# ✅ Read Unread Emails and Reply Automatically
def read_and_reply_emails():
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)

    try:
        # Get unread emails
        results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread").execute()
        messages = results.get("messages", [])

        if not messages:
            print("📩 No new unread emails.")
            return

        print(f"📬 {len(messages)} new emails found.")

        for msg in messages:
            email_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
            headers = email_data["payload"].get("headers", [])
            sender, subject = "Unknown", "No Subject"
            body = "No content available."

            # Extract sender & subject
            for header in headers:
                if header["name"] == "From":
                    sender = header["value"]
                if header["name"] == "Subject":
                    subject = header["value"]

            # Extract email body (handling missing parts)
            payload = email_data["payload"]
            if "parts" in payload:
                for part in payload["parts"]:
                    if part["mimeType"] == "text/plain" and "data" in part["body"]:
                        body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                        break
                    elif part["mimeType"] == "text/html" and "data" in part["body"]:
                        body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                        break

            print(f"\n📌 From: {sender}")
            print(f"📌 Subject: {subject}")
            print(f"📜 Message: {body[:300]}...")  # Show first 300 characters

            # ✅ Generate AI reply
            ai_reply = generate_ai_reply(subject, body)

            # ✅ Send AI-generated reply
            send_email_reply(service, sender, subject, ai_reply)

            # ✅ Mark email as read after replying
            service.users().messages().modify(userId="me", id=msg["id"], body={"removeLabelIds": ["UNREAD"]}).execute()

    except HttpError as error:
        print(f"❌ Error: {error}")

# ✅ Run the script
if __name__ == "__main__":
    read_and_reply_emails()
