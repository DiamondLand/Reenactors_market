import random

from aiogram import Router, F
from aiogram.types import Message

# Список милых сообщений благодарности
thank_you_sticker_messages = [
    "Спасибо за этот замечательный стикер!",
    "Твои стикеры всегда приносят улыбку!",
    "Спасибо за милый стикер! 😊",
    "Так мило! Спасибо за стикер!",
]

thank_you_animation_messages = [
    "Спасибо за гифку! 😊",
    "Твои гифвки всегда приносят улыбку!",
    "Спасибо за милую анимацию! 😊",
    "Так мило! Спасибо за гифку!",
]

router = Router()

@router.message(F.sticker)
async def message_with_sticker(message: Message):
    await message.answer(random.choice(thank_you_sticker_messages))

@router.message(F.animation)
async def message_with_gif(message: Message):
    await message.answer(random.choice(thank_you_animation_messages))