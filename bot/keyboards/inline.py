from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# --- Выбор аккаунта ---
def choice_account_btns() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Я покупатель 😉",
            callback_data="i_am_buyer"
        ),
        InlineKeyboardButton(
            text="Я продавец 😎",
            callback_data="i_am_seller"
        )
    )
    return builder


# --- Кнопка открытия магазина ---
def shop_open_btn() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="В магазин 🛍️",
            callback_data="shop_open"
        )
    )
    return builder


# --- Панель администратора ---
def admin_panel_btns() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="В магазин 🛍️",
            callback_data="shop_open"
        ),
        InlineKeyboardButton(
            text="Продавцы 💖",
            callback_data="all_sellers"
        ),
        InlineKeyboardButton(
            text="Ответить на запросы 💌",
            callback_data="chat_with_support"
        ),
        InlineKeyboardButton(
            text="Товары на модерации ⚙️",
            callback_data="new_products"
        ),
        InlineKeyboardButton(
            text="Заблокировать аккаунт 💀",
            callback_data="ban_account"
        ),
        InlineKeyboardButton(
            text="Назначить оператора поддержки 🎉",
            callback_data="new_support"
        )
    )
    builder.adjust(2, 1)
    return builder


# --- Панель оператора поддержки ---
def support_panel_btns() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="В магазин 🛍️",
            callback_data="shop_open"
        ),
        InlineKeyboardButton(
            text="Ответить на запросы 💌",
            callback_data="chat_with_support"
        )
    )
    builder.adjust(1, 1)
    return builder


# --- Завершение регистрации ---
def сompletion_sellers_registration_btns() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Всё верно 😎",
            callback_data="accept_seller_account_creating"
        ),
        InlineKeyboardButton(
            text="Я ошибся 😐",
            callback_data="refresh_seller_account_creating"
        )
    )
    return builder


# --- Информационная панель ---
def info_panel_btns() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Политика конфиденциальности",
            callback_data="privacy_policy"
        ),
        InlineKeyboardButton(
            text="Условия использования",
            callback_data="terms_of_use"
        ),
        InlineKeyboardButton(
            text="Поддержка",
            callback_data="connect_with_support"
        )
    )
    builder.adjust(1, 1)
    return builder


def back_info_panel_btns() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data="info_panel_back"
        )
    )
    return builder


# --- Панель связи с поддержкой---
def open_chat_with_support_btn() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Перейти в чат",
            callback_data="open_chat_with_support"
        )
    )
    return builder


# --- Чат с поддержкой---
def on_chat_with_support_btn() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Далее",
            callback_data="next_on_chat_with_support"
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data="back_on_chat_with_support"
        ),
        InlineKeyboardButton(
            text="К последней",
            callback_data="last_on_chat_with_support"
        ),
        InlineKeyboardButton(
            text="К первой",
            callback_data="first_on_chat_with_support"
        ),
        InlineKeyboardButton(
            text="Написать",
            callback_data="wrtite_to_support"
        )
    )
    builder.adjust(2, 2)
    return builder
