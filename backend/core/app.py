from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.db import init_db
from admin.controller import admin
from products.controller import product
from register.controller import reg
from support.controller import support

app = FastAPI()
init_db(app)


app.include_router(admin, tags=['Admin'])
app.include_router(product, tags=['Product'])
app.include_router(reg, tags=['Register'])
app.include_router(support, tags=['Support'])


# --- Добавление middleware для обработки CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.title = 'Recons Bot'
app.description = f'''Backend developer tg/vk @ivan_abutkov\n
Count of routes: {len(app.routes)}\n'''