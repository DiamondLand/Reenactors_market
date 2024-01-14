import httpx

from aiogram import Router, F, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

from configs.answers import *
from configs.states_group import not_in_state_filter
from keyboards.inline import seller_products_on_moderation_btns
from configs.patterns import send_product_card


router = Router()
products_indices = {}
seller_products_on_moderation_response = {}

# --- Отображение товаров на модерации для продавца ---
async def display_card(res, callback: CallbackQuery = None):
    await callback.message.edit_text(
        text=send_product_card(
            name=res['product_name'],
            description=res['product_description'],
            price=res['product_price'],
            prev_send=True,
            category=res['product_category'],
            subcategory=res['product_subcategory'],
            subsubcategory=res['product_subsubcategory']
        ),
        reply_markup=seller_products_on_moderation_btns().as_markup()
    )


# --- Обработчик кнопоки просмотра товаров на модерации---
@router.callback_query(not_in_state_filter, F.data == "cheak_product_on_moderation")
async def cheak_product_on_moderation_btn(callback: CallbackQuery):
    # --- Проверка на существование аккаунта продавца ---
    async with httpx.AsyncClient() as client:
        seller_response = await client.get(
            f"{callback.bot.config['SETTINGS']['backend_url']}get_seller?user_id={callback.from_user.id}"
        )

    if seller_response.status_code == 200:
        if seller_response.json() is None:
            await callback.message.edit_text(
                text="Похоже у Вас <b>нет аккаунта продавца</b>, но это не страшно! Вы можете создать его прямо сейчас.\
                \n\n<i>Воспользуйтесь /start для выбора аккаунта или же регистрации</i>",
                reply_markup=None
            )
        else:
            # --- Берём данные о товарах на модерации ---
            async with httpx.AsyncClient() as client:
                get_company_products_on_moderation = await client.get(
                    f"{callback.bot.config['SETTINGS']['backend_url']}get_company_products_on_moderation?company_name={seller_response.json()['company_name']}"
                )
            if get_company_products_on_moderation.status_code == 200:

                company_products_on_moderation = get_company_products_on_moderation.json()
                seller_products_on_moderation_response[callback.from_user.id] = company_products_on_moderation
                products_indices[callback.from_user.id] = 0

                if company_products_on_moderation and len(company_products_on_moderation) > 0:
                    await display_card(res=company_products_on_moderation[0], callback=callback)
                else:
                    await callback.message.answer(
                        text="У Вас отсутствуют товары на модерации. Вероятнее всего они уже в магазине 🤩",
                    )
            else:
                await callback.answer(text=response_server_error)
    else:
        await callback.answer(text=response_server_error)


# --- Обработчик кнопоки ДАЛЕЕ ---
@router.callback_query(not_in_state_filter, F.data == "next_on_seller_products_on_moderation")
async def next_on_seller_products_on_moderation_btn(callback: CallbackQuery):
    user_id = callback.from_user.id
    messages = seller_products_on_moderation_response[user_id]
    current_index = products_indices.get(user_id, 0)

    if messages and len(messages) > current_index + 1:
        products_indices[user_id] = current_index + 1
        await display_card(res=messages[current_index + 1], callback=callback)
    else:
        await callback.answer(
            text="Это последняя страница!", 
            show_alert=True
        )


# --- Обработчик кнопоки НАЗАД ---
@router.callback_query(not_in_state_filter, F.data == "back_on_seller_products_on_moderation")
async def back_on_seller_products_on_moderation_btn(callback: CallbackQuery):
    user_id = callback.from_user.id
    if products_indices.get(user_id) is not None:
        current_index = products_indices[user_id]
        if current_index > 0:
            products_indices[user_id] -= 1
            messages = seller_products_on_moderation_response[user_id]
            await display_card(res=messages[current_index - 1], callback=callback)
        else:
            await callback.answer(
                text="Это последняя страница!", 
                show_alert=True
            )
    else:
        await callback.answer(
            text="Это последняя страница!", 
            show_alert=True
        )