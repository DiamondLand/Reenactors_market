import configparser
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from loguru import logger

from handlers import register_panel, different_types, info_panel, chat_with_support, add_product

config = configparser.ConfigParser()
config.read("bot/configs/config.ini")


async def main():
    bot = Bot(config["SETTINGS"]["token"], parse_mode=ParseMode.HTML)
    bot.config = config
    dp = Dispatcher()


    # --- Подключение модулей ---
    logger.info("Loading modules...")
    dp.include_routers(
        register_panel.router,
        add_product.router,
        info_panel.router,
        chat_with_support.router,
        different_types.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    logger.success("Bot successfully launched")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())