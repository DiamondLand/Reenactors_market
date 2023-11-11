import httpx

from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import support_panel_btns, on_chat_with_support_btn, on_chat_with_support_buyer_btn
from configs.answers import *
from configs.states_group import SupportConnect, not_in_state_filter, cancel_func


router = Router()
user_question_indices = {}
messages_response = {}


# --- Отображение запросов и ответов в панеле ---
async def display_question(res, msg: Message = None, callback: CallbackQuery = None):
    if res['answer']:
        answer_text = f"📥 <b>Ответил: @{res['answer_username']}</b>\
        \n<i>{res['answer']}</i>\
        \n\n⌚ <b>Ответ получен </b>\n<i>{datetime.fromisoformat(res['answer_date']).strftime('%m-%d-%Y %H:%M:%S по МСК')}</i>"

    all_text = f"📤 <b>Ваш вопрос:</b>\
        \n<i>{res['question']}</i>\
        \n\n⌚ <b>Вы обратились </b>\n<i>{datetime.fromisoformat(res['question_date']).strftime('%m-%d-%Y %H:%M:%S по МСК')}</i>\
        \nn{answer_text if res['answer'] is not None else 'Ответ ещё не получен, но мы показываем Ваш вопрос всем агентам поддержки! 😎'}"
    
    if msg:
        await msg.answer(
            text=all_text,
            reply_markup=on_chat_with_support_btn().as_markup()
        )

    if callback:
        await callback.message.edit_text(
            text=all_text,
            reply_markup=on_chat_with_support_btn().as_markup()
        )


# --- Отображение запросов  панеле сотрудников поддержки ---
async def display_question_for_support(res, callback: CallbackQuery):
    all_text = f"📥 <b>Вопрос пользователя:</b>\
        \n<i>{res['question']}</i>\
        \n\n⌚ <b>Пользователь обратился </b>\n<i>{datetime.fromisoformat(res['question_date']).strftime('%m-%d-%Y %H:%M:%S по МСК')}</i>"

    if callback:
        await callback.message.edit_text(
            text=all_text,
            reply_markup=on_chat_with_support_buyer_btn().as_markup()
        )


# --- Выход из чата с поддержкой ---
@router.message(F.text == cancel_support_write_button_kb)
async def cancel_connect_with_support_handler(message: Message, state: FSMContext):
    await cancel_func(message=message, state=state)
    await message.answer(
        "<b>Заполнение прервано!</b>\n\nВведённые данные не были сохранены!",
        reply_markup=ReplyKeyboardRemove()
    )
    await cmd_support(message)


# --- Панель связи с поддержкой ---
@router.message(not_in_state_filter, Command("support"))
async def cmd_support(message: Message):
    # --- Проверка на существование записи и при отсутствии insert ---
    async with httpx.AsyncClient() as client:
        buyer_response = await client.post(message.bot.config["SETTINGS"]["backend_url"] + 'create_buyer', json={
            "user_id": message.from_user.id,
            'username': message.from_user.username
        })
        # --- Проверка привелегии ---
        privilege_res = await client.get(
            f"{message.bot.config['SETTINGS']['backend_url']}get_privilege?user_id={message.from_user.id}"
        )
        if buyer_response.status_code == 200 and privilege_res.status_code == 200:
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
                    messages_response[message.from_user.id] = messages
                    user_question_indices[message.from_user.id] = 0
                    if messages and len(messages) > 0:
                        await display_question(res=messages[0], msg=message)
                    else:
                        await message.answer(
                            text="У вас нет запросов в поддержку!",
                            reply_markup=on_chat_with_support_btn().as_markup()
                        )
                else:
                    await message.answer(text=response_server_error) 
        else:
            await message.answer(text=response_server_error) 
    

# --- Обработчик кнопоки ДАЛЕЕ ---
@router.callback_query(not_in_state_filter, F.data == "next_on_chat_with_support")
async def next_question_to_support_btn(callback: CallbackQuery):
    user_id = callback.from_user.id
    messages = messages_response[user_id]
    current_index = user_question_indices.get(user_id, 0)

    if messages and len(messages) > current_index + 1:
        user_question_indices[user_id] = current_index + 1
        await display_question(res=messages[current_index + 1], callback=callback)
    else:
        await callback.answer(
            text="Это последняя страница!", 
            show_alert=True
        )


# --- Обработчик кнопоки НАЗАД ---
@router.callback_query(not_in_state_filter, F.data == "back_on_chat_with_support")
async def next_question_to_support_btn(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_question_indices.get(user_id) is not None:
        current_index = user_question_indices[user_id]
        if current_index > 0:
            user_question_indices[user_id] -= 1
            messages = messages_response[user_id]
            await display_question(res=messages[current_index - 1], callback=callback)
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


# --- Обработчик кнопоки ответа на вопросы ---
@router.callback_query(not_in_state_filter, F.data == "chat_with_support")
async def chat_with_support_btn(callback: CallbackQuery):
    # --- Проверка на существование записи и при отсутствии insert ---
    async with httpx.AsyncClient() as client:
        buyer_response = await client.post(callback.bot.config["SETTINGS"]["backend_url"] + 'create_buyer', json={
            "user_id": callback.from_user.id,
            'username': callback.from_user.username
        })
        # --- Проверка привелегии ---
        privilege_res = await client.get(
            f"{callback.bot.config['SETTINGS']['backend_url']}get_privilege?user_id={callback.from_user.id}"
        )
        if buyer_response.status_code == 200 and privilege_res.status_code == 200:
            if privilege_res.json() == 'admin' or privilege_res.json() == 'support':
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{callback.bot.config['SETTINGS']['backend_url']}get_messages_on_support_for_staff"
                    )

                if response.status_code == 200:
                    messages = response.json()
                    messages_response[callback.from_user.id] = messages
                    user_question_indices[callback.from_user.id] = 0
                    if messages and len(messages) > 0:
                        await display_question_for_support(res=messages[0], callback=callback)
                    else:
                        await callback.message.edit_text(
                            text="Новых запросов не поступало! Отдыхаем 🤩", 
                            reply_markup=None
                        )
                else:
                    await callback.message.edit_text(text=response_server_error)


