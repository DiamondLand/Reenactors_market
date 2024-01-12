import httpx

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from configs.answers import *
from configs.states_group import AddSeller, not_in_state_filter, cancel_func


router = Router()