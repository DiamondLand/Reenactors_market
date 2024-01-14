import configparser

from tortoise.contrib.fastapi import register_tortoise

config = configparser.ConfigParser()
config.read("bot/configs/config.ini")


def init_db(app):
    register_tortoise(
        app,
        #db_url=f"postgres://{config['DATABASE']['user']}:{config['DATABASE']['password']}@{config['DATABASE']['host']}:{config['DATABASE']['port']}/{config['DATABASE']['database']}",
        db_url='sqlite://bot/database.db',
        modules={'models': ['products.models', 'register.models', 'support.models']},
        generate_schemas=True,
        add_exception_handlers=False,
    )
