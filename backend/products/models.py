from tortoise import fields
from tortoise.models import Model


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
    moderation = fields.BooleanField(null=True)
    moderation_comment = fields.CharField(null=True, max_length=50)
