from pydantic import BaseModel
from typing import List, Optional

# API istek ve cevaplarında kullanılacak veri şemalarının  tanımlanma kısmıdır 

# user şemaları
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True

class User(UserBase):
    id: int

    class Config:
        from_attributes = True


# category şemaları
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# product şemaları 
class ProductBase(BaseModel):
    name: str
    price: int
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[int] = None
    category_id: Optional[int] = None

    class Config:
        from_attributes = True

from typing import Optional

class Product(ProductBase):
    id: int
    category_id: Optional[int] = None  

    class Config:
        from_attributes = True


# review şemaları 
class ReviewBase(BaseModel):
    text: str
    product_id: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class Config:
        from_attributes = True


# oreder şemaları 
class OrderBase(BaseModel):
    user_id: int

class OrderCreate(OrderBase):
    product_ids: List[int] = []

class OrderUpdate(OrderBase):
    product_ids: Optional[List[int]] = None

class Order(OrderBase):
    id: int
    products: List[Product] = []

    class Config:
        from_attributes = True
        

class ReviewUpdate(BaseModel):
    text: Optional[str] = None

class OrderDelete(BaseModel):  
    pass