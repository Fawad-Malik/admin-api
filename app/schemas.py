from pydantic import BaseModel
from typing import List
class CategorySchema(BaseModel):
    category_name : str

class ProductSchema(BaseModel):
    product_name : str
    product_description : str
    product_price : float
    category_id : int

class InventorySchema(BaseModel):
    product_id : int
    quantity : int

class SaleSchema(BaseModel):
    product_id: int 
    quantity: int

class ListSaleSchema(BaseModel):
    data: List[SaleSchema]
