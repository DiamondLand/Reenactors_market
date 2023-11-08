import configparser

from tortoise.contrib.fastapi import register_tortoise

config = configparser.ConfigParser()
config.read("bot/configs/config.ini")


def init(app):
    """Функция для инициализации базы данных."""
    register_tortoise(
        app,
        db_url=f"postgres://{config['DATABASE']['user']}:{config['DATABASE']['password']}@{config['DATABASE']['host']}:{config['DATABASE']['port']}/{config['DATABASE']['database']}",
        modules={"models": ['app.models']},
        generate_schemas=True,
        add_exception_handlers=False,
    )
