from config import Areas, GarbageTyeps, CollectionTypes
import datetime
from zoneinfo import ZoneInfo
import pytz


def display_all_area():
    areas = Areas.select()
    for area in areas:
        print(area.area_id, area.area_name, area.collection_type_id)


def display_all_garbage_type():
    garbage_types = GarbageTyeps.select()
    for garbage_type in garbage_types:
        print(garbage_type.garbage_type_id, garbage_type.garbage_type_name)


def display_all_collection_type():
    collection_types = CollectionTypes.select()
    cnt = 0
    jst = pytz.timezone('Asia/Tokyo')
    for collection_type in collection_types:
        cnt += 1
        date = collection_type.collection_date
        print(
            collection_type.collection_type_id,
            collection_type.garbage_type_id,
            # collection_type.collection_date,
            jst.localize(date)
        )
        if cnt >= 10:
            break


# 向こう一週間のごみ収集データの取得 リストで返す
def output_collection_data(current_area):
    join_cond = CollectionTypes.collection_type_id == Areas.collection_type_id

    today = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    # today = datetime.datetime.now()
    today = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
    print(f"today:{today}")
    # jst = pytz.timezone('Asia/Tokyo')
    # today = jst.localize(today)
    date_after_one_week = today + datetime.timedelta(days=7)
    where_cond = (
        (Areas.area_name == current_area)
        & (CollectionTypes.collection_date.between(today, date_after_one_week))
        # & (CollectionTypes.collection_date <= (today + datetime.timedelta(days=7)))
    )

    collection_dates = (
        CollectionTypes.select()
        .join(Areas, on=join_cond)
        .objects(constructor=CollectionTypes)
        .where(where_cond)
    )

    # return collection_dates
    # for data in collection_dates:
    #     print(
    #         data.collection_date.strftime("%m/%d %a"),
    #         GarbageTyeps.get_by_id(data.garbage_type_id).garbage_type_name,
    #     )
    result = []
    day_names = ["月", "火", "水", "木", "金", "土", "日"]
    # jst = pytz.timezone('Asia/Tokyo')
    for data in collection_dates:
        # print(data.collection_date)
        # date = data.collection_date.astimezone(jst)
        date = data.collection_date
        print(date)
        date = date + datetime.timedelta(hours=9)
        print(date)
        # print(date.weekday())
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
    # print(areas.count())
    # for area in areas:
    #     print(area.area_id, area.area_name, area.collection_type_id)
    result = []
    for area in areas:
        result.append([area.area_id, area.area_name, area.collection_type_id])
    return result


if __name__ == "__main__":
    # display_all_area()
    # display_all_garbage_type()
    # display_all_collection_type()
    # collection_data = output_collection_data("箱清水一")
    # print(collection_data)
    # test()
    # print(get_candidate_area("箱清水"))
    # print(output_collection_data("箱清水一～二丁目"))
    display_all_collection_type()
