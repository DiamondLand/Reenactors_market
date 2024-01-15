from fastapi import APIRouter
from .models import Seller, Buyer
from .schemas import CreateBuyerModel, CreateSellerModel

reg = APIRouter()

# --- Проверка наличия аккаунта продавца ---
@reg.get('/get_seller')
async def get_seller(user_id: int):
    return await Seller.get_or_none(user_id=user_id)


# --- Проверка на повторение аккаунта продавца ---
@reg.get('/check_duplicate_company_name')
async def check_duplicate_company_name(company_name: str):
    return await Seller.get_or_none(company_name=company_name)


# --- Проверка привилегий аккаунта ---
@reg.get('/get_privilege')
async def get_privilege(user_id: int):
    return await Buyer.get_or_none(user_id=user_id)


# --- Регистрация продавца ---
@reg.post('/create_seller')
async def create_seller(data: CreateSellerModel):
    new_seller, created = await Seller.get_or_create(
        user_id=data.user_id,
        defaults={
            'company_name': data.company_name,
            'contact': data.contact,
        }
    )
    return {'user_id': new_seller.user_id, 'created': created}


# --- Регистрация покупателя ---
@reg.post('/create_buyer')
async def create_buyer(data: CreateBuyerModel):
    buyer, created = await Buyer.get_or_create(
        user_id=data.user_id,
        defaults={
            'username': data.username,
            'privilege': data.privilege
        }
    )
    return {'user_id': buyer.user_id, 'created': created}
