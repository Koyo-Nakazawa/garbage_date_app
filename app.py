import os
from flask import Flask, request, abort, render_template
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
from read import get_candidate_area, display_all_collection_type, output_collection_data
from reply_text import create_collection_dates_types_reply


load_dotenv(override=True)

app = Flask(__name__)


line_bot_api = LineBotApi(os.environ["ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])
sessions = {}


@app.route("/")
def index():
    test = create_collection_dates_types_reply("箱清水一～二丁目").split("\n")
    print(test)
    return render_template("index.html", test=test)


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


# テキストメッセージを受け取ったときの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ユーザーidをもとにセッションを管理します
    display_all_collection_type()
    if event.source.user_id not in sessions.keys():
        sessions[event.source.user_id] = {"flag": False, "first": True, "area": None}

    # 受け取ったメッセージが「ごみ」のとき
    if event.message.text == "ごみ":
        sessions[event.source.user_id]["flag"] = True

        # 初回であれば、エリア特定のやりとりをする
        if sessions[event.source.user_id]["first"]:
            message = "町名を入力してください（初回のみ）"

        # 初回でなければ、収集日の情報を返信する
        else:
            message = create_collection_dates_types_reply(sessions[event.source.user_id]["area"])

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

    # 受け取ったメッセージが「ごみ」以外のとき
    # 初回の町名を受け取ったとき
    elif sessions[event.source.user_id]["first"]:
        sessions[event.source.user_id]["first"] = False
        candidate_areas = get_candidate_area(event.message.text)
        items = [
            QuickReplyButton(action=MessageAction(text=f"{area[1]}", label=f"{area[1]}"))
            for area in candidate_areas
        ]
        # クイックリプライオブジェクトを作成
        messages = TextSendMessage(text="地区を選択してください", quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)
    # 候補地から地区名を受け取ったとき
    elif sessions[event.source.user_id]["area"] is None:
        sessions[event.source.user_id]["area"] = event.message.text
        message = f"あなたの地区を「{sessions[event.source.user_id]['area']}」に決定しました。\n"
        print(sessions[event.source.user_id]['area'])
        message += create_collection_dates_types_reply(sessions[event.source.user_id]["area"])
        # print(create_collection_dates_types_reply(sessions[event.source.user_id]["area"]))
        print(output_collection_data(sessions[event.source.user_id]["area"]))
        # print(message)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

    # 地区の変更（引っ越し）
    elif event.message.text in ["引っ越し", "引越", "引越し", "ひっこし"]:
        sessions[event.source.user_id]["first"] = True
        sessions[event.source.user_id]["area"] = None
        message = "引っ越し先の町名を入力してください。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
    # 関係ないワードのとき
    else:
        message = "ちょっと何言ってるかわかりません。"
        message += "\n・「ごみ」と入力すると、収集日が出力されます。（初回のみ地区の選択）"
        message += "\n・一度選択した地区名を変更する場合は「引っ越し」と入力してください。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))


if __name__ == "__main__":
    # port = int(os.getenv("PORT", 5000))
    # app.run(host="0.0.0.0", port=port)
    port = int(os.getenv("PORT", 8000))
    app.run(port=port, debug=True)
