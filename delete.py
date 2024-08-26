from config import Areas, GarbageTyeps, CollectionTypes

q = Areas.delete()
q.execute()
q = GarbageTyeps.delete()
q.execute()
q = CollectionTypes.delete()
q.execute()
