import httpx

from datetime import date
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import support_panel_btns, on_chat_with_support_btn
from configs.answers import *
from .states_group import SupportConnect, not_in_state_filter, cancel_func


router = Router()


# --- Панель связи с поддержкой ---
@router.message(not_in_state_filter, Command("support"))
async def cmd_support(message: Message):
    # --- Проверка на существование записи и при отсутствии insert ---
    async with httpx.AsyncClient() as client:
        response = await client.post(message.bot.config["SETTINGS"]["backend_url"] + 'create_buyer', json={
            "user_id": message.from_user.id,
            'username': message.from_user.username
        })
        # --- Проверка привелегии ---
        privilege_res = await client.get(
            f"{message.bot.config['SETTINGS']['backend_url']}get_privilege?user_id={message.from_user.id}"
        )
        if response.status_code == 200 and privilege_res.status_code == 200:
            if privilege_res.json() == 'admin' or privilege_res.json() == 'support':
                await message.answer(
                    f"💌 <b>Готовы помочь пользователям?</b>\
                    \n\nВы — представитель поддержки и связь со своими коллегами через данный чат просто не потребуется 😉\
                    \n\n<i>Вы всегда можете связаться с администраций, дабы решить возникшие вопросы!</i>",
                    reply_markup=support_panel_btns().as_markup()
                )
            else:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{message.bot.config['SETTINGS']['backend_url']}get_messages_on_support?user_id={message.from_user.id}"
                    )

                if response.status_code == 200:
                    messages = response.json()
                    if messages and len(messages) > 0:
                        first_message = messages[0] 

                        await message.answer(
                            f"📤 <b>Ваш крайний вопрос:</b>\
                            \n<i>{first_message['question']}</i>\
                            \n<b>Дата обращения (МСК):</b> <i>{first_message['question_date']}</i>\
                            \n\n📥 <b>Ответил: @{first_message['answer_username']}</b>\
                            \n<i>{first_message['answer'] if first_message['answer'] else '—'}</i>\
                            \n<b>Дата ответа (МСК):</b> <i>{first_message['answer_date'] if first_message['answer_date'] else '—'}</i>",
                            reply_markup=on_chat_with_support_btn().as_markup()
                        )
                    else:
                        await message.answer(
                            text="У вас нет запросов в поддержку!",
                            reply_markup=on_chat_with_support_btn().as_markup()
                        )
                else:
                    await message.answer(text=response_server_error)
        else:
            await message.answer(text=response_server_error)


# --- Выход из чата с поддержкой ---
@router.message(F.text == cancel_support_write_button_kb)
async def cancel_connect_with_support_handler(message: Message, state: FSMContext):
    await cancel_func(message=message, state=state)
    await message.answer(
        "✅ Чат с оператором поддержки был сохранён!",
        reply_markup=ReplyKeyboardRemove()
    )
    await cmd_support(message)
    

# --- Обработчик кнопоки написания сообщения с поддержкой ---
@router.callback_query(not_in_state_filter, F.data == "wrtite_to_support")
async def wrtite_to_support_btn(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SupportConnect.support_text)
    # --- Обычная кнопка для отмены заполнения формы [cancel] ---
    kb = [[KeyboardButton(text=cancel_support_write_button_kb)]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Прервать заполнение формы"
    )
    await callback.message.answer(
        text="💌 <b>Так-так. Записываем!</b>\
        \n\nОпишите проблему. Чем лучше будет сформулирован вопрос, тем больше вероятность решения проблемы!\
        \n\n<i>Помните, что лимит символов — 1.500. Текст больше будет обрезан!</i>",
        reply_markup=keyboard
    )


# --- Стадия 1. Получения сообщения ---
@router.message(SupportConnect.support_text)
async def write_to_support_text(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(text=slash_on_state)
    else:
        async with httpx.AsyncClient() as client:            
            response = await client.post(
                f"{message.bot.config['SETTINGS']['backend_url']}to_send_question", json={
                    'user_id': message.from_user.id,
                    'question': message.text[:1500],
                    'question_data': str(date.today())
                })

        await state.clear()
        if response.status_code == 422:
            await message.answer(
                text=f"✅ Ваш вопрос: <i>{message.text[:1500]}?</i> был записан!\n\n<i>Ответ появится в панеле запросов.</i>",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await message.answer(text=response_server_error, reply_markup=ReplyKeyboardRemove())

