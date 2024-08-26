from config import Areas, GarbageTyeps, CollectionTypes


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


def output_collection_data():
    join_cond = (CollectionTypes.collection_type_id == Areas.collection_type_id)

    where_cond = (Areas.area_name == "箱清水")

    collection_dates = (
        CollectionTypes.select()
        .join(Areas, on=join_cond)
        .objects(constructor=CollectionTypes)
        .where(where_cond)
    )

    return collection_dates
    # for data in collection_dates:
    #     print(data.collection_date, GarbageTyeps.get_by_id(data.garbage_type_id).garbage_type_name)


if __name__ == "__main__":
    # display_all_area()
    # display_all_garbage_type()
    # display_all_collection_type()
    collection_data = output_collection_data()
    for data in collection_data:
        print(data.collection_date)
