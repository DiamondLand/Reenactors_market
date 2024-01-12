from fastapi import APIRouter

from .models import Seller, Buyer
from .schemas import CreateBuyerModel, CreateSellerModel

client = APIRouter()

# --- Проверка наличия аккаунта Seller ---
@client.get('/get_seller')
async def get_seller(user_id: int):
    res = await Seller.get_or_none(user_id=user_id)
    return res


# --- Проверка привилегий аккаунта ---
@client.get('/get_privilege')
async def get_privilege(user_id: int):
    res = await Buyer.get_or_none(user_id=user_id)
    return res.privilege if res and res.privilege else None


# --- Регистрация Seller ---
@client.post('/create_seller')
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
@client.post('/create_buyer')
async def create_buyer(data: CreateBuyerModel):
    buyer, created = await Buyer.get_or_create(
        user_id=data.user_id,
        defaults={
            'username': data.username,
            'privilege': data.privilege
        }
    )
    return {'user_id': buyer.user_id, 'created': created}
