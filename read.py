from config import Areas, GarbageTyeps, CollectionTypes
import datetime


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
    for collection_type in collection_types:
        print(
            collection_type.collection_type_id,
            collection_type.garbage_type_id,
            collection_type.collection_date,
        )


def output_collection_data(current_area):
    join_cond = CollectionTypes.collection_type_id == Areas.collection_type_id

    today = datetime.datetime.now()
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
    for data in collection_dates:
        print(data.collection_date, GarbageTyeps.get_by_id(data.garbage_type_id).garbage_type_name)


# 日付の処理
def test():
    days = []
    today = datetime.datetime.now()
    days.append(today.strftime("%Y%m%d %a"))
    for i in range(1, 8):
        next_date = datetime.datetime.strptime(days[i - 1], "%Y%m%d %a") + datetime.timedelta(days=1)
        days.append(next_date.strftime("%Y%m%d %a"))

    print(days)


if __name__ == "__main__":
    # display_all_area()
    # display_all_garbage_type()
    # display_all_collection_type()
    collection_data = output_collection_data("箱清水")
    # test()
