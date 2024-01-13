from fastapi import APIRouter
from datetime import datetime
from .schemas import CreateBuyerModel, CreateSellerModel, CreateQuestionToSupport, CreateAnswerQuestionToSupport, AddProductModel

admin = APIRouter()

