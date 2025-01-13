from datetime import datetime
import peewee as pw

db = pw.SqliteDatabase('MyGeo3.db')


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())

    class Meta():
        database = db


class History(ModelBase):
    request = pw.TextField()
    id = pw.AutoField(primary_key=True)

