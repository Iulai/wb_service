from datetime import datetime
from sqlalchemy.sql import func
from db import db_session
from collections import Counter
import time
from webapp.model import db, Articles, Orders


def prices():
    items_price = OrderData.query.order_by(OrderData.totalPrice)

    for p in items_price:
        print(f'Цены {p.totalPrice}')


def items_by_article(article):
    items = OrderData.query.filter(OrderData.supplierArticle == article)
    counter = 0
    for p in items:
        counter += 1
    print(f'Заказ с артикулом {p.number} {counter} штук')


def orders_in_day(day):
    orders = Orders.query.filter(Orders.date == day)
    counter = 0
    number = []
    for p in orders:
        number.append(p.supplierArticle)
    print(f'Общее количество заказов за данный период {len(number)}')
    print(f'Количество заказов по позициям {Counter(number)}')


if __name__ == '__main__':
    start = time.time()
    orders_in_day(datetime.now().strftime('%Y-%m-%d'))
    print(f'Загрузка заняла {time.time() - start} сек')