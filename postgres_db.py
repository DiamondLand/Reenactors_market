import configparser
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model

config = configparser.ConfigParser()
config.read("configs/config.ini")


class Buyer(Model):
    user_id = fields.BigIntField(unique=True)
    username = fields.CharField(max_length=50)
    purchased = fields.IntField()


class Product(Model):
    product_id = fields.IntField(pk=True)
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
    user_id = fields.BigIntField(unique=True)
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


async def main():
    await Tortoise.init(
        modules={"models": ["postgres_db"]},
        db_url=f"postgres://{config['DATABASE']['user']}:{config['DATABASE']['password']}@{config['DATABASE']['host']}:{config['DATABASE']['port']}/{config['DATABASE']['database']}"
    )

    queries = [
        "DROP TABLE IF EXISTS Buyer;",
        "DROP TABLE IF EXISTS Product;",
        "DROP TABLE IF EXISTS Ordering;",
        "DROP TABLE IF EXISTS Staff;",
        "DROP TABLE IF EXISTS Support;"
    ]
    
    for query in queries:
        await Tortoise.get_connection("default").execute_query(query)

    await Tortoise.generate_schemas()

if __name__ == "__main__":
    run_async(main())