# --- Обработчик кнопоки ДАЛЕЕ для сотрудников ---
@router.callback_query(not_in_state_filter, F.data == "next_on_chat_with_support_buyer")
async def next_question_to_support_btn(callback: CallbackQuery):
    user_id = callback.from_user.id
    messages = messages_response[user_id]
    current_index = user_question_indices.get(user_id, 0)

    if messages and len(messages) > current_index + 1:
        user_question_indices[user_id] = current_index + 1
        await display_question_for_support(res=messages[current_index + 1], callback=callback)
    else:
        await callback.answer(
            text="Это последняя страница!", 
            show_alert=True
        )


# --- Обработчик кнопоки НАЗАД для сотрудников ---
@router.callback_query(not_in_state_filter, F.data == "back_on_chat_with_support_buyer")
async def next_question_to_support_btn(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_question_indices.get(user_id) is not None:
        current_index = user_question_indices[user_id]
        if current_index > 0:
            user_question_indices[user_id] -= 1
            messages = messages_response[user_id]
            await display_question_for_support(res=messages[current_index - 1], callback=callback)
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


# --- Обработчик кнопоки написания сообщения в поддержкой ---
@router.callback_query(not_in_state_filter, F.data == "wrtite_to_support")
async def wrtite_to_support_btn(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SupportConnect.to_support_text)
    # --- Обычная кнопка для отмены заполнения формы [cancel] ---
    kb = [[KeyboardButton(text=cancel_support_write_button_kb)]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Прервать заполнение формы"
    )
    await callback.message.edit_text(
        text="💌 <b>Так-так. Записываем!</b>\
        \n\nОпишите проблему. Чем лучше будет сформулирован вопрос, тем больше вероятность решения проблемы!",
        reply_markup=None
    )
    await callback.message.answer(
        text="<i>Помните, лимит символов — 1.500. Текст больше будет обрезан!</i>",
        reply_markup=keyboard
    )


# --- Стадия 1. Получения сообщения ---
@router.message(SupportConnect.to_support_text)
async def write_to_support_text(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(text=slash_on_state)
    else:
        async with httpx.AsyncClient() as client:            
            response = await client.post(
                f"{message.bot.config['SETTINGS']['backend_url']}send_question", json={
                    'user_id': message.from_user.id,
                    'question': message.text[:1500]
                })

        await state.clear()
        del messages_response[message.from_user.id]
        del user_question_indices[message.from_user.id]
        if response.status_code == 200:
            await message.answer(
                text=f"✅ <b>Вопрос записан!</b>\n\n<i>{message.text[:1500]}</i>\n\n<i>Ответ появится в панеле запросов /support 💕</i>",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await message.answer(text=response_server_error, reply_markup=ReplyKeyboardRemove())
        


# --- Обработчик кнопоки написания сообщения от поддержки пользователю ---
@router.callback_query(not_in_state_filter, F.data == "wrtite_to_buyer_support")
async def wrtite_to_buyer_support_btn(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SupportConnect.to_buyer_text)
    # --- Обычная кнопка для отмены заполнения формы [cancel] ---
    kb = [[KeyboardButton(text=cancel_support_write_button_kb)]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Прервать заполнение формы"
    )
    await callback.message.edit_text(
        text="💌 <b>Так-так. Помогаем пользователю!</b>\
        \n\nЧем лучше будет сформулирован ответ, тем больше вероятность решения проблемы!",
        reply_markup=None
    )
    await callback.message.answer(
        text="<i>Помните, лимит символов — 1.500. Текст больше будет обрезан!</i>",
        reply_markup=keyboard
    )


# --- Стадия 1. Получение ответа---
@router.message(SupportConnect.to_buyer_text)
async def wrtite_to_buyer_support_text(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(text=slash_on_state)
    else:
        index = user_question_indices[message.from_user.id]
        messages = messages_response[message.from_user.id][index]
        async with httpx.AsyncClient() as client:            
            response = await client.post(
                f"{message.bot.config['SETTINGS']['backend_url']}answer_question", json={
                    'user_id': int(messages['user_id']),
                    'question': str(messages['question']),
                    'answer_username': message.from_user.username,
                    'answer': message.text[:1500]
                })

        await state.clear()
        if response.status_code == 200:
            await message.answer(
                text=f"✅ <b>Ответ записан!</b>\n\n<i>{message.text[:1500]}</i>\n\n<i>Для быстрого возвращения в панель используйте /support</i>",
                reply_markup=ReplyKeyboardRemove()
            )
            await message.bot.send_message(
                chat_id=int(messages['user_id']),
                text="💌 <b>Вам пришёл ответ от поддержки!</b>\
                \n\nИспользуйте /support для просмотра сообщения."
            )
        else:
            await message.answer(text=response_server_error, reply_markup=ReplyKeyboardRemove())
        del messages_response[message.from_user.id]
        del user_question_indices[message.from_user.id]
