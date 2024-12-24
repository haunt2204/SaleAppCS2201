from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from saleapp import app, db
from flask_login import UserMixin
from enum import Enum as RoleEnum
from datetime import datetime

class UserEnum(RoleEnum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    avatar = Column(String(200), default="https://res.cloudinary.com/dy1unykph/image/upload/v1729842193/iPhone_15_Pro_Natural_1_ltf9vr.webp")
    role = Column(Enum(UserEnum), default=UserEnum.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        self.name


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, default=0)
    image = Column(String(200), default="https://res.cloudinary.com/dy1unykph/image/upload/v1729842193/iPhone_15_Pro_Natural_1_ltf9vr.webp")
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    active = Column(Boolean, default=True)
    details = relationship('ReceiptDetail', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())


class Receipt(Base):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref="receipt", lazy=True)


class ReceiptDetail(Base):
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0.0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


class Comment(Base):
    content = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # c1 = Category(name="Mobile")
        # c2 = Category(name="Laptop")
        # c3 = Category(name="Tablet")
        # db.session.add_all([c1,c2,c3])
        # db.session.commit()
        # import json
        # with open('data/products.json', encoding='utf-8') as f:
        #     products = json.load(f)
        #     for p in products:
        #         prod = Product(**p)
        #         db.session.add(prod)
        #
        # import hashlib
        #
        # password = str(hashlib.md5("123".encode('utf-8')).hexdigest())
        #
        # u = User(name="Hau Nguyen", username="user", password=password)
        # u2 = User(name="Hau Nguyen", username="admin", password=password, role=UserEnum.ADMIN)
        # db.session.add(u)
        # db.session.add(u2)
        # db.session.commit()

