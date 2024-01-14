import pydantic


class CreateSellerModel(pydantic.BaseModel):
    user_id: int
    company_name: str
    contact: str


class CreateBuyerModel(pydantic.BaseModel):
    user_id: int
    username: str
    #privilege: str = 'buyer'
    privilege: str = 'admin'
