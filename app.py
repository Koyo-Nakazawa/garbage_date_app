import os
from flask import Flask, request, abort, render_template, url_for
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
    ImageSendMessage,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    ImagemapSendMessage,
    BaseSize,
    URIImagemapAction,
    ImagemapArea,
)
from dotenv import load_dotenv
from read import get_candidate_area, output_collection_data
from reply_text import create_collection_dates_types_reply
import time

load_dotenv(override=True)

app = Flask(__name__)


line_bot_api = LineBotApi(os.environ["ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])
sessions = {}
garbage_type_images = {
    "可燃ごみ": ["可燃ごみ", "kanengomi.png"],
    "スプレー缶・カセットボンベ": ["スプレー缶等", "spraycan.png"],
    "プラスチックごみ": ["プラごみ", "plastic.png"],
    "不燃ごみ": ["不燃ごみ", "hunengomi.png"],
    "びん・カン・ペットボトル": ["びんカンペット", "bincan.png"],
    "古紙": ["古紙", "koshi.png"],
}


def make_image_carousel(image_uri, garbage_name):
    column = ImageCarouselColumn(
        image_url=image_uri,
        action=URIAction(
            label=garbage_name,
            uri=image_uri,
        ),
    )
    return column


@app.route("/")
def index():
    test = create_collection_dates_types_reply("箱清水一～二丁目").split("\n")
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
    if event.source.user_id not in sessions.keys():
        sessions[event.source.user_id] = {"flag": False, "first": True, "area": None}

    # 受け取ったメッセージが「ごみ」のとき
    if event.message.text == "ごみ":
        sessions[event.source.user_id]["flag"] = True

        # 初回であれば、エリア特定のやりとりをする
        if sessions[event.source.user_id]["first"]:
            message = "町名を入力してください（初回のみ）"
            text_message = TextSendMessage(text=message)
            line_bot_api.reply_message(event.reply_token, text_message)

        # 初回でなければ、収集日の情報を返信する
        else:
            message = create_collection_dates_types_reply(sessions[event.source.user_id]["area"])
            text_message = TextSendMessage(text=message)
            collection_data = output_collection_data(sessions[event.source.user_id]["area"])
            garbage_type_names = map(lambda x: x[1], collection_data)
            cnt = 0
            registered_list = []
            columns = []
            for garbate_type_name in garbage_type_names:
                if cnt > 3:
                    break
                images_data = garbage_type_images[garbate_type_name]
                if images_data[0] not in registered_list:
                    columns.append(
                        make_image_carousel(
                            f"https://garbage-date-app.onrender.com/static/images/{images_data[1]}",
                            images_data[0],
                        )
                    )
                    registered_list.append(images_data[0])
                    cnt += 1
            image_carousel_template = ImageCarouselTemplate(columns=columns)
            template_message = TemplateSendMessage(alt_text=message, template=image_carousel_template)
            line_bot_api.reply_message(event.reply_token, [template_message, text_message])

    # 受け取ったメッセージが「ごみ」以外のとき
    # 初回の町名を受け取ったとき
    elif sessions[event.source.user_id]["first"]:
        candidate_areas = get_candidate_area(event.message.text)
        if candidate_areas:
            sessions[event.source.user_id]["first"] = False
            items = [
                QuickReplyButton(action=MessageAction(text=f"{area[1]}", label=f"{area[1]}"))
                for area in candidate_areas
            ]
            # クイックリプライオブジェクトを作成
            messages = TextSendMessage(text="地区を選択してください", quick_reply=QuickReply(items=items))
        else:
            text = "※※※対象外の地域が返信されました※※※"
            text += "\n・都南地区、玉山地区は対象外です。"
            text += "\n・返信した町名が正しいか確認してください。"
            text += "\n　(漢字が違う場合も対象外と判定されてしまいます。)"

            messages = TextSendMessage(text=text)

        line_bot_api.reply_message(event.reply_token, messages=messages)

    # 候補地から地区名を受け取ったとき
    elif sessions[event.source.user_id]["area"] is None:
        sessions[event.source.user_id]["area"] = event.message.text
        message = f"あなたの地区を「{sessions[event.source.user_id]['area']}」に決定しました。\n"
        message += create_collection_dates_types_reply(sessions[event.source.user_id]["area"])
        text_message = TextSendMessage(text=message)
        collection_data = output_collection_data(sessions[event.source.user_id]["area"])
        garbage_type_names = map(lambda x: x[1], collection_data)
        cnt = 0
        registered_list = []
        columns = []
        for garbate_type_name in garbage_type_names:
            if cnt > 3:
                break
            images_data = garbage_type_images[garbate_type_name]
            if images_data[0] not in registered_list:
                columns.append(
                    make_image_carousel(
                        f"https://garbage-date-app.onrender.com/static/images/{images_data[1]}",
                        images_data[0],
                    )
                )
                registered_list.append(images_data[0])
                cnt += 1
        image_carousel_template = ImageCarouselTemplate(columns=columns)
        template_message = TemplateSendMessage(alt_text=message, template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, [template_message, text_message])

    # 地区の変更（引っ越し）
    elif event.message.text == "引っ越し":
        sessions[event.source.user_id]["first"] = True
        sessions[event.source.user_id]["area"] = None
        message = "引っ越し先の町名を入力してください。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
    # 関係ないワードのとき
    else:
        message = "メニューのボタンから選択してください。"
        message += "\n・「収集日確認」（初回のみ地区の選択）"
        message += "\n　向こう一週間のごみ収集予定が返信されます。"
        message += "\n・「引っ越し」"
        message += "\n　引っ越しで住んでいる地区が変わった場合はこちらから変更してください。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    # port = int(os.getenv("PORT", 8000))
    # app.run(port=port, debug=True)
