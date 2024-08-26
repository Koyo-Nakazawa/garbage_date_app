# import datetime
import logging
import os
from dotenv import load_dotenv
from peewee import Model, IntegerField, CharField, TimestampField, ForeignKeyField
from playhouse.db_url import connect

# .envの読み込み
load_dotenv(override=True)

# 実行したSQLをログで出力する設定
# logger = logging.getLogger("peewee")
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)


# データベースへの接続設定
# db = SqliteDatabase("peewee_db.sqlite")  # SQLite固定の場合(この場合はインポートが必要 from peewee import SqliteDatabase)
db = connect(os.environ.get("DATABASE"))  # 環境変数に合わせて変更する場合
# db = connect(os.environ.get("DATABASE") or "sqlite:///peewee_db.sqlite")  # 環境変数が無い場合にデフォルト値として値を設定することも可能


# 地区テーブルのモデル
class Areas(Model):
    """Areas Model"""

    area_id = IntegerField(primary_key=True)  # idは自動で追加されるが明示
    area_name = CharField()
    collection_type_id = IntegerField()

    class Meta:
        database = db
        table_name = "areas"


# ごみ種別テーブルのモデル
class GarbageTyeps(Model):
    """GarbageTyeps Model"""

    garbage_type_id = IntegerField(primary_key=True)
    garbage_type_name = CharField()

    class Meta:
        database = db
        table_name = "garbage_types"


# 収集種別テーブルのモデル
class CollectionTypes(Model):
    """CollectionTypes Model"""

    collection_type_id = ForeignKeyField(Areas, backref="areas", on_delete="CASCADE")
    garbage_type_id = ForeignKeyField(GarbageTyeps, backref="garbage_types", on_delete="CASCADE")
    collection_date = TimestampField()

    class Meta:
        database = db
        table_name = "collection_types"


db.create_tables([Areas, CollectionTypes, GarbageTyeps])
