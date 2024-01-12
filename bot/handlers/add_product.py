import httpx
import validators
import re

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from PIL import Image
from io import BytesIO

from keyboards.inline import сompletion_add_product_btns
from configs.categories import *
from configs.answers import *
from configs.patterns import send_product_card
from configs.states_group import AddProduct, not_in_state_filter


router = Router()


# --- Обработчик кнопоки добавления товара ---
@router.callback_query(not_in_state_filter, F.data == "add_product_to_moderation")
async def add_product_to_moderation_btn(callback: CallbackQuery, state: FSMContext):
    # --- Проверка на существование записи ---
    async with httpx.AsyncClient() as client:
        cheak_seller_response = await client.get(
            f"{callback.bot.config['SETTINGS']['backend_url']}get_seller?user_id={callback.from_user.id}"
        )

    if cheak_seller_response.status_code == 200:
        if cheak_seller_response.json() is None:
            await callback.message.edit_text(
                text="Похоже у Вас <b>нет аккаунта продавца</b>, но это не страшно! Вы можете создать его прямо сейчас.\
                \n\n<i>Воспользуйтесь /start для выбора аккаунта или же регистрации</i>",
                reply_markup=None
            )
        else:
            # --- Обычная кнопка для отмены заполнения формы [cancel] ---
            kb = [[KeyboardButton(text=cancel_button_kb)]]
            keyboard = ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
                input_field_placeholder="Прервать заполнение формы"
            )
            await callback.message.edit_text(
                text="🐼 <b>Начинаем добавление товара!</b>\
                \n\nХотим сразу предупредить, что прежде появления товара на маркетплейсе, он должен пройти модерацию. Обычно это занимает не более 5-и часов!",
                reply_markup=None
            )
            await callback.message.answer(
                text="<b>Как называется товар?</b>\
                \n\n<i>Помните, лимит символов — 1.500. Текст больше будет обрезан!</i>",
                reply_markup=keyboard
            )
            await state.set_state(AddProduct.name)

    else:
        await callback.answer(text=response_server_error)


