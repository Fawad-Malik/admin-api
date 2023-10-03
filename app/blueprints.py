from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .settings import get_db

router = APIRouter()

@router.get('/product', status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    products = db.query(models.Product).filter(
        models.Product.product_name.contains(search)).limit(limit).offset(skip).all()
    return {"status": "success", 'total_products': len(products), 'products': products}

@router.post('/product', status_code=status.HTTP_201_CREATED)
def add_product(payload: schemas.ProductSchema, db: Session = Depends(get_db)):
    product = models.Product(**payload.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"status": "success", "product_id": product.product_id}

@router.get('/inventory', status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    query = db.query(models.Inventory).join(models.Product, models.Inventory.product_id == models.Product.product_id)
    inventories = query.add_columns(models.Inventory.inventory_id, models.Product.product_name, models.Inventory.quantity).limit(limit).offset(skip).all()
    return {"status": "success", 'total_inventories': len(inventories), 'products': inventories}

@router.post('/inventory', status_code=status.HTTP_201_CREATED)
def add_inventory(product_id: int, payload: schemas.InventorySchema, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No product with this id: {product_id} found')
    inventory = models.Inventory(**payload.dict())
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return {"status": "success", "inventory_id": inventory.inventory_id}

@router.patch('/inventory')
def update_inventory(inventory_id: int, payload: schemas.NoteBaseSchema, db: Session = Depends(get_db)):
    inventory_query = db.query(models.Inventory).filter(models.Inventory.inventory_id == inventory_id)
    inventory = inventory_query.first()
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No inventory with this id: {inventory_id} found')
    update_data = payload.dict(exclude_unset=True)
    inventory_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(inventory)
    return {"status": "success", "inventory": inventory.inventory_id}