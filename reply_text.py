import datetime


def create_candidate_area_reply(areas):
    result = ""
    cnt = 1
    for area in areas:
        result += f"{str(cnt)}. {area['area_name']}"
        cnt += 1
    return result


def create_collection_dates_types_reply(date_list, collection_data):
    result_list = []
    for date in date_list:
        for data in collection_data:
            if data["collection_date"] == date:
                result_list.append(f" {data['garbage_type_name']}")
            else:
                pass
    return result_list


# 日付の処理
def test():
    days = []
    today = datetime.datetime.now()
    days.append(today.strftime("%Y%m%d %a"))
    for i in range(1, 8):
        next_date = datetime.datetime.strptime(days[i - 1], "%Y%m%d %a") + datetime.timedelta(days=1)
        days.append(next_date.strftime("%Y%m%d %a"))

    print(days)
