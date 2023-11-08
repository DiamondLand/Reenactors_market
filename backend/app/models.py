import configparser
from tortoise import fields, run_async
from tortoise.models import Model

config = configparser.ConfigParser()
config.read("configs/config.ini")


class Buyer(Model):
<<<<<<< HEAD
    user_id = fields.BigIntField(unique=True, pk=True)
=======
    user_id = fields.BigIntField(unique=True)
>>>>>>> 3cd027d45fbe7bbc8de4e9412f46a37672aa01d1
    username = fields.CharField(max_length=50)
    purchased = fields.IntField()


class Product(Model):
<<<<<<< HEAD
    product_id = fields.IntField()
=======
    product_id = fields.IntField(pk=True)
>>>>>>> 3cd027d45fbe7bbc8de4e9412f46a37672aa01d1
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
    order_id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    company_name = fields.CharField(max_length=50)
    price = fields.IntField()
    username = fields.CharField(max_length=50)
    order_date = fields.DateField()
    order_status = fields.BooleanField()


class Staff(Model):
<<<<<<< HEAD
    user_id = fields.BigIntField(unique=True, pk=True)
=======
    user_id = fields.BigIntField(unique=True)
>>>>>>> 3cd027d45fbe7bbc8de4e9412f46a37672aa01d1
    username = fields.CharField(max_length=50)
    company_name = fields.CharField(max_length=50)
    phone = fields.CharField(max_length=18)
    sold = fields.IntField()
    post = fields.CharField(max_length=50)


class Support(Model):
    request_id = fields.IntField(pk=True)
    chat_id = fields.BigIntField()
    username = fields.CharField(max_length=50)
    question = fields.TextField()
    question_date = fields.DateField()
    answer = fields.TextField()
    answer_date = fields.DateField()