import pydantic

from typing import Optional


class CreateSellerModel(pydantic.BaseModel):
    user_id: int
    company_name: str
    contact: str


class CreateBuyerModel(pydantic.BaseModel):
    user_id: int
    username: str
    privilege: str = None


class CreateQuestionToSupport(pydantic.BaseModel):
    user_id: int
    question: str


class CreateAnswerQuestionToSupport(pydantic.BaseModel):
    user_id: int
    question: Optional[str]
    answer_username: Optional[str]
    answer: Optional[str]
