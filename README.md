 📧 Gmail Auto Reply

A Python script that automatically reads unread emails from your Gmail inbox and sends AI-generated replies using Google's Gemini API.

 🌟 Features

- Authenticates with Gmail API using OAuth2
- Reads unread emails from your inbox
- Generates intelligent, context-aware replies using Google's Gemini 1.5 Pro AI model
- Automatically sends replies to the original sender
- Marks emails as read after processing

 📋 Prerequisites

- Python 3.7 or higher
- Google account with Gmail
- Google Cloud project with Gmail API enabled
- Google Gemini API key

 🛠️ Installation

1. Clone this repository or download the script
2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Set up Google Cloud credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Gmail API
   - Create OAuth credentials (Desktop application)
   - Download the client secret JSON file

4. Get your Google Gemini API key from [Google AI Studio](https://ai.google.dev/)

 ⚙️ Configuration

1. Replace the `GOOGLE_GEMINI_API_KEY` in the script with your actual API key
2. Update the path to your client secret JSON file in the `authenticate_gmail()` function

 🚀 Usage

Run the script to process unread emails and send AI-generated replies:

```bash
python gmail_auto_reply.py
```

The script will:
1. Authenticate with Gmail
2. Retrieve unread emails
3. Generate AI replies using Gemini
4. Send the replies automatically
5. Mark the original emails as read

 🔒 Security Notes

- The script creates a `token.pickle` file for storing your Gmail API credentials
- Ensure your API keys and credentials are kept secure
- Consider using environment variables for sensitive information instead of hardcoding

 🔄 Customization

- Modify the `generate_ai_reply()` function to customize the AI prompt
- Adjust the email filtering in `read_and_reply_emails()` to target specific emails

 🤝 Contributing

Feel free to fork this project and submit pull requests with improvements or bug fixes!

 ⚠️ Limitations

- The script requires internet connectivity
- API rate limits may apply for both Gmail and Gemini APIs
- AI-generated responses may not always be perfectly contextual

 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.