from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base
# veri tabanı tablolarını ve aralarındaki ilişkileri SQLAlchemy ORM ile tanımlama kısmı burada gerçekleşicektir

# Order ile Product arasındaki many-to-many ilişki tablosu
order_product_association = Table(
    'order_product',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)
# User tablosu: kullanıcı bilgilerini tutar, bir kullanıcının birden fazla siparişi olabilecktir

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    orders = relationship("Order", back_populates="user")

 # Category tablosu: ürün kategorilerini tutacaktır

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    products = relationship("Product", back_populates="category")

# Product tablosu: ürün bilgilerini tutacaktır. Kategori, yorum ve siparişlerle ilişkilidir 

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")
    reviews = relationship("Review", back_populates="product")
    orders = relationship("Order", secondary=order_product_association, back_populates="products")

# Review tablosu: Ürünlere yapılan yorumları tutacak

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))

    product = relationship("Product", back_populates="reviews")

# Order tablosu: Kullanıcıya ait siparişleri tutacaktır ve ürünlerle many to many ilişkilidir

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="orders")
    products = relationship("Product", secondary=order_product_association, back_populates="orders")