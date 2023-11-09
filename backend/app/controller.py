from fastapi import APIRouter
from .models import Seller, Buyer, Support
from .schemas import CreateBuyerModel, CreateSellerModel, CreateQuestionToSupport

controller = APIRouter()


# --- Проверка наличия аккаунта Seller --- 
@controller.get('/get_seller')
async def get_seller(user_id: int):
    res = await Seller.get_or_none(user_id=user_id)
    if res:
        return res
    else:
        return None
    

# --- Проверка привелегий аккаунта --- 
@controller.get('/get_privilege')
async def get_privilege(user_id: int):
    res = await Buyer.get_or_none(user_id=user_id)
    if res and res.privilege:
        return res.privilege
    else:
        return None
    

# --- Регистрация Seller ---
@controller.post('/create_seller')
async def create_seller(data: CreateSellerModel):
    new, _ = await Seller.update_or_create(
        user_id=data.user_id,
        defaults={
            'username': data.username,
            'company_name': data.company_name,
            'phone': data.phone_number,
            'sold': data.sold
        }
    )
    return {'user_id': new.user_id}


# --- Регистрация Buyer ---
@controller.post('/create_buyer')
async def create_buyer(data: CreateBuyerModel):
    res = await Buyer.get_or_none(user_id=data.user_id)
    if not res:
        created = await Buyer.create(
            user_id = data.user_id,
            username = data.username,
            purchased = data.purchased,
            privilege = data.privilege
        )
        created.save()


# --- Проверка привелегий аккаунта --- 
@controller.get('/get_privilege')
async def get_privilege(user_id: int):
    res = await Buyer.get_or_none(user_id=user_id)
    if res and res.privilege:
        return res.privilege
    else:
        return None
    

# --- Получение сообщений в чате с поддержкой --- 
@controller.get('/get_messages_on_support')
async def get_messages_on_support(user_id: int):
    res = await Support.filter(user_id=user_id).all()
    if res:
        return res
    else:
        return None
    

# --- Новый вопрос поддержке ---
@controller.post('/send_question')
async def send_question(data: CreateQuestionToSupport):
    created = await Support.create(
        user_id = data.user_id,
        question = data.question,
        question_date = data.question_date
    )
    created.save()


# --- Ответ от поддержки ---
@controller.post('/answer_question')
async def answer_question(data: CreateQuestionToSupport):
    created = await Support.filter(user_id = data.user_id).update(
        answer_user_id  = data.answer_user_id,
        answer = data.answer_user_id,
        answer_date = data.answer_user_id
    )
    created.save()
    

