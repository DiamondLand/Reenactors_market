from fastapi import APIRouter
from .models import Product
from .schemas import AddProductModel

product = APIRouter()

# --- Добавление товара ---
@product.post('/add_product')
async def add_product(data: AddProductModel):
    await Product.create(**data.__dict__)


# --- Проверка на повторение товара ---
@product.get('/check_duplicate_product')
async def check_duplicate_product(company_name: str, product_name: str):
    return await Product.get_or_none(
        company_name=company_name,
        product_name=product_name
    )


# --- Обновление статуса модерации товара ---
@product.post('/update_moderation_status')
async def update_moderation_status(company_name: str, product_name: str, moderation_status: bool):
    product = await Product.get_or_none(
        company_name=company_name,
        product_name=product_name
    )

    if product:
        product.moderation = moderation_status
        await product.save()


# --- ФУНКЦИЯ получения данных товаров на модерации ---
def get_products_on_moderation(company_name=None):
    return Product.filter(moderation__isnull=True, company_name=company_name)

# --- ФУНКЦИЯ получения данных товаров прошедших модерацию ---
def get_products(company_name=None, moderation=None):
    return Product.filter(company_name=company_name, moderation=moderation)


# --- Получение данных всех товаров на модерации ---
@product.get('/get_all_products_on_moderation')
async def get_all_products_on_moderation():
    return await get_products_on_moderation()


# --- Получение данных всех товаров продавца на модерации ---
@product.get('/get_company_products_on_moderation')
async def get_company_products_on_moderation(company_name: str):
    return await get_products_on_moderation(company_name)


# --- Получение данных всех товаров в магазине ---
@product.get('/get_all_products')
async def get_all_products():
    return await get_products(moderation=True)


# --- Получение данных всех товаров продавца в магазине ---
@product.get('/get_company_products')
async def get_company_products(company_name: str):
    return await get_products(company_name=company_name, moderation=True)


# --- Получение данных всех отбракованных товара продавца на модерации ---
@product.get('/get_company_false_products_on_moderation')
async def get_company_false_products_on_moderation(company_name: str):
    return await get_products(company_name=company_name, moderation=False)
