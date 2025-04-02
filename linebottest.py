from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from transformers import pipeline

app = Flask(__name__)

# 填入你的LINE資訊
line_bot_api = LineBotApi('2EJtlrv04R4wBMSgFojkdOvJHbVhawiW/58Nb7oXaDU1usOT93DSNnbvrjoz7zWHd+pM3wTJKGRSeSfmbOV800Ldb9S8rwBdiXkRWZyfgwKNLo4jNFVDgBreSaVVQOMmkerV+YWrtpZCsB7E3RrnfQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('685f61fbe19391266373fa109672b812')

# 載入distilgpt2模型
generator = pipeline('text-generation', model='distilgpt2')

@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_json()
    user_message = json_data['events'][0]['message']['text']  # 拿到用戶訊息
    
    # 用distilgpt2生成回應
    response = generator(user_message, max_length=50, num_return_sequences=1)
    reply_text = response[0]['generated_text']
    
    # 回傳給LINE用戶
    line_bot_api.reply_message(
        json_data['events'][0]['replyToken'],
        TextSendMessage(text=reply_text)
    )
    return 'OK'

if __name__ == "__main__":
    app.run(port=5000)