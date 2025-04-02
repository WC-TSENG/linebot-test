from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from transformers import pipeline
import os

app = Flask(__name__)

line_bot_api = LineBotApi('2EJtlrv04R4wBMSgFojkdOvJHbVhawiW/58Nb7oXaDU1usOT93DSNnbvrjoz7zWHd+pM3wTJKGRSeSfmbOV800Ldb9S8rwBdiXkRWZyfgwKNLo4jNFVDgBreSaVVQOMmkerV+YWrtpZCsB7E3RrnfQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('685f61fbe19391266373fa109672b812')
generator = pipeline('text-generation', model='uer/gpt2-chinese-cluecorpussmall')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        json_data = request.get_json()
        if not json_data or 'events' not in json_data or not json_data['events']:
            print("No events in webhook request")
            return 'OK', 200
        user_message = json_data['events'][0]['message']['text']
        response = generator(user_message, max_length=50, num_return_sequences=1)
        reply_text = response[0]['generated_text']
        line_bot_api.reply_message(
            json_data['events'][0]['replyToken'],
            TextSendMessage(text=reply_text)
        )
        return 'OK', 200
    except Exception as e:
        print(f"Error: {e}")
        return 'OK', 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)