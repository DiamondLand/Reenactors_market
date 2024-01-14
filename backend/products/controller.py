from fastapi import APIRouter
from .models import Product
from .schemas import AddProductModel

product = APIRouter()

# --- Добавление товара ---
@product.post('/add_product')
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


# --- Проверка на повторение товара ---
@product.get('/check_duplicate_product')
async def check_duplicate_product(company_name: str, product_name: str):
    existing_product = await Product.get_or_none(
        company_name=company_name,
        product_name=product_name
    )

    if existing_product:
        return True
    else:
        return False


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



# --- Получение данных всех товаров на модерации --- 
@product.get('/get_all_products_on_modering')
async def get_all_products_on_modering():
    products = await Product.filter(moderation__isnull=True)
    return products


# --- Получение данных всех товаров в магазине --- 
@product.get('/get_all_products')
async def get_all_products():
    products = await Product.filter(moderation=True)
    return products


# --- Получение данных всех товаров продавца на модерации --- 
@product.get('/get_company_products_on_modering')
async def get_company_products_on_modering(company_name: str):
    products = await Product.filter(moderation__isnull=True, company_name=company_name)
    return products


# --- Получение данных всех товаров в магазине от продавца--- 
@product.get('/get_company_products')
async def get_company_products(company: str):
    products = await Product.filter(company=company, moderation=True)
    return products


# --- Получение данных всех отбракованных товара продавца на модерации --- 
@product.get('/get_company_false_products_on_modering')
async def get_company_false_products_on_modering(company_name: str):
    products = await Product.filter(company_name=company_name, moderation=False)
    return products
