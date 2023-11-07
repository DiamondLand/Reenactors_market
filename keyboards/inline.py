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