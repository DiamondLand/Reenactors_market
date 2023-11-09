from fastapi import APIRouter
<<<<<<< HEAD
from .models import Seller, Buyer
from .schemas import CreateBuyerModel, CreateSellerModel
=======
from .models import Staff, Buyer

>>>>>>> 4c3fdcfd7ca61bb01d81015cd559d46bfbba71d9

controller = APIRouter()


<<<<<<< HEAD
# --- Проверка наличия аккаунта Seller --- 
@controller.get('/get_seller')
async def get_seller(user_id: int):
    res = await Seller.get_or_none(user_id=user_id)
=======
# --- Проверка наличия аккаунта Staff --- 
@controller.get('/get_staff')
async def get_staff(user_id: int):
    res = await Staff.get_or_none(user_id=user_id)
>>>>>>> 4c3fdcfd7ca61bb01d81015cd559d46bfbba71d9
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
    

<<<<<<< HEAD
# --- Регистрация Seller ---
@controller.post('/create_seller')
async def create_seller(data: CreateSellerModel):
    new, _ = await Seller.update_or_create(
=======
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
>>>>>>> 4c3fdcfd7ca61bb01d81015cd559d46bfbba71d9
        user_id=data.user_id,
        defaults={
            'username': data.username,
            'company_name': data.company_name,
            'phone': data.phone_number,
<<<<<<< HEAD
            'sold': data.sold
=======
            'sold': data.sold,
            'post': data.post
>>>>>>> 4c3fdcfd7ca61bb01d81015cd559d46bfbba71d9
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