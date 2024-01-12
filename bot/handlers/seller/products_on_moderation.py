import httpx

from aiogram import Router, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

from configs.answers import *
from configs.states_group import not_in_state_filter


router = Router()


# --- Обработчик кнопоки добавления товара ---
@router.callback_query(not_in_state_filter, F.data == "cheak_product_on_moderation")
async def cheak_product_on_moderation_btn(callback: CallbackQuery):
    # --- Проверка на существование записи ---
    async with httpx.AsyncClient() as client:
        cheak_seller_response = await client.get(
            f"{callback.bot.config['SETTINGS']['backend_url']}get_seller?user_id={callback.from_user.id}"
        )

    if cheak_seller_response.status_code == 200:
        if cheak_seller_response.json() is None:
            await callback.message.edit_text(
                text="Похоже у Вас <b>нет аккаунта продавца</b>, но это не страшно! Вы можете создать его прямо сейчас.\
                \n\n<i>Воспользуйтесь /start для выбора аккаунта или же регистрации</i>",
                reply_markup=None
            )
        else:
            # --- Берём данные о товарах на модерации ---
            async with httpx.AsyncClient() as client:
                cheak_seller_response = await client.get(
                    f"{callback.bot.config['SETTINGS']['backend_url']}get_seller?user_id={callback.from_user.id}"
                )

    else:
        await callback.answer(text=response_server_error)
