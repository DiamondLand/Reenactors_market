from fastapi import APIRouter
from .models import Seller, Buyer
from .schemas import CreateBuyerModel, CreateSellerModel

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
    new, created = await Buyer.update_or_create(
        user_id=data.user_id,
        defaults={
            'username': data.username,
            'purchased': data.purchased,
            'privilege': data.privilege
        }
    )
    if created:
        return {'user_id': new.user_id}
    else:
        pass


# --- Проверка привелегий аккаунта --- 
@controller.get('/get_privilege')
async def get_privilege(user_id: int):
    res = await Buyer.get_or_none(user_id=user_id)
    if res and res.privilege:
        return res.privilege
    else:
        return None