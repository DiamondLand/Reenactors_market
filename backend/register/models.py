from tortoise import fields
from tortoise.models import Model


class Buyer(Model):
    user_id = fields.BigIntField(unique=True, pk=True)
    username = fields.CharField(max_length=50)
    privilege = fields.CharField(max_length=50, null=True)


class Seller(Model):
    user_id = fields.BigIntField(unique=True, pk=True)
    company_name = fields.CharField(max_length=50)
    contact = fields.CharField(max_length=100)
