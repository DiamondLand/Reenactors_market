import httpx
import re

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import сompletion_sellers_registration_btns, admin_panel_btns, support_panel_btns, shop_open_btn, seller_panel_btns
from configs.answers import *
from configs.states_group import AddSeller, not_in_state_filter


router = Router()

# --- Обработчик кнопоки регистрации/авторизации покупателя ---
@router.callback_query(not_in_state_filter, F.data == "i_am_buyer")
async def i_am_buyer_btn(callback: CallbackQuery):
    # --- Проверка на существование аккаунта покупателя и при отсутствии - создание ---
    async with httpx.AsyncClient() as client:
        response = await client.post(callback.bot.config["SETTINGS"]["backend_url"] + 'create_buyer', json={
            "user_id" : callback.from_user.id,
            'username': callback.from_user.username
        })
        # --- Проверка привелегии ---
        privilege_res = await client.get(
            f"{callback.bot.config['SETTINGS']['backend_url']}get_privilege?user_id={callback.from_user.id}"
        )
    
    if response.status_code == privilege_res.status_code == 200:
        match privilege_res.json()['privilege']:
            case 'admin':
                await callback.message.edit_text(
                    text=f"Добро пожаловать, @{callback.from_user.username}!\
                    \n\nВы — <b>администратор</b>.\
                    \n\n<i>Начнём работу с контроля товаров, или с запросов в поддержку? 😊</i>",
                    reply_markup=admin_panel_btns().as_markup()
                )
                
            case 'support':
                await callback.message.edit_text(
                    text=f"Добро пожаловать, @{callback.from_user.username}!\
                    \n\nВы — <b>оператор поддержки</b>.\
                    \n\n<i>Давайте посмотрим новые запросы в поддержку? 😊</i>",
                    reply_markup=support_panel_btns().as_markup()
                )
                
            case _:     
                await callback.message.edit_text(
                    text=f"Добро пожаловать, @{callback.from_user.username}!\
                    \n\nВы — <b>покупатель</b>.\
                    \n\n<i>Хотите заглянуть в магазин? 😊</i>",
                    reply_markup=shop_open_btn().as_markup()
                )
    else:
        await callback.answer(text=response_server_error)


# --- Обработчик кнопоки регистрации/авторизации продавца ---
@router.callback_query(not_in_state_filter, F.data == "i_am_seller")
async def i_am_seller_btn(callback: CallbackQuery, state: FSMContext):
    # --- Проверка на существование аккаунта продавца ---
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{callback.bot.config['SETTINGS']['backend_url']}get_seller?user_id={callback.from_user.id}"
        )

    if response.status_code == 200:
        if response.json() is None:
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
                text=f"Добро пожаловать, @{callback.from_user.username}!\n\nВы — продавец.\n\n",
                reply_markup=seller_panel_btns().as_markup()
            )
    else:
        await callback.answer(text=response_server_error)


