import configparser
import asyncio

from handlers import register_panel, different_types, states_group
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from postgres_db import create_db_pool

config = configparser.ConfigParser()
config.read("configs/config.ini")

async def main():
    bot = Bot(config["SETTINGS"]["token"], parse_mode=ParseMode.HTML)
    bot.pool = await create_db_pool()
    dp = Dispatcher()


    # --- Подключение модулей ---


    dp.include_routers(
        register_panel.router,
        states_group.router,
        different_types.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())