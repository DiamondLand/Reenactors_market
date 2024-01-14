import configparser
from tortoise import fields
from tortoise.models import Model

config = configparser.ConfigParser()
config.read("configs/config.ini")


class Buyer(Model):
    user_id = fields.BigIntField(unique=True, pk=True)
    username = fields.CharField(max_length=50)
    privilege = fields.CharField(max_length=50, null=True)


class Product(Model):
    product_id = fields.BigIntField(pk=True)
    product_name = fields.CharField(max_length=50)
    product_description = fields.CharField(max_length=100)
    product_price = fields.IntField()
    product_category = fields.CharField(max_length=50)
    product_subcategory = fields.CharField(max_length=50)
    product_subsubcategory = fields.CharField(max_length=50)
    product_image_url = fields.CharField(max_length=255)
    company_name = fields.CharField(max_length=50)
    moderation = fields.BooleanField()
    moderation_comment = fields.CharField(null=True, max_length=50)


class Seller(Model):
    user_id = fields.BigIntField(unique=True, pk=True)
    company_name = fields.CharField(max_length=50)
    contact = fields.CharField(max_length=100)


class Support(Model):
    request_id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    question = fields.TextField()
    question_date = fields.DatetimeField()
    answer_username = fields.CharField(null=True, max_length=50)
    answer = fields.TextField(null=True)
    answer_date = fields.DatetimeField(null=True)