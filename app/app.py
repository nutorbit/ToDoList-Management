from helper import getIntent
from constants import API_KEY, SECRET
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)
line_bot_api = LineBotApi(API_KEY)
handler = WebhookHandler(SECRET)
state = None
todo = []  # TODO: add to firebase


@app.route('/')
def home():
    return "hello"


@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global state
    text = event.message.text
    reply_token = event.reply_token

    intent = getIntent(text)

    # if state has assigned, we need to get answer from user
    if state != None:
        if state == 'createTask':
            todo.append(text)
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text=f'จำให้เรียบร้อย'))
        if state == 'clearTask':
            try:
                todo.remove(text)
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text=f'ลบให้แล้ว'))
            except:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text=f'หาไม่เจอ'))
        state = None
    else:  # assign state
        state = intent

        if state == 'createTask':
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text=f'อยากให้ช่วยจำอะไร'))
        if state == 'displayTask':
            if len(todo) == 0:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text=f"ไม่มีอะไรต้องทำ"))
            else:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text=f"{', '.join(todo)}"))

            state = None
        if state == 'clearTask':
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text=f"เหลือสิ่งนี้ให้ทำ\n{', '.join(todo)}\nทำอันไหนเสร็จแล้ว"))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
