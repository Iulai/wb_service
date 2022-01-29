from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
#from webapp.db import Base, engine
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Articles(db.Model):
    __tablename__ = 'articles'

    article_id = db.Column(db.BigInteger, primary_key=True)  # Баркод
    barcode = db.Column(db.BigInteger, nullable=False)
    subject = db.Column(db.String(64), nullable=False)
    supplierArticle = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(64))
    brand = db.Column(db.String(64), nullable=False)
    techSize = db.Column(db.String(64))
    orders = relationship("Orders")

    def __repr__(self):
        return self.supplierArticle


class Orders(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.BigInteger, primary_key=True)
    article_id = db.Column(db.BigInteger, ForeignKey(Articles.article_id), index=True, nullable=False)
    number = db.Column(db.BigInteger, nullable=False)
    date = db.Column(db.Date, nullable=False)
    lastChangeDate = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    totalPrice = db.Column(db.Float, nullable=False)
    discountPercent = db.Column(db.Float)
    warehouseName = db.Column(db.String(64), nullable=False)
    oblast = db.Column(db.String(64), nullable=False)
    isCancel = db.Column(db.Boolean, nullable=False)
    cancel_dt = db.Column(db.String(64))
    price = db.Column(db.Float, nullable=False)
    week = db.Column(db.Integer)
    weekday = db.Column(db.String(32))
    articles = relationship("Articles", lazy="joined")

    def __repr__(self):
        return f'Order id: {self.order_id}, article: {self.article_id}'
