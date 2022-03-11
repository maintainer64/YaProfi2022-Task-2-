import peewee

from application.database.bind import database
from application.database.promo import PromoDB


class PrizeDB(peewee.Model):
    id = peewee.AutoField(primary_key=True, index=True, null=False)
    description = peewee.CharField(index=True, null=False)
    promo = peewee.ForeignKeyField(PromoDB, index=True, backref="prizes", on_delete="CASCADE")

    class Meta:
        db_table = "prize"
        database = database
