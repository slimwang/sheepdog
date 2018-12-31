from peewee import SqliteDatabase
from peewee import Model
from peewee import ForeignKeyField
from peewee import CharField
from peewee import IntegerField
from peewee import DateField
from peewee import BooleanField

db = SqliteDatabase('weibo.db')


class Person(Model):
    username = CharField()
    user_id = IntegerField(unique=True)
    weibo_num = IntegerField()
    following = IntegerField()
    followers = IntegerField()
    Q1 = IntegerField(default=0)
    Q2 = IntegerField(default=0)
    Q3 = IntegerField(default=0)
    mean = IntegerField(default=0)
    std = IntegerField(default=0)

    class Meta:
        database = db


class Weibo(Model):
    person = ForeignKeyField(Person, backref='weibo')
    weibo_content = CharField()
    weibo_place = CharField()
    publish_time = DateField()
    up_num = IntegerField()
    retweet_num = IntegerField()
    comment_num = IntegerField()
    publish_tool = CharField()
    is_original = BooleanField()
    sentiment = IntegerField(default=0)

    class Meta:
        database = db


class DB:
    def __init__(self):
        db.connect(reuse_if_open=True)
        db.create_tables([Person, Weibo])

    def store_person(self, username, user_id, weibo_num, following, followers):
        person = Person.select().where(Person.user_id == user_id)
        if person:
            self.person = person[0]
        else:
            self.person = Person.create(
                username=username,
                user_id=user_id,
                weibo_num=weibo_num,
                following=following,
                followers=followers
            )

    def get_person(self, user_id):
        person = Person.get(Person.user_id == user_id)
        return person

    def store_weibo(self, weibo_content, weibo_place, publish_time, up_num, retweet_num, comment_num, publish_tool, is_original):
        Weibo.create(
            person=self.person,
            weibo_content=weibo_content,
            weibo_place=weibo_place,
            publish_time=publish_time,
            up_num=up_num,
            retweet_num=retweet_num,
            comment_num=comment_num,
            publish_tool=publish_tool,
            is_original=is_original,
        )

    def store_sentiment(self, weibo, sentiment):
        weibo.sentiment = sentiment
        weibo.save()

    def store_Q1_Q2_Q3(self, person, Q1, Q2, Q3):
        person.Q1 = Q1
        person.Q2 = Q2
        person.Q3 = Q3
        person.save()

    def store_mean_and_std(self, person, mean, std):
        person.mean = mean
        person.std = std
        person.save()
