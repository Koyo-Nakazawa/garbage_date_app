from config import Areas, GarbageTyeps, CollectionTypes


def delete_all_data():
    q = Areas.delete()
    q.execute()
    q = GarbageTyeps.delete()
    q.execute()
    q = CollectionTypes.delete()
    q.execute()


if __name__ == "__main__":
    delete_all_data()
