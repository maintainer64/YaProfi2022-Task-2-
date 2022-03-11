import peewee

from application.database.bind import database
from application.database.promo import PromoDB


class MemberDB(peewee.Model):
    id = peewee.AutoField(primary_key=True, index=True, null=False)
    name = peewee.CharField(index=True, null=False)
    promo = peewee.ForeignKeyField(PromoDB, index=True, backref="members", on_delete="CASCADE")

    class Meta:
        db_table = "member"
        database = database