# --- Стадия 1. Ввод названия фирмы ---
@router.message(AddSeller.company_name)
async def get_company_name(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(text=slash_on_state)
    else:
        company_name = message.text[:50]
        # --- Проверка на существование комапании с таким же названием ---
        async with httpx.AsyncClient() as client:
            check_duplicate_company_name = await client.get(
                f"{message.bot.config['SETTINGS']['backend_url']}check_duplicate_company_name?company_name={company_name}"
            )

        if check_duplicate_company_name.status_code == 200:
            if check_duplicate_company_name.json():
                await message.answer(
                    text=f"<b>❌ Название комапании уже занято!</b>\
                    \n\n<i>Компания с названием</i> <u>{company_name}</u> <i>уже существует. Пожалуйста, введите иное:</i>"
                )
                return
            else:
                data = await state.get_data()        
                data['company_name'] = company_name
                await state.update_data(data)
                
                await message.answer(
                    text=f"<b>{company_name}?</b> — звучит отлично!\
                    \n\n<b>Нам потребуется дополнительный контакт для связи продавца с Вами.</b>\
                    \n\n<i>Предоставьте информацию о любом способе связи, исключая Telegram:</i>"
                )
                await state.set_state(AddSeller.contact)
        else:
            await message.answer(text=response_server_error)


# --- Стадия 2. Ввод способа для связи ---
@router.message(AddSeller.contact)
async def get_company_name(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(text=slash_on_state)
    else:
        data = await state.get_data()

        # --- Проверка на существование стадии заполнения ---
        if not data:
            await message.answer(text=no_state)
            return

        if message.text and any(char.isdigit() for char in message.text):
            phone_number = re.sub(r'\D', '', message.text) # Оставить только цифры
            if len(phone_number) == 11:
                contact = f"+7 ({phone_number[1:4]}) {phone_number[4:7]}-{phone_number[7:9]}-{phone_number[9:]}"
            else:
                await message.answer("❌ <b>Нет-нет-нет!</b>\n\nПохоже, Вы пытались указать номер телефона, но он должен состоять из <b>11 цифр</b>.\n\n<i>Пожалуйста, повторите попытку:</i>")
                return
        else:
            contact = message.text[:100]

        data['contact'] = contact
        await state.update_data(data)

        text = (
            f"<b>Подытожим:</b>"
            f"\n\n✅ Ваш рабочий аккаунт: @{message.from_user.username}"
            f"\n✅ Название фирмы: <i>{data.get('company_name', '')}</i>"
            f"\n✅ Резервный способ связи: <i>{data.get('contact', '')}</i>"
            f"\n\n<i>Мы покажем данную информацию рядом с выставленным товаром.</i>"
        )

        await message.answer(text, reply_markup=сompletion_sellers_registration_btns().as_markup())


# --- Обработчик кнопоки завершения регистрации продавца ---
@router.callback_query(F.data == "accept_seller_account_creating")
async def accept_seller_account_creating_btn(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # --- Проверка на существование стадии ---
    if not data:
        await callback.message.answer(text=no_state)
        return
    
    company_name = data.get('company_name', '')
    contact = data.get('contact', '')
    await state.clear()

    # --- Проверка на существование комапании с таким же названием ---
    async with httpx.AsyncClient() as client:
        check_duplicate_company_name = await client.get(
            f"{callback.bot.config['SETTINGS']['backend_url']}check_duplicate_company_name?company_name={company_name}"
        )
            
    if check_duplicate_company_name.status_code == 200:
        if check_duplicate_company_name.json():
            await callback.message.delete()
            await callback.message.answer(
                text=f"<b>❌ Название комапании уже занято!</b>\
                \n\n<i>Компания с названием <u>{company_name}</u> уже существует...</i>",
                reply_markup=ReplyKeyboardRemove()
            )
            return
        else:
            # --- Создание аккаунта ---
            async with httpx.AsyncClient() as client:
                response = await client.post(callback.bot.config["SETTINGS"]["backend_url"] + 'create_seller', json={
                    'user_id': callback.from_user.id,
                    'company_name': company_name,
                    'contact': contact,
                })

        if response.status_code == 200:
            await callback.message.edit_text(
                text="Ваши даннные сохранены и находятся в полной безопасности!\n\n<i>Мы обо всём позаботимся 😉</i>",
                reply_markup=ReplyKeyboardRemove
            )
            await callback.message.answer(
                text=f"Добро пожаловать, @{callback.from_user.username}!\n\n<b>Вы — продавец.</b>\n\n<i>Не затягивайте, выставляйте свои потрясающие товары! 💖</i>",
                reply_markup=seller_panel_btns().as_markup()
            )
        else:
            await callback.message.delete()
            await callback.message.answer(
                text=response_server_error,
                reply_markup=ReplyKeyboardRemove()
            )
    else:
        await callback.message.delete()
        await callback.message.answer(
            text=response_server_error,
            reply_markup=ReplyKeyboardRemove()
        )
      

# --- Обработчик кнопоки рестарта регистрации продавца ---
@router.callback_query(F.data == "refresh_seller_account_creating")
async def refresh_seller_account_creating_btn(callback: CallbackQuery, state: FSMContext):
    # --- Проверка на существование аккаунта продавца ---
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{callback.bot.config['SETTINGS']['backend_url']}get_seller?user_id={callback.from_user.id}"
        )

    if response.status_code == 200:
        if response.json() is None:
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
            text="🔄 <b>У вас уже есть аккаунт продавца!</b>\n\nВы можете начинать выставлять товары.",
            reply_markup=seller_panel_btns().as_markup()
        )
    else:
        await callback.answer(text=response_server_error)