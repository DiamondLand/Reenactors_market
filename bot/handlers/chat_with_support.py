import httpx

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import support_panel_btns, open_chat_with_support_btn, on_chat_with_support_btn
from configs.answers import *
from .states_group import SupportConnect, not_in_state_filter, cancel_func


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
                f"💌 <b>Готовы помочь пользователям?</b>\
                \n\nВы — представитель поддержки и связь со своими коллегами через данный чат просто не потребуется 😉\
                \n\n<i>Вы всегда можете связаться с администраций, дабы решить возникшие вопросы!</i>",
                reply_markup=support_panel_btns().as_markup()
            )
        else:
            await message.answer(
                f"💌 <b>У вас есть вопросы? Мы всё решим!</b>\
                \n\n<i>Все запросы в поддержку будут отображены в данном сообщении при нажатии кнопки по форме (запрос-ответ, запрос-ответ).</i>",
                reply_markup=open_chat_with_support_btn().as_markup()
            )


# --- Выход из чата с поддержкой ---
@router.message(F.text == cancel_button_kb)
async def cancel_connect_with_support_handler(message: Message, state: FSMContext):
    await cancel_func(message=message, state=state)
    await message.answer(
        "✅ Чат с оператором поддержки был сохранён!",
        reply_markup=ReplyKeyboardRemove()
    )
    await cmd_support(message)


# --- Обработчик кнопоки окрытия чата с поддержкой ---
@router.callback_query(not_in_state_filter, F.data == "open_chat_with_support")
async def chat_with_support_btn(callback: CallbackQuery):
    # # --- Проверка на существование записи ---
    # async with httpx.AsyncClient() as client:
    #     res = await client.get(
    #         f"{callback.bot.config['SETTINGS']['backend_url']}get_messages_on_support?user_id={callback.from_user.id}"
    #     )
    await callback.message.edit_text(
        "<b>Это <u>первая</u> страница</b>",
        reply_markup=on_chat_with_support_btn().as_markup()
    )

    # if callback.message.text.startswith("/"):
    #     await callback.message.answer(text=slash_on_state)
    # else:
        
        

# --- Обработчик кнопоки написания сообщения с поддержкой ---
@router.callback_query(not_in_state_filter, F.data == "wrtite_to_support")
async def wrtite_to_support_btn(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SupportConnect.support_text)
    # --- Обычная кнопка для отмены заполнения формы [cancel] ---
    kb = [[KeyboardButton(text=cancel_button_kb)]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Прервать заполнение формы"
    )
    await callback.message.answer(text="✅", reply_markup=keyboard)
    await callback.message.delete()

