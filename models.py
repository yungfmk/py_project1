from peewee import *

db = SqliteDatabase('database.bd')
cursor = db.cursor


class BaseModel(Model):
    class Meta:
        database = db


class Meta:
    bd_table = 'expenses'


class UserDb(BaseModel):
    username = TextField(default="None")

    email = TextField(default="None")

    age = IntegerField()

    city = TextField()


with db:
    db.create_tables(
        [
            UserDb
        ]
    )


def create_user(**user):
    user_query = UserDb.select().where(UserDb.username == user['username'])
    if user_query.exists():
        return {'message': 'user already exists'}

    UserDb(username=user['username'], email=user['email'], age=user['age'],
           city=user['city']).save()
    return {"message": "user added"}


def delete_user(id_: int):
    user_query = UserDb.select().where(UserDb.id == id_)
    if not user_query.exists():
        return {'message': 'user does not exists'}

    UserDb.select().where(UserDb.id == id_).get().delete_instance()
    return {'message': 'user deleted'}


def update_user(id_: int, **user):
    user_query = UserDb.select().where(UserDb.id == id_)
    if not user_query.exists():
        return {'message': 'user does not exists'}

    user_query = user_query.get()

    for user_key in user:
        if user[user_key]:
            setattr(user_query, user_key, user[user_key])

    user_query.save()
    return {'message': 'user updated'}


def show_users(username=None):
    if username:
        user_query = UserDb.select().where(UserDb.username == username)
        if not user_query.exists():
            return {'message': 'user does not exists'}

        user_query = user_query.get().__dict__
        return {'message': 'user found', 'user': user_query}

    result = [user.__dict__['__data__'] for user in UserDb.select()]
    return result
