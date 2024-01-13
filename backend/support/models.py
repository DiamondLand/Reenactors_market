from tortoise import fields
from tortoise.models import Model


class Support(Model):
    request_id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    question = fields.TextField()
    question_date = fields.DatetimeField()
    answer_username = fields.CharField(null=True, max_length=50)
    answer = fields.TextField(null=True)
    answer_date = fields.DatetimeField(null=True)