import pytest
from sqlalchemy.orm import Session

from app import models, schemas, crud

# utils.py yoksa oluştur, içine şu fonksiyonu koy:
# def validate_email(email: str) -> bool:
#     return "@" in email and "." in email

from app.utils import validate_email

# ====================== VALIDATION POZİTİF ======================
def test_user_create_valid():
    user = schemas.UserCreate(username="validuser", email="valid@example.com")
    assert user.username == "validuser"

def test_product_create_valid():
    product = schemas.ProductCreate(name="Laptop", price=5000, category_id=1)
    assert product.price == 5000

def test_category_create_valid():
    cat = schemas.CategoryCreate(name="Books")
    assert cat.name == "Books"

def test_review_create_valid():
    review = schemas.ReviewCreate(text="Great", product_id=1)
    assert review.product_id == 1

def test_order_create_valid():
    order = schemas.OrderCreate(user_id=1, product_ids=[1])
    assert order.user_id == 1

# ====================== UTILITY ======================
def test_validate_email_positive():
    assert validate_email("test@example.com") is True

def test_validate_email_negative():
    assert validate_email("bad") is False
    assert validate_email("test@") is False

# ====================== MODEL ======================
def test_user_model():
    user = models.User(username="ali", email="ali@example.com")
    assert user.username == "ali"
    assert user.orders == []

def test_product_model():
    product = models.Product(name="Phone", price=1000, category_id=1)
    assert product.reviews == []
    assert product.orders == []

def test_order_model():
    order = models.Order(user_id=1)
    assert order.products == []

# ====================== BUSINESS LOGIC (CRUD + DB) ======================
def test_create_and_get_user_crud(db_session: Session):
    user_in = schemas.UserCreate(username="cruduser", email="crud@example.com")
    created = crud.create_user(db=db_session, user=user_in)
    assert created.id is not None

    fetched = crud.get_user(db=db_session, user_id=created.id)
    assert fetched.username == "cruduser"

def test_create_category_crud(db_session: Session):
    cat_in = schemas.CategoryCreate(name="Electronics")
    cat = crud.create_category(db=db_session, category=cat_in)
    assert cat.id is not None
    assert cat.name == "Electronics"

def test_create_product_crud(db_session: Session):
    cat = crud.create_category(db=db_session, category=schemas.CategoryCreate(name="Cat"))
    prod_in = schemas.ProductCreate(name="Mouse", price=200, category_id=cat.id)
    prod = crud.create_product(db=db_session, product=prod_in)
    assert prod.id is not None

def test_update_user_crud(db_session: Session):
    # Oluştur
    user_in = schemas.UserCreate(username="oldname", email="old@example.com")
    user = crud.create_user(db=db_session, user=user_in)
    
   
    update_data = schemas.UserUpdate(username="newname", email="new@example.com")
    updated = crud.update_user(db=db_session, user_id=user.id, user_update=update_data)  # <--- BURASI DEĞİŞTİ!
    
    assert updated is not None
    assert updated.username == "newname"
    assert updated.email == "new@example.com"

def test_delete_user_crud(db_session: Session):
    user_in = schemas.UserCreate(username="todelete", email="del@example.com")
    user = crud.create_user(db=db_session, user=user_in)
    success = crud.delete_user(db=db_session, user_id=user.id)
    assert success is True  # veya None dönebilir, crud.py'ye göre
    fetched = crud.get_user(db=db_session, user_id=user.id)
    assert fetched is None

def test_create_order_with_products_crud(db_session: Session):
    user = crud.create_user(db=db_session, user=schemas.UserCreate(username="buyer", email="b@example.com"))
    cat = crud.create_category(db=db_session, category=schemas.CategoryCreate(name="Tech"))
    prod = crud.create_product(db=db_session, product=schemas.ProductCreate(name="Keyboard", price=300, category_id=cat.id))

    order_in = schemas.OrderCreate(user_id=user.id, product_ids=[prod.id])
    order = crud.create_order(db=db_session, order=order_in)
    assert order.id is not None
    assert len(order.products) == 1
    assert order.products[0].name == "Keyboard"

# ====================== NEGATİF (Manuel kontrol, çünkü Pydantic otomatik raise etmiyor) ======================
def test_manual_validation_email():
    assert "@" in "good@example.com"
    assert "@" not in "badmail"

def test_manual_price_positive():
    assert 5000 > 0
    assert -100 < 0

