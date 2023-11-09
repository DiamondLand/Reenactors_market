import pydantic


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
    question_date: str
    answer_user_id: int = None
    answer: str = None
    answer_date: str = None