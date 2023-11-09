import configparser
from tortoise import fields, run_async
from tortoise.models import Model

config = configparser.ConfigParser()
config.read("configs/config.ini")


class Buyer(Model):
    user_id = fields.BigIntField(unique=True, pk=True)
    username = fields.CharField(max_length=50)
    purchased = fields.IntField()
    privilege = fields.CharField(max_length=50, null=True)


class Product(Model):
    product_id = fields.BigIntField()
    name = fields.CharField(max_length=50)
    description = fields.CharField(max_length=100)
    price = fields.IntField()
    amount = fields.IntField()
    category = fields.CharField(max_length=50)
    subcategory = fields.CharField(max_length=50)
    subsubcategory = fields.CharField(max_length=50)
    image_url = fields.CharField(max_length=255)
    company_name = fields.CharField(max_length=50)
    moderation = fields.BooleanField()
    moderation_comment = fields.CharField(max_length=50)


class Ordering(Model):
    order_id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=50)
    company_name = fields.CharField(max_length=50)
    price = fields.IntField()
    username = fields.CharField(max_length=50)
    order_date = fields.DateField()
    order_status = fields.BooleanField()


class Seller(Model):
    user_id = fields.BigIntField(unique=True, pk=True)
    username = fields.CharField(max_length=50)
    company_name = fields.CharField(max_length=50)
    phone = fields.CharField(max_length=18)
    sold = fields.IntField()


class Support(Model):
    request_id = fields.BigIntField(pk=True)
    chat_id = fields.BigIntField()
    user_id = fields.BigIntField()
    question = fields.TextField()
    question_date = fields.DateField()
    answer_user_id = fields.BigIntField()
    answer = fields.TextField()
    answer_date = fields.DateField()