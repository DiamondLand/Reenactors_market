from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def choice_account() -> InlineKeyboardBuilder:
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


def accepting_seller_account_creating() -> InlineKeyboardBuilder:
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