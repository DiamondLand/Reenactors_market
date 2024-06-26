from fastapi import APIRouter
from datetime import datetime
from .models import Support
from .schemas import CreateQuestionToSupport, CreateAnswerQuestionToSupport

support = APIRouter()

# --- Получение всех сообщений в поддержку --- 
@support.get('/get_messages_on_support')
async def get_messages_on_support(user_id: int):
    return await Support.filter(user_id=user_id).order_by('-question_date').all()


# --- Получение сообщений в поддержку без ответа --- 
@support.get('/get_messages_on_support_for_staff')
async def get_messages_on_support_for_staff():
    return await Support.filter(answer=None).order_by('-question_date').all()


# --- Новый вопрос поддержке ---
@support.post('/send_question')
async def send_question(data: CreateQuestionToSupport):
    await Support.create(
        user_id=data.user_id,
        question=data.question,
        question_date=datetime.now()
    )


# --- Запись ответа от поддержки ---
@support.post('/answer_question')
async def answer_question(data: CreateAnswerQuestionToSupport):
    await Support.filter(user_id = data.user_id, question=data.question).update(
        answer_username = data.answer_username,
        answer = data.answer,
        answer_date = datetime.now()
    )
