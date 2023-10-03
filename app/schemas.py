from datetime import datetime
from typing import List
from pydantic import BaseModel


class ProductSchema(BaseModel):
    product_name : str
    product_description : str
    product_price : float
    category_id : int


class InventorySchema(BaseModel):
    product_id = int
    quantity = int
