import datetime
from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .settings import get_db
from sqlalchemy import and_

router = APIRouter()

@router.get('/category', status_code=status.HTTP_200_OK)
def get_categories(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    categories = db.query(models.Category)
    if search:
        categories = categories.filter(models.Category.category_name.contains(search))
    categories = categories.limit(limit).offset(skip).all()
    return {"status": "success", 'total_categories': len(categories), 'categories': categories}

@router.post('/category', status_code=status.HTTP_201_CREATED)
def add_category(payload: schemas.CategorySchema, db: Session = Depends(get_db)):
    category = models.Category(**payload.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return {"status": "success", "category_id": category.category_id}

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
def get_inventories(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    query = db.query(models.Inventory).join(models.Product, models.Inventory.product_id == models.Product.product_id)
    if search:
        query = query.filter(models.Product.product_name.contains(search))
    inventories = query.add_columns(models.Inventory.inventory_id, models.Product.product_name, models.Inventory.quantity).limit(limit).offset(skip).all()
    return {"status": "success", 'total_inventories': len(inventories), 'products': inventories}

@router.post('/inventory', status_code=status.HTTP_201_CREATED)
def add_inventory(payload: schemas.InventorySchema, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No product with this id: {payload.product_id} found')
    # check if inventory entry exists against current product if not create it and update it if exists
    chk_inventory = product.inventory
    if not chk_inventory:
        inventory = models.Inventory(product_id=payload.product_id)
        db.add(inventory)
        db.flush()
        inventory_log = models.InventoryLog(inventory_id=inventory.inventory_id, new_quantity=payload.quantity) 
    else:
        inventory_id, old_quantity = chk_inventory[-1].inventory_id, chk_inventory[-1].new_quantity
        new_quantity = old_quantity + new_quantity
        inventory_log = models.InventoryLog(inventory_id = inventory_id, old_quantity= old_quantity, new_quantity=new_quantity)
    db.add(inventory_log)
    db.commit()
    db.refresh(inventory)
    return {"status": "success", "inventory_id": inventory.inventory_id}

# I have to fix this endpoint by tomorrow
# @router.post('/sale', status_code=status.HTTP_201_CREATED)
# def add_sale(payload: schemas.ListSaleSchema, db: Session = Depends(get_db)):
#     params = payload.data
#     products = db.query(models.Product).filter(models.Product.product_id.in_(payload.product_ids)).all()
#     if len(payload.data) != len(products):
#         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                             detail='Please provide valid parameters')
#     for param in params:
#         if param.product_id in products:
#             pass
#     products = db.query(models.Product).filter(models.Product.product_id.in_(payload.product_ids)).all()
#     total_price = 0
#     for product in products:
#         total_price += product.product_price
#     sale = models.Sale(total_price=total_price)
#     db.add(sale)
#     sale.products = products
#     db.commit()
#     db.refresh(sale)
#     return {"status": "success", "sale_id": sale.sale_id}

@router.get('/sale', status_code=status.HTTP_200_OK)
def get_saless(db: Session = Depends(get_db), product_id: int=0, category_id: int=0, start_date: str ='', end_date: str = ''):
    qry = db.query(models.Product).join(models.Category, models.Product.category_id==models.Category.category_id)
    qry = qry.join(models.sale_products, models.Product.product_id==models.sale_products.product_id)
    qry = qry.join(models.Sale, models.sale_products.sale_id==models.Sale.sale_id)
    if product_id:
        qry = qry.filter(models.Product.product_id == product_id)
    if category_id:
        qry = qry.filter(models.Category.category_id == category_id)
    if start_date and end_date:
        qry = qry.filter(models.Sale.sale_date>=start_date, models.Sale.sale_date<=end_date)
    products = qry.all()
    result = []
    for product in products:
        result.append({"product_id": product.product_id, "product_name": product.product_name, "category_id": product.category_id, "category_name": product.category_name})
    return {"status": "success", 'products': result}

@router.get('/stock-alert', status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    qry = db.query(models.Product).join(models.Inventory, models.Product.product_id==models.Inventory.product_id)
    qry = qry.filter(models.Inventory.product_quantity <= 10).limit(limit).offset(skip).all()
    products = qry.limit(limit).offset(skip).all()
    return {"status": "success", 'total_products': len(products), 'products': products}

@router.get('/analyze-revenue', status_code=status.HTTP_200_OK)
def analyze_revenue(db: Session = Depends(get_db), start_date: str = '', end_date: str=''):
    if not start_date:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail='Please provide valid parameters')
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%m-%d-%Y').date()
        end_date = datetime.strptime(end_date, '%m-%d-%Y').date()
        qry = db.query(models.Sale).filter(and_(models.Sale.sale_date >= start_date, models.Sale.sale_date <= end_date))
    else:
        start_date = datetime.strptime(start_date, '%m-%d-%Y').date()
        qry = db.query(models.Sale).filter(and_(models.Sale.sale_date == start_date))
    total_revenue = qry.sum(models.Sale.sale_price)
    return {"status": "success", 'revenue': total_revenue}

@router.get('/compare-revenue', status_code=status.HTTP_200_OK)
def compare_revenue(db: Session = Depends(get_db), start_date: str = '', end_date: str='', first_category: int=0, second_category: int=0):
    start_date = datetime.strptime(start_date, '%m-%d-%Y').date()
    end_date = datetime.strptime(end_date, '%m-%d-%Y').date()
    if not start_date or not end_date or not first_category or not second_category:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail='Please provide valid parameters')
    base_qry = db.query(models.sale_products).join(models.Sale, models.sale_products.sale_id==models.Sale.sale_id).join(models.Product, models.sale_products.product_id == models.Product.product_id).join(models.Category, models.Product.category_id == models.Category.category_id)
    first_category_revenue = base_qry.filter(and_(models.Category.category_id == first_category, models.Sale.sale_date >= start_date, models.Sale.sale_date <= end_date))
    first_category_revenue = first_category_revenue.sum(models.Product.product_price * models.sale_products.quantity)
    second_category_revenue = base_qry.filter(and_(models.Category.category_id == first_category, models.Sale.sale_date >= start_date, models.Sale.sale_date <= end_date))
    second_category_revenue = second_category_revenue.sum(models.Product.product_price * models.sale_products.quantity)
    return {"status": "success", 'first_category_revenue': first_category_revenue}
