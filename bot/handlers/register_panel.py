from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import choice_account_btns, сompletion_sellers_registration_btns
from configs.answers import *
from .states_group import AddSeller, not_in_state_filter, cancel_func
import httpx

router = Router()


# --- Основная панель ---


@router.message(not_in_state_filter, Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать на маркетплейс для <b>реконструкторов</b> 💖\
        \n\nДавайте знакомиться! Кто вы?",
        reply_markup=choice_account_btns().as_markup()
    )


# --- Завершение заполнения ---


@router.message(F.text == cancel_button_kb)
async def cancel_handler(message: Message, state: FSMContext):
    await cancel_func(message=message, state=state)


# --- Обработчик кнопоки регистрации/авторизации покупателя ---


@router.callback_query(not_in_state_filter, F.data == "i_am_buyer")
async def i_am_buyer_btn(callback: CallbackQuery):
    # --- Проверка на существование записи и при отсутствии insert ---
    async with httpx.AsyncClient() as client:
        await client.post(callback.bot.config["SETTINGS"]["backend_url"] + 'create_buyer', json={
            "user_id" : callback.from_user.id,
            'username': callback.from_user.username,
            'purchased': 0
        })
        
    await callback.message.edit_text(
        text=f"Добро пожаловать, @{callback.from_user.username}!\n\nВы — покупатель.\n\n<i>Хотите заглянуть в магазин? 😊</i>",
        reply_markup=None
    )


# --- Обработчик кнопоки регистрации/авторизации продавца ---


@router.callback_query(not_in_state_filter, F.data == "i_am_seller")
async def i_am_seller_btn(callback: CallbackQuery, state: FSMContext):
    # --- Проверка на существование записи ---
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{callback.bot.config['SETTINGS']['backend_url']}get_staff?user_id={callback.from_user.id}"
        )

    if res.json() is None:
        await callback.message.edit_text(
            text="Похоже у Вас <b>нет аккаунта продавца</b>, но это не страшно! Мы создадим его прямо сейчас 😎",
            reply_markup=None
        )

        # --- Обычная кнопка для отмены заполнения формы [cancel] ---
        kb = [[KeyboardButton(text=cancel_button_kb)]]
        keyboard = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Прервать заполнение формы"
        )

        await callback.message.answer(
            text="<b>Как называется Ваша фирма?</b>\
            \n\n<i>Введите название в чат:</i>",
            reply_markup=keyboard
        )
        await state.set_state(AddSeller.company_name)
    else:
        await callback.message.edit_text(
            text=f"Добро пожаловать, @{callback.from_user.username}!\n\nВы — продавец.\n\n<i>Не забудьте проверить возможные заказы 🤑</i>",
            reply_markup=None
        )


# --- Стадия 1. Ввод названия фирмы ---


@router.message(AddSeller.company_name)
async def get_company_name(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(text=slash_on_state)
    else:
        data = await state.get_data()        
        data['name'] = message.text[:50]

        await state.update_data(data)
        await message.answer(
            text=f"<b>{message.text[:50]}?</b> — звучит отлично!\
            \n\n<b>Нам потребуется Ваш номер телефона,</b> но мы никому про это не расскажем 😉\
            \n\n<i>Введите его в удобном формате, а дальше позаботимся мы:</i>"
        )
        await state.set_state(AddSeller.phone)


# --- Стадия 2. Ввод номера телефона ---


import re

@router.message(AddSeller.phone)
async def get_company_name(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(text=slash_on_state)
    else:
        data = await state.get_data()

        # --- Проверка на существование стадии ---
        if not data:
            await message.answer(text=no_state)
            return
        
        phone_number = re.sub(r'[\s+]', '', message.text)
        if re.match(r'^\d{11}$', phone_number):
            formatted_phone_number = f"+7 ({phone_number[1:4]}) {phone_number[4:7]}-{phone_number[7:9]}-{phone_number[9:]}"

            data['formatted_phone_number'] = formatted_phone_number
            await state.update_data(data)
            await message.answer(
                text=f"<b>Подытожим:</b>\
                \n\n✅ Ваш рабочий аккаунт: @{message.from_user.username}\
                \n✅ Название фирмы: <i>{data['name']}</i>\
                \n✅ Номер телефона: <i>{data['formatted_phone_number']}</i>\
                \n\n<i>Мы покажем ваш рабочий аккаунт рядом с выставленным товаром.</i>",
                reply_markup=сompletion_sellers_registration_btns().as_markup()
            )
        else:
            await message.answer("❌ <b>Нет-нет-нет!</b>\n\nНомер должен состоять из <b>11 цифр</b>.\n\n<i>Пожалуйста, повторите попытку:</i>")


# --- Обработчик кнопоки завершения регистрации продавца ---


@router.callback_query(F.data == "accept_seller_account_creating")
async def accept_seller_account_creating_btn(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # --- Проверка на существование стадии ---
    if not data:
        await callback.message.answer(text=no_state)
        return
    
    # --- Проверка на существование записи и при отсутствии insert ---
    async with httpx.AsyncClient() as client:
        response = await client.post(callback.bot.config["SETTINGS"]["backend_url"] + 'create_staff', json={
            "user_id": callback.from_user.id,
            'username': callback.from_user.username,
            'company_name': data['name'],
            'phone_number': data['formatted_phone_number'],
            'sold': 0,
            'post': "seller"
        })

    
        if response.status_code == 200:
            await callback.message.edit_text(
                text=f"Добро пожаловать, @{callback.from_user.username}!\n\nВы — продавец.\n\n<i>Не затягивайте, выставляйте свои потрясающие товары! 💖</i>",
                reply_markup=None
            )
            await callback.message.answer(
                text="✅ Ваши даннные успешно сохранены и находятся в полной безопасности!",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await callback.message.edit_text(
                text="Что-то пошло не так...",
                reply_markup=None
            )
            await callback.message.answer(
                text=response_server_error,
                reply_markup=ReplyKeyboardRemove()
            )
        await state.clear()
      

# --- Обработчик кнопоки рестарта регистрации продавца ---


@router.callback_query(F.data == "refresh_seller_account_creating")
async def accept_seller_account_creating_btn(callback: CallbackQuery, state: FSMContext):
    # --- Проверка на существование записи ---
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{callback.bot.config['SETTINGS']['backend_url']}get_staff?user_id={callback.from_user.id}"
        )

    if res.json() is None:
        # --- Обычная кнопка для отмены заполнения формы [cancel] ---
        kb = [[KeyboardButton(text=cancel_button_kb)]]
        keyboard = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Прервать заполнение формы"
        )
        await callback.message.edit_text(
            text="Без проблем, заполним форму заново 👌",
            reply_markup=None
        )
        await callback.message.answer(
            text="<b>Как называется Ваша фирма?</b>\
            \n\n<i>Введите название в чат:</i>",
            reply_markup=keyboard
        )
        await state.set_state(AddSeller.company_name)

    else:
        await callback.message.edit_text(
            text="🔄 <b>У вас уже есть аккаунт продавца!</b>\n\nВы уже можете начинать выставлять товары.\n\n<i>Зайдите в аккаунт, использовав /start</i>",
            reply_markup=None
        )