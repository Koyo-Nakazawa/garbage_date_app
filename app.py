import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    LocationMessage,
    TextSendMessage,
    QuickReplyButton,
    QuickReply,
    MessageAction,
    ImageMessage,
    LocationAction,
    TemplateSendMessage,
    CarouselTemplate,
    CarouselColumn,
    PostbackAction,
    CarouselTemplate,
    URIAction,
)
from dotenv import load_dotenv
from read import get_candidate_area, output_collection_data

load_dotenv(override=True)

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])


@app.route("/")
def index():
    return "You call index()"


@app.route("/callback", methods=["POST"])
def callback():
    """Messaging APIからの呼び出し関数"""
    # LINEがリクエストの改ざんを防ぐために付与する署名を取得
    signature = request.headers["X-Line-Signature"]
    # リクエストの内容をテキストで取得
    body = request.get_data(as_text=True)
    # ログに出力
    app.logger.info("Request body: " + body)

    try:
        # signature と body を比較することで、リクエストがLINEから送信されたものであることを検証
        handler.handle(body, signature)
    except InvalidSignatureError:
        # クライアントからのリクエストに誤りがあったことを示すエラーを返す
        abort(400)

    return "OK"


# たぶんこの関数をがしがしいじっていく感じだと思われる。
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
    if event.message.text == "ごみ":
        # sessions[event.source.user_id]["flag"]=True
        candidate_areas = get_candidate_area("園")
        items = [
            QuickReplyButton(action=MessageAction(text=f"{area[1]}", label=f"{area[1]}"))
            for area in candidate_areas
        ]
        # クイックリプライオブジェクトを作成
        messages = TextSendMessage(text="地区を選択してください", quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
