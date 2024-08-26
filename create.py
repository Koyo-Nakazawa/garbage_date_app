from config import Areas, GarbageTyeps, CollectionTypes
import datetime


# 地区テーブルのデータ作成
def create_area(area_name, collection_type_id):
    Areas.create(area_name=area_name, collection_type_id=collection_type_id)


# ごみ種別テーブルのデータ作成
def create_garbage_type(garbage_type_name):
    GarbageTyeps.create(garbage_type_name=garbage_type_name)


# 収集種別テーブルのデータ作成
def create_collection_type(collection_type_id, garbage_type_id, collection_date):
    CollectionTypes.create(
        collection_type_id=collection_type_id,
        garbage_type_id=garbage_type_id,
        collection_date=collection_date,
    )


if __name__ == "__main__":
    # とりあえず一件ずつ作成する処理は完了
    # CSVを読み込んで一括で作成する処理をあとで追加すること
    areas_data = [
        ["箱清水一丁目", 1],
        ["箱清水二丁目", 1],
        ["高松一丁目", 1],
        ["高松二丁目", 2],
        ["高松三丁目", 2],
        ["上田四丁目", 2],
        ["高松四丁目", 3],
        ["上田一丁目", 3],
        ["上田二丁目", 3]
        ]
    garbage_types_data = [
        "可燃ごみ",
        "スプレー缶・カセットボンベ",
        "プラスチックごみ",
        "不燃ごみ",
        "びん・カン・ペットボトル",
        "古紙"
        ]

    collection_types_data = [
        [1, 1, datetime.date(2024, 8, 26)],
        [1, 2, datetime.date(2024, 8, 27)],
        [1, 3, datetime.date(2024, 8, 27)],
    
        ]
    


    create_area("箱清水", 1)
    create_garbage_type("可燃ごみ")
    create_collection_type(1, 1, datetime.date(2024, 8, 26))
