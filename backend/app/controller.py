import pydantic

from fastapi import APIRouter
<<<<<<< HEAD
=======
from tortoise.exceptions import DoesNotExist
>>>>>>> 3cd027d45fbe7bbc8de4e9412f46a37672aa01d1
from .models import Staff, Buyer


controller = APIRouter()


<<<<<<< HEAD
# --- Проверка наличия аккаунта Staff --- 
@controller.get('/get_staff')
async def get_staff(user_id: int):
    res = await Staff.get_or_none(user_id=user_id)
    if res:
        return res
=======
# --- Проверка наличия аккаунта Staff ---
@controller.post('/get_staff')
async def get_staff(user_id: int):
    data = await Staff.get_or_none(user_id=user_id)
    if data:
        return data
>>>>>>> 3cd027d45fbe7bbc8de4e9412f46a37672aa01d1
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
<<<<<<< HEAD
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
=======
    new = Staff(
        user_id=data.user_id,
        username=data.username,
        company_name=data.company_name,
        phone=data.phone_number,
        sold=data.sold,
        post=data.post
    )
    await new.save()
    return {'id': new.user_id}
>>>>>>> 3cd027d45fbe7bbc8de4e9412f46a37672aa01d1


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
<<<<<<< HEAD
        return {'user_id': new.user_id}
=======
        return {'id': new.user_id}
>>>>>>> 3cd027d45fbe7bbc8de4e9412f46a37672aa01d1
    else:
        pass
