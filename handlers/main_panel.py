from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.inline import choice_account


router = Router()


# --- StatesGroup для регистрации продавца ---


class AddSeller(StatesGroup):
    company_name = State()
    phone = State()


# --- Основная панель ---


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать на маркетплейс для <b>реконструкторов</b>\
        \n\nДавайте знакомиться! Кто вы?",
        reply_markup=choice_account().as_markup()
    )


# --- Обработчик кнопоки рагистрации/авторизации покупателя ---


@router.callback_query(F.data == "i_am_buyer")
async def i_am_buyer_btn(callback: CallbackQuery):
    pool = callback.bot.pool

    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(
                "INSERT INTO buyers (user_id, username, purchased) VALUES ($1, $2, $3) ON CONFLICT (user_id) DO NOTHING",
                callback.from_user.id,
                callback.from_user.username,
                0
            )
            username = await connection.fetchval(
                "SELECT username from buyers WHERE user_id = $1",
                callback.from_user.id
            )

    await callback.message.answer(
        text=f"Добро пожаловать, <b>{username}</b>!",
        reply_markup=None
    )


# --- Обработчик кнопоки рагистрации/авторизации продавца ---


@router.callback_query(F.data == "i_am_seller")
async def i_am_seller_btn(callback: CallbackQuery, state: FSMContext):
    pool = callback.bot.pool

    async with pool.acquire() as connection:
        async with connection.transaction():
            username = await connection.fetchval(
                "SELECT username from staff WHERE user_id = $1",
                callback.from_user.id
            )
            if username is None:
                await callback.message.answer(
                    text="Похоже у Вас нет аккаунт продавца 😥\n\nНе страшно! Мы создадим его прямо сейчас!\n\n<b>Как называется Ваша фирма?</b>\n<i>Введите название в чат:</i>",
                    reply_markup=None
                )
                await state.set_state(AddSeller.company_name)
            else:
                await callback.message.answer(
                    text=f"Добро пожаловать, продавец <b>{username}</b>!",
                    reply_markup=None
                )


# --- Стадия 1. Ввод названия фирмы ---


@router.message(AddSeller.company_name)
async def get_company_name(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id

    if user_id not in data:
        data[user_id] = {}

    data[user_id]['name'] = message.text[:50]
    await state.update_data(data)
    await message.answer(
        text=f"<b>{message.text[:50]}?</b> — звучит отлично!\n\n<b>Нам потребуется Ваш Российский номер телефона,</b> но мы никому его не скажем 😉\n<i>Введите в любом удобном формате:</i>",
        reply_markup=None
    )
    await state.set_state(AddSeller.phone)


# --- Стадия 2. Ввод номера телефона ---


import re

@router.message(AddSeller.phone)
async def get_company_name(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id

    phone_number = re.sub(r'[\s+]', '', message.text)
    if re.match(r'^\d{11}$', phone_number):
        formatted_phone_number = f"+7 ({phone_number[1:4]}) {phone_number[4:7]}-{phone_number[7:9]}-{phone_number[9:]}"

        await state.update_data(data)
        await message.answer(
            text=f"<b>Подытожим:</b>\n\
            \n✅ Ваш рабочий аккаунт: @{message.from_user.username}\
            \n✅ Название фирмы: <i>{data[user_id]['name']}</i>\
            \n✅ Номер телефона: <i>{formatted_phone_number}</i>\
            \n\n<i>Мы покажем ваш рабочий аккаунт рядом с выставленным товаром.</i>",
            reply_markup=None
        )
        print(data)
        await state.clear()
    else:
        await message.answer("Номер должен состоять из 11 цифр. Пожалуйста, повторите попытку:")




# --- Игнорирование действий пока пользователь находяится в стадиях ---


@router.message(lambda message: not message.text, AddSeller.company_name)
@router.message(lambda message: not message.text, AddSeller.phone)
async def ignore_messages(message: Message):
    pass