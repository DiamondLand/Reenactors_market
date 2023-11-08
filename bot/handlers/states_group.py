from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from configs.answers import no_state_but_button_is


router = Router()


# --- StatesGroup для регистрации продавца и блокирующий фильтр для использования команд во время стадий ---


class AddSeller(StatesGroup):
    company_name = State()
    phone = State()

    
not_in_state_filter = ~StateFilter(AddSeller.company_name, AddSeller.phone)


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
    await message.answer(
        "<b>Заполнение формы прервано!</b>\n\n<i>Пропишите</i> /start <i>для возвращения в главную панель 🔄</i>",
        reply_markup=ReplyKeyboardRemove()
    )
