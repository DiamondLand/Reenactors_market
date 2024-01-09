from fastapi import APIRouter
from datetime import datetime
from .models import Seller, Buyer, Support, Product
from .schemas import CreateBuyerModel, CreateSellerModel, CreateQuestionToSupport, CreateAnswerQuestionToSupport, AddProductModel

controller = APIRouter()

# --- Проверка наличия аккаунта Seller --- 
@controller.get('/get_seller')
async def get_seller(user_id: int):
    res = await Seller.get_or_none(user_id=user_id)
    return res


# --- Проверка привилегий аккаунта --- 
@controller.get('/get_privilege')
async def get_privilege(user_id: int):
    res = await Buyer.get_or_none(user_id=user_id)
    return res.privilege if res and res.privilege else None


# --- Регистрация Seller ---
@controller.post('/create_seller')
async def create_seller(data: CreateSellerModel):
    new_seller, created = await Seller.get_or_create(
        user_id=data.user_id,
        defaults={
            'company_name': data.company_name,
            'contact': data.contact,
        }
    )
    return {'user_id': new_seller.user_id, 'created': created}


# --- Регистрация Buyer ---
@controller.post('/create_buyer')
async def create_buyer(data: CreateBuyerModel):
    buyer, created = await Buyer.get_or_create(
        user_id=data.user_id,
        defaults={
            'username': data.username,
            'privilege': data.privilege
        }
    )
    return {'user_id': buyer.user_id, 'created': created}


# --- Добавление товара ---
@controller.post('/add_product')
async def add_product(data: AddProductModel):
    await Product.create(
        product_name = data.product_name,
        product_description = data.product_description,
        product_price = data.product_price,
        product_category = data.product_category,
        product_subcategory = data.product_subcategory,
        product_subsubcategory = data.product_subsubcategory,
        product_image_url = data.product_image_url,
        company_name = data.company_name
    )


# --- Получение всех сообщений в поддержку --- 
@controller.get('/get_messages_on_support')
async def get_messages_on_support(user_id: int):
    res = await Support.filter(user_id=user_id).order_by('-question_date').all()
    return res


# --- Получение сообщений в поддержку без ответа --- 
@controller.get('/get_messages_on_support_for_staff')
async def get_messages_on_support_for_staff():
    res = await Support.filter(answer=None).order_by('-question_date').all()
    return res


# --- Новый вопрос поддержке ---
@controller.post('/send_question')
async def send_question(data: CreateQuestionToSupport):
    support = await Support.create(
        user_id=data.user_id,
        question=data.question,
        question_date=datetime.now()
    )
    return support


# --- Запись ответа от поддержки ---
@controller.post('/answer_question')
async def answer_question(data: CreateAnswerQuestionToSupport):
    support = await Support.filter(user_id = data.user_id, question=data.question).update(
        answer_username = data.answer_username,
        answer = data.answer,
        answer_date = datetime.now()
    )
    return support
