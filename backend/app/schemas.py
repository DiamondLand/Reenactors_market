import pydantic

from typing import Optional

class CreateSellerModel(pydantic.BaseModel):
    user_id: int
    username: str
    company_name: str
    phone_number: str
    sold: int = 0


class CreateBuyerModel(pydantic.BaseModel):
    user_id: int
    username: str
    purchased: int = 0
    privilege: str = None


class CreateQuestionToSupport(pydantic.BaseModel):
    user_id: int
    question: str


class CreateAnswerQuestionToSupport(pydantic.BaseModel):
    answer_username: Optional[str]
    answer: Optional[str]