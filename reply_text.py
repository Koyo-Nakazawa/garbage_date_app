import datetime
from config import GarbageTyeps
from read import get_candidate_area, output_collection_data


def create_candidate_area_reply(keyword):
    candidate_areas = get_candidate_area(keyword)
    # cnt = candidate_areas.count()
    result = []
    for index, area in enumerate(candidate_areas):
        print(index + 1, area.area_name)
        result.append([index + 1, area.area_name])
    return result


def create_collection_dates_types_reply(current_area):
    collection_data = output_collection_data(current_area)
    days_one_week = get_days_one_week()
    for day in days_one_week:
        if day in collection_data.collection_data:
            print('yes')
    # for data in collection_data:
    #     if data.collection_date.strftime("%m/%d %a") in days_one_week:
    #         print(
    #             data.collection_date.strftime("%m/%d %a"),
    #             GarbageTyeps.get_by_id(data.garbage_type_id).garbage_type_name,
    #         )
    #     else:
    #         pass


# 向こう一週間の日付をリストで返すもの
def get_days_one_week():
    days = []
    today = datetime.datetime.now()
    days.append(today.strftime("%Y%m%d %a"))
    for i in range(1, 8):
        next_date = datetime.datetime.strptime(days[i - 1], "%m/%d %a") + datetime.timedelta(days=1)
        days.append(next_date.strftime("%m/%d %a"))

    # print(days)
    return days


if __name__ == "__main__":
    candidate_areas = create_candidate_area_reply("箱")
    current_area_index = int(input("該当する地域を番号で指定してください : "))
    current_area = candidate_areas[current_area_index - 1][1]
    create_collection_dates_types_reply(current_area)
