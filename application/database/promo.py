import peewee

from application.database.bind import database


class PromoDB(peewee.Model):
    id = peewee.AutoField(primary_key=True, index=True, null=False)
    name = peewee.CharField(index=True, null=False)
    description = peewee.CharField(index=True, null=True)

    class Meta:
        db_table = "promo"
        database = database