# --- Стадия 1. Ввод названия ---
@router.message(AddProduct.name)
async def get_product_name(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(text=slash_on_state)
    else:
        data = await state.get_data()        
        data['product_name'] = message.text[:50]

        await state.update_data(data)
        await message.answer(
            text=f"<b>Укажите описание товара:</b>\
            \n\n<i>Помните, лимит символов — 100. Текст больше будет обрезан!</i>"
        )
        await state.set_state(AddProduct.description)


# --- Стадия 2. Ввод описания ---
@router.message(AddProduct.description)
async def get_product_description(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(text=slash_on_state)
    else:
        data = await state.get_data()

        # --- Проверка на существование стадии ---
        if not data:
            await message.answer(text=no_state)
            return
         
        data['product_description'] = message.text[:100]

        await state.update_data(data)
        await message.answer(
            text=f"Сколько стоит <b>{data.get('product_name', '').lower()}</b>?\
            \n\n<i>Нам потребуется только число, как цена в Российских рублях!</i>"
        )
        await state.set_state(AddProduct.price)


# --- Стадия 3. Ввод цены ---
@router.message(AddProduct.price)
async def get_product_price(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(text=slash_on_state)
    else:
        data = await state.get_data()

        # --- Проверка на существование стадии ---
        if not data:
            await message.answer(text=no_state)
            return
        
        only_numbers = re.sub(r'\D', '', message.text)

        if len(str(only_numbers)) >= 1:
            if 100 <= int(only_numbers) <= 100000:
                data['product_price'] = only_numbers

                await state.update_data(data)
                await message.answer(
                    text=f"<b>Укажите категорию товара...</b>\
                    \n\nПожалуйста, перепишите название из предложенного списка:\
                    \n\n➡️ <i>{', '.join(category)}</i>"
                )
                await state.set_state(AddProduct.category)
            else:
                await message.answer(
                    text=f"❌ <b>Ого-го!</b>\
                    \n\nК сожалению, мы не можем принять товар дешевле 100₽ или же дороже 100.000₽!\
                    \n\n<i>Нам потребуется только число, как цена в Российских рублях!</i>"
                )
        else:
            await message.answer(
                text="❌ <b>Ну это же не цена...</b>\
                \n\nУкажите цену товара.\
                \n\n<i>Нам потребуется только число, как цена в Российских рублях!</i>"
            )


# --- Стадия 4. Ввод категории ---
@router.message(AddProduct.category)
async def get_product_category(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(text=slash_on_state)
    else:
        data = await state.get_data()

        # --- Проверка на существование стадии ---
        if not data:
            await message.answer(text=no_state)
            return
        
        if message.text.lower() in category:
            data['product_category'] = message.text
        
            await state.update_data(data)
            await message.answer(
                text=f"<b>Выберите страну, как подкатегорию...</b>\
                \n\n➡️ <i>{', '.join(word.capitalize() for word in subcategory)}</i>"
            )
            await state.set_state(AddProduct.subcategory)
        else:
            await message.answer(
                text=f"❌ <b>Такого варианта нет...</b>\
                \n\nУбедитесь, что вы корректно переписали категорию товара!\
                \n\n➡️ <i>{', '.join(category)}</i>"
            )


# --- Стадия 5. Ввод подкатегории ---
@router.message(AddProduct.subcategory)
async def get_product_subcategory(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(text=slash_on_state)
    else:
        data = await state.get_data()

        # --- Проверка на существование стадии ---
        if not data:
            await message.answer(text=no_state)
            return
        
        if message.text.lower() in subcategory:
            data['product_subcategory'] = message.text
        
            await state.update_data(data)
            await message.answer(
                text=f"<b>Какая подподкатегория товара?</b>\
                \n\nДа-да, и такое бывает!\
                \n\n➡️ <i>{', '.join(subsubcategory)}</i>"
            )
            await state.set_state(AddProduct.subsubcategory)
        else:
            await message.answer(
                text=f"❌ <b>Такого варианта нет...</b>\
                \n\nУбедитесь, что вы корректно переписали подкатегорию товара!\
                \n\n➡️ <i>{', '.join(word.capitalize() for word in subcategory)}</i>"
            )


# --- Стадия 6. Ввод подподкатегории ---
@router.message(AddProduct.subsubcategory)
async def get_product_subsubcategory(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(text=slash_on_state)
    else:
        data = await state.get_data()

        # --- Проверка на существование стадии ---
        if not data:
            await message.answer(text=no_state)
            return
        
        if message.text.lower() in subsubcategory:
            data['product_subsubcategory'] = message.text
        
            await state.update_data(data)
            await message.answer(
                text=f"Потребуется url фотографии товара:"
            )
            await state.set_state(AddProduct.image_url)
        else:
            await message.answer(
                text=f"❌ <b>Такого варианта нет...</b>\
                \n\nУбедитесь, что вы корректно переписали подподкатегорию товара!\
                \n\n➡️ <i>{', '.join(subsubcategory)}</i>"
            )


# --- Стадия 7. Ввод ссылки ---
@router.message(AddProduct.image_url)
async def get_product_image_url(message: Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer(text=slash_on_state)
    else:
        data = await state.get_data()

        # --- Проверка на существование стадии ---
        if not data:
            await message.answer(text=no_state)
            return
        
        # Проверка на корректность URL
        if not validators.url(message.text):
            await message.answer(
                text="❌ <b>Некорректный URL!</b>\
                \n\nУбедитесь, что вы отправили корректную ссылку."
            )
            return

        # Проверка, является ли содержимое URL изображением
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(message.text)
                response.raise_for_status()  # Вызывает исключение, если не 200 OK
                Image.open(BytesIO(response.content))
        except (IOError, Exception):
            await message.answer(
                text="❌ <b>Это же не фото!</b>\
                \n\nУбедитесь, что вы отправили корректную ссылку, содержащую фото товара!"
            )
            return

        data['product_image_url'] = message.text
        await state.update_data(data)
        
        send_product_card_text = send_product_card(
            name=data.get('product_name', ''),
            description=data.get('product_description', ''),
            price=data.get('product_price', ''),
            category=data.get('product_category', ''),
            subcategory=data.get('product_subcategory', ''),
            subsubcategory=data.get('product_subsubcategory', ''),
            prev_send=True
        )
        await message.answer_photo(
            photo=message.text,
            caption=send_product_card_text,
            reply_markup=сompletion_add_product_btns().as_markup(),
        )


# --- Обработчик кнопоки завершения добавления товара ---
@router.callback_query(F.data == "accept_add_product")
async def accept_add_product_btn(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # --- Проверка на существование стадии ---
    if not data:
        await callback.message.answer(text=no_state)
        return
    
    # --- Проверка на существование записи и при отсутствии insert ---
    async with httpx.AsyncClient() as client:
        # --- Берём данные о компании продавца ---
        company_name_response = await client.get(
            f"{callback.bot.config['SETTINGS']['backend_url']}get_seller?user_id={callback.from_user.id}"
        )
        add_product_response = await client.post(
            f"{callback.bot.config['SETTINGS']['backend_url']}add_product", json={
                'product_name': data.get('product_name', ''),
                'product_description': data.get('product_description', ''),
                'product_price': data.get('product_price', ''),
                'product_category': data.get('product_category', ''),
                'product_subcategory': data.get('product_subcategory', ''),
                'product_subsubcategory': data.get('product_subsubcategory', ''),
                'product_image_url': data.get('product_image_url', ''),
                'company_name': company_name_response.json()['company_name'],
        })

    await state.clear()
    if company_name_response.status_code == add_product_response.status_code == 200:
        await callback.bot.delete_message(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id
        )
        await callback.message.answer(
            text="✅ Товар отправлен на модерацию и как только мы всё проверим, не медля, сообщим вам!",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await callback.message.answer(
            text=response_server_error,
            reply_markup=ReplyKeyboardRemove()
        )
        