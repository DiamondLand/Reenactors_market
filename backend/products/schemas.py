import pydantic

from typing import Optional


class AddProductModel(pydantic.BaseModel):
    product_name: str
    product_description: str
    product_price: int
    product_category: str
    product_subcategory: str
    product_subsubcategory: str
    product_image_url: Optional[str]
    company_name: str