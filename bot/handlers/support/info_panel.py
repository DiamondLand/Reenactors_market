from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline import info_panel_btns, back_info_panel_btns
from configs.answers import *
from configs.states_group import not_in_state_filter


router = Router()
    

# --- Информационная панель c обработчиком кнопки возврата---
@router.message(not_in_state_filter, Command("info"))
async def cmd_info(message: Message):
    await message.answer(
        f"<b>Добро пожаловать!</b> 💖\
        \n\nМы — удобный маркетплейс для реконструкторов!\
        \n\nРады видеть Вас на нашей площадке и настоятельно просим ознакомиться с <i>методами сбора, храенения и использования</i> Ваших данных, а также с <i>принимаемыми условиями использования</i>!",
        reply_markup=info_panel_btns().as_markup()
    )


@router.callback_query(not_in_state_filter, F.data == "info_panel_back")
async def info_panel_back_btn(callback: CallbackQuery):
    await callback.message.edit_text(
        f"<b>Добро пожаловать!</b> 💖\
        \n\nМы — удобный маркетплейс для реконструкторов!\
        \n\nРады видеть Вас на нашей площадке и настоятельно просим ознакомиться с <i>методами сбора, храенения и использования</i> Ваших данных, а также с <i>принимаемыми условиями использования</i>!",
        reply_markup=info_panel_btns().as_markup()
    )


# --- Обработчик кнопоки политики конфиденциальности ---
@router.callback_query(not_in_state_filter, F.data == "privacy_policy")
async def privacy_policy_btn(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f"@{callback.from_user.username}, ознакомьтесь с нашей <u>политикой конфиденциальности</u>.",
        reply_markup=back_info_panel_btns().as_markup()
    )


# --- Обработчик кнопоки условий использования ---
@router.callback_query(not_in_state_filter, F.data == "terms_of_use")
async def terms_of_use_btn(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f"@{callback.from_user.username}, ознакомьтесь с нашими <u>условиями использования</u>.",
        reply_markup=back_info_panel_btns().as_markup()
    )