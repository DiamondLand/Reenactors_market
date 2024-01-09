import pydantic

from typing import Optional

class CreateSellerModel(pydantic.BaseModel):
    user_id: int
    company_name: str
    contact: str


class AddProductModel(pydantic.BaseModel):
    product_name: str
    product_description: str
    product_price: int
    product_category: str
    product_subcategory: str
    product_subsubcategory: Optional[str]
    product_image_url: Optional[str]
    company_name: str


class CreateBuyerModel(pydantic.BaseModel):
    user_id: int
    username: str
    privilege: str = 'buyer'
    #privilege: str = 'admin'


class CreateQuestionToSupport(pydantic.BaseModel):
    user_id: int
    question: str


class CreateAnswerQuestionToSupport(pydantic.BaseModel):
    user_id: int
    question: Optional[str]
    answer_username: Optional[str]
    answer: Optional[str]