import httpx

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline import support_panel_btns, open_chat_with_support_btn
from configs.answers import *
from .states_group import not_in_state_filter


router = Router()


# --- Панель связи с поддержкой ---


@router.message(not_in_state_filter, Command("support"))
async def cmd_support(message: Message):
    # --- Проверка на существование записи и при отсутствии insert ---
    async with httpx.AsyncClient() as client:
        await client.post(message.bot.config["SETTINGS"]["backend_url"] + 'create_buyer', json={
            "user_id" : message.from_user.id,
            'username': message.from_user.username
        })
        # --- Проверка привелегии ---
        privilege_res = await client.get(
            f"{message.bot.config['SETTINGS']['backend_url']}get_privilege?user_id={message.from_user.id}"
        )
        if privilege_res.json() == 'admin' or privilege_res.json() == 'support':
            await message.answer(
                f"<b>Готовы помочь пользователям?</b>\
                \n\nВы и так представитель поддержки и связь со своими коллегами через данный чат просто не потребуется 😉\
                \n\n<i>Вы всегда можете связаться с администраций, дабы решить возникшие вопросы!</i>",
                reply_markup=support_panel_btns().as_markup()
            )
        else:
            await message.answer(
                f"💌 <b>У вас есть вопросы? Мы всё решим!</b>\
                \n\nВаш чат №{message.from_user.id}.\
                \n\n<i>Все сообщения из Вашего чата будут отправлены после нажатия кнопки и отображаться списком.</i>",
                reply_markup=open_chat_with_support_btn().as_markup()
            )


# --- Обработчик кнопоки окрытия чата с поддержкой ---
@router.callback_query(not_in_state_filter, F.data == "open_chat_with_support")
async def chat_with_support_btn(callback: CallbackQuery):
    # --- Проверка на существование записи ---
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{callback.bot.config['SETTINGS']['backend_url']}get_seller?user_id={callback.from_user.id}"
        )

