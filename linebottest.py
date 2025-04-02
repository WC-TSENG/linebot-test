from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi('2EJtlrv04R4wBMSgFojkdOvJHbVhawiW/58Nb7oXaDU1usOT93DSNnbvrjoz7zWHd+pM3wTJKGRSeSfmbOV800Ldb9S8rwBdiXkRWZyfgwKNLo4jNFVDgBreSaVVQOMmkerV+YWrtpZCsB7E3RrnfQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('685f61fbe19391266373fa109672b812')

@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_json()
    user_message = json_data['events'][0]['message']['text']
    reply_text = f"收到你的訊息：{user_message}"
    line_bot_api.reply_message(
        json_data['events'][0]['replyToken'],
        TextSendMessage(text=reply_text)
    )
    return 'OK', 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)