import peewee

from application.database.bind import database
from application.database.group import GroupDB


class ParticipantDB(peewee.Model):
    id = peewee.AutoField(primary_key=True, index=True, null=False)
    name = peewee.CharField(index=True, null=False)
    wish = peewee.CharField(index=True, null=True)
    group = peewee.ForeignKeyField(GroupDB, index=True, backref="participants", on_delete="CASCADE")
    recipient = peewee.ForeignKeyField("self", index=True, backref="participants", on_delete="SET NULL", null=True)

    class Meta:
        db_table = "participant"
        database = database
