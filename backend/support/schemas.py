import pydantic

from typing import Optional


class CreateQuestionToSupport(pydantic.BaseModel):
    user_id: int
    question: str


class CreateAnswerQuestionToSupport(pydantic.BaseModel):
    user_id: int
    question: Optional[str]
    answer_username: Optional[str]
    answer: Optional[str]
