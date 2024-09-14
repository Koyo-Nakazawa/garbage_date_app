import datetime
from read import output_collection_data


# 向こう一週間の日付をキーとした辞書を返すもの
def get_days_one_week():
    day_names = ["日", "月", "火", "水", "木", "金", "土"]
    days = {}
    today = datetime.datetime.now()
    days[f"{today.strftime('%m/%d')} ({day_names[int(today.strftime('%w'))]})"] = "なし"
    for i in range(1, 8):
        next_date = today + datetime.timedelta(days=i)
        days[f"{next_date.strftime('%m/%d')} ({day_names[int(next_date.strftime('%w'))]})"] = "なし"

    return days


# 確定された地区の向こう一週間の収集ごみを返す
def create_collection_dates_types_reply(current_area):
    collection_data = output_collection_data(current_area)
    days_one_week = get_days_one_week()
    # data[0]->日付, data[1]->ごみ種別
    for data in collection_data:
        if data[0] in days_one_week:
            if days_one_week[data[0]] == "なし":
                days_one_week[data[0]] = f"{data[1]}"
            else:
                days_one_week[data[0]] += f"\n{' '*21}{data[1]}"

    result = f"\n{'-'*5}今日の収集ごみ{'-'*31}\n\n"
    for i, v in enumerate(days_one_week.items()):
        result += f"{v[0]}  {v[1]}\n"
        if i == 0:
            result += f"\n{'-'*5}今後の予定{'-'*37}\n\n"

    return result


if __name__ == "__main__":
    pass
