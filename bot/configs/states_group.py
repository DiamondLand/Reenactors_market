from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from configs.answers import no_state_but_button_is


# --- StatesGroup для регистрации продавца ---
class AddSeller(StatesGroup):
    company_name = State()
    phone = State()


# --- StatesGroup для работы с чатом поддержки ---
class SupportConnect(StatesGroup):
    to_support_text = State()
    to_buyer_text = State()


# Блокирующий фильтр для использования команд во время стадий
not_in_state_filter = ~StateFilter(AddSeller.company_name, AddSeller.phone, SupportConnect.to_support_text)


# --- Завершение заполнения формы по кнопке отмены ---
async def cancel_func(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            text=no_state_but_button_is,
            reply_markup=ReplyKeyboardRemove()
        )
        return
    
    await state.clear()
