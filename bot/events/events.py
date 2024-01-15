from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from keyboards.inline import choice_account_btns

from configs.states_group import cancel_func
from configs.answers import cancel_button_kb
from configs.states_group import not_in_state_filter

router = Router()

# --- Главная панель (выбор аккаунта) ---
@router.message(not_in_state_filter, Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать на маркетплейс для <b>реконструкторов</b> 💖\
        \n\nПожалуйста, выберите аккаунт:",
        reply_markup=choice_account_btns().as_markup()
    )


# --- Завершение заполнения формы ---
@router.message(F.text == cancel_button_kb)
async def cancel_register_handler(message: Message, state: FSMContext):
    cheaker = await cancel_func(message=message, state=state)
    if cheaker is not False:
        await message.answer(
            "<b>Заполнение формы прервано!</b>\n\nВведённые данные не были сохранены!",
            reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(
            "Добро пожаловать на маркетплейс для <b>реконструкторов</b> 💖\
            \n\nПожалуйста, выберите аккаунт:",
            reply_markup=choice_account_btns().as_markup()
        )
    else:
        await message.answer(
            "Добро пожаловать на маркетплейс для <b>реконструкторов</b> 💖\
            \n\nПожалуйста, выберите аккаунт:",
            reply_markup=choice_account_btns().as_markup()
        )


# --- Возвращение в главную панель ---
@router.callback_query(not_in_state_filter, F.data == "back_to_main_panel")
async def back_to_main_panel_btn(callback: CallbackQuery):
    await callback.message.edit_text(
        "Добро пожаловать на маркетплейс для <b>реконструкторов</b> 💖\
        \n\nПожалуйста, выберите аккаунт:",
        reply_markup=choice_account_btns().as_markup()
    )