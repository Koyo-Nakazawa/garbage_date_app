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
                

    return result
