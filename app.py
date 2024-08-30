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
from read import get_candidate_area, display_all_area
from reply_text import create_collection_dates_types_reply
from bs4 import BeautifulSoup
import requests
import json

# import time


load_dotenv(override=True)

app = Flask(__name__)


places_api_key = "AIzaSyD1EuDN49A_sbC8-166UB7l7S06yY9ldgw"
places_api_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/"
google_map_url = "https://www.google.com/maps/search/?api=1"


# def find_place_by_geoinfo(latitude, longitude, keyword) -> str:
#     global places_api_url, places_api_key
#     # 半径1km県内の店を取得します
#     places_parameter = f"json?keyword={keyword}&types=food?language=ja&location={latitude},{longitude}&radius=1000&key={places_api_key}"
#     places_api = places_api_url + places_parameter

#     response = requests.get(places_api)
#     soup = BeautifulSoup(response.content)
#     data = json.loads(soup.text)
#     print(data)
#     return data


line_bot_api = LineBotApi(os.environ["ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])
sessions = {}


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


# テキストメッセージを受け取ったときの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ユーザーidをもとにセッションを管理します
    print(sessions)
    print(display_all_area())
    if event.source.user_id not in sessions.keys():
        sessions[event.source.user_id] = {"flag": False, "area": None}

    if event.message.text == "ごみ":
        sessions[event.source.user_id]["flag"] = True
        candidate_areas = get_candidate_area("箱")
        print(candidate_areas)
        print("chage")
        items = [
            QuickReplyButton(action=MessageAction(text=f"{area[1]}", label=f"{area[1]}"))
            for area in candidate_areas
        ]
        # クイックリプライオブジェクトを作成
        messages = TextSendMessage(text="地区を選択してください", quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)
    elif sessions[event.source.user_id]["flag"]:
        sessions[event.source.user_id]["area"] = event.message.text
        message = create_collection_dates_types_reply(sessions[event.source.user_id]["area"])
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))


# 位置情報を受け取ったときの処理
# @handler.add(MessageEvent, message=LocationMessage)
# def handle_location(event):
#     latitude = event.message.latitude
#     longitude = event.message.longitude
#     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"{latitude, longitude}"))
#     print(latitude, longitude)

    # global sessions, google_api_key, google_map_url
    # # セッションで検索する要件( 飲食店の種類, 位置情報 )があるか確認
    # if sessions[event.source.user_id]["flag"] and sessions[event.source.user_id]["food"]:
    #     latitude = event.message.latitude
    #     longitude = event.message.longitude
    #     # thumnailImage
    #     data = find_place_by_geoinfo(
    #         latitude=latitude, longitude=longitude, keyword=sessions[event.source.user_id]["food"]
    #     )
    #     columns = []
    #     # カルーセルメッセージは最大10件までしか表示できない点に注意
    #     for data in range(data["results"][:10]):
    #         try:
    #             photo_reference = data["photos"][0]["photo_reference"]
    #             image_url = get_photoURL(photo_reference)
    #             # shop_name and shop_rating
    #             shop_name = data["name"]
    #             like_num = data["rating"]
    #             place_id = data["place_id"]
    #             user_ratings_total = data["user_ratings_total"]
    #             latitude = data["geometry"]["location"]["lat"]
    #             longitude = data["geometry"]["location"]["lng"]

    #             # 対象の飲食店におけるgooglemapのURLを作成
    #             map_url = google_map_url + f"&query={latitude}%2C{longitude}&quary_place_id={place_id}"
    #             # カルーセルメッセージオブジェクトを作成
    #             carousel = make_carousel(
    #                 thumbnail_image_url=image_url,
    #                 shop_name=shop_name,
    #                 like=like_num,
    #                 user_ratings_total=user_ratings_total,
    #                 map_url=map_url,
    #             )
    #             columns.append(carousel)
    #         except:
    #             continue
    #     # 対象の飲食店が1店舗もない場合の判別
    #     if len(columns) >= 1:
    #         message = TextSendMessage(text="近くにこんなお店があるみたい")
    #         line_bot_api.reply_message(event.reply_token, message)
    #         carousel_template_message = TemplateSendMessage(
    #             alt_text="Carousel template", template=CarouselTemplate(columns=columns)
    #         )
    #         time.sleep(0.4)
    #         line_bot_api.push_message(event.source.user_id, carousel_template_message)
    #     else:
    #         message = TextSendMessage(text="1km以内に候補が見つかりませんでした")
    #         line_bot_api.reply_message(event.reply_token, messages=mssage)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
