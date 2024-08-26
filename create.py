from config import Areas, GarbageTyeps, CollectionTypes
import datetime


# 地区テーブルのデータ作成
def create_area(area_name, collection_type_id):
    Areas.create(area_name=area_name, collection_type_id=collection_type_id)


# ごみ種別テーブルのデータ作成
def create_gabage_type(garbage_type_name):
    GarbageTyeps.create(garbage_type_name=garbage_type_name)


# 収集種別テーブルのデータ作成
def create_collection_type(collection_type_id, garbage_type_id, collection_date):
    CollectionTypes.create(
        collection_type_id=collection_type_id,
        garbage_type_id=garbage_type_id,
        collection_date=collection_date,
    )


if __name__ == "__main__":
    create_area("箱清水", 1)
    create_gabage_type("可燃ごみ")
    create_collection_type(1, 1, datetime.date(2024, 8, 26))
