import datetime

# from config import GarbageTyeps
from read import get_candidate_area, output_collection_data


# 候補地をindex付で出力する
def create_candidate_area_reply(keyword):
    candidate_areas = get_candidate_area(keyword)
    # cnt = candidate_areas.count()
    result = []
    for index, area in enumerate(candidate_areas):
        print(index + 1, area[1])
        result.append([index + 1, area[1]])

    return result


# 確定された地区の向こう一週間の収集ごみを
def create_collection_dates_types_reply(current_area):
    collection_data = output_collection_data(current_area)
    days_one_week = get_days_one_week()
    # print(collection_data)
    # print(days_one_week)
    for data in collection_data:
        if data[0] in days_one_week:
            if days_one_week[data[0]] == "なし":
                days_one_week[data[0]] = f"{data[1]}"
            else:
                days_one_week[data[0]] += f" {data[1]}"

    for i, v in enumerate(days_one_week.items()):
        print(f"{v[0]}  {v[1]}")
        if i == 0:
            print(f"{'-'*8}今後の予定{'-'*8}")


# 向こう一週間の日付をキーとした辞書を返すもの
def get_days_one_week():
    day_names = ["日", "月", "火", "水", "木", "金", "月"]
    days = {}
    today = datetime.datetime.now()
    days[f"{today.strftime('%m/%d')} ({day_names[int(today.strftime('%w'))]})"] = "なし"
    for i in range(1, 8):
        next_date = today + datetime.timedelta(days=i)
        days[f"{next_date.strftime('%m/%d')} ({day_names[int(next_date.strftime('%w'))]})"] = "なし"

    # print(days)
    return days


if __name__ == "__main__":
    candidate_areas = create_candidate_area_reply("箱")
    current_area_index = int(input("該当する地域を番号で指定してください : "))
    current_area = candidate_areas[current_area_index - 1][1]
    create_collection_dates_types_reply(current_area)
