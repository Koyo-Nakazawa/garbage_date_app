from config import Areas, GarbageTyeps, CollectionTypes
import datetime
from zoneinfo import ZoneInfo


# 向こう一週間のごみ収集データの取得 リストで返す
def output_collection_data(current_area):
    join_cond = CollectionTypes.collection_type_id == Areas.collection_type_id

    today = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    today = datetime.datetime(today.year, today.month, today.day, 0, 0, 0) - datetime.timedelta(hours=9)
    date_after_one_week = today + datetime.timedelta(days=7, hours=9)
    where_cond = (
        (Areas.area_name == current_area)
        & (CollectionTypes.collection_date.between(today, date_after_one_week))
    )

    collection_dates = (
        CollectionTypes.select()
        .join(Areas, on=join_cond)
        .objects(constructor=CollectionTypes)
        .where(where_cond)
    )

    result = []
    day_names = ["月", "火", "水", "木", "金", "土", "日"]
    # jst = pytz.timezone('Asia/Tokyo')
    for data in collection_dates:
        date = data.collection_date
        # date = data.collection_date.astimezone(jst)
        date = date + datetime.timedelta(hours=9)
        result.append(
            [
                f"{date.strftime('%m/%d')} ({day_names[date.weekday()]})",
                GarbageTyeps.get_by_id(data.garbage_type_id).garbage_type_name,
            ]
        )

    return result


# 候補地の取得 リストで返す
def get_candidate_area(keyword):
    areas = Areas.select().where(Areas.area_name.contains(keyword))
    result = []
    for area in areas:
        result.append([area.area_id, area.area_name, area.collection_type_id])
    return result


if __name__ == "__main__":
    pass
