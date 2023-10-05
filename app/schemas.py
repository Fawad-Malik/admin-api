from datetime import datetime
from typing import List
from pydantic import BaseModel

class CategorySchema(BaseModel):
    category_name : str

class ProductSchema(BaseModel):
    product_name : str
    product_description : str
    product_price : float
    category_id : int

class InventorySchema(BaseModel):
    product_id = int
    quantity = int

class SaleSchema(BaseModel):
    product_ids= List[int]