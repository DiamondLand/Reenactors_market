import pydantic

from fastapi import APIRouter
from .models import Staff, Buyer


controller = APIRouter()


# --- Проверка наличия аккаунта Staff --- 
@controller.get('/get_staff')
async def get_staff(user_id: int):
    res = await Staff.get_or_none(user_id=user_id)
    if res:
        return res
    else:
        return None


# --- Регистрация Staff ---
class CreateStaffModel(pydantic.BaseModel):
    user_id: int
    username: str
    company_name: str
    phone_number: str
    sold: int = 0
    post: str = 'seller'


@controller.post('/create_staff')
async def get_user(data: CreateStaffModel):
    new, created = await Staff.update_or_create(
        user_id=data.user_id,
        defaults={
            'username': data.username,
            'company_name': data.company_name,
            'phone': data.phone_number,
            'sold': data.sold,
            'post': data.post
        }
    )
    return {'user_id': new.user_id}


# --- Регистрация Buyer ---
class CreateBuyerModel(pydantic.BaseModel):
    user_id: int
    username: str
    purchased: int = 0


@controller.post('/create_buyer')
async def get_user(data: CreateBuyerModel):
    new, created = await Buyer.update_or_create(
        user_id=data.user_id,
        defaults={
            'username': data.username,
            'purchased': data.purchased,
        }
    )
    if created:
        return {'user_id': new.user_id}
    else:
        pass
