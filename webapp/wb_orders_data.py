from sqlalchemy.dialects.mysql import insert
from flask import current_app
from webapp.model import db, Articles, Orders
import requests
from datetime import datetime, date, timedelta


def orders_for_date(date_from):
    orders_url = current_app.config["BASE_URL"] + "/api/v1/supplier/orders"
    params = {
        'key': current_app.config["API_KEY"],
        'dateFrom': date_from,
        'flag': 0
    }
    try:
        result = requests.get(orders_url, params=params)
        result.raise_for_status()  # Этот вызов Автоматически генерирует исключение если сервер ответил 4хх или 5хх кодом
        orders = result.json()
        for row in orders:
            save_result(row)
    except (requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def save_result(row):
    weekdays = {1: "Monday",
                2: "Tuesday",
                3: "Wednesday",
                4: "Thursday",
                5: "Friday",
                6: "Saturday",
                7: "Sunday"}
    article = insert(Articles).values(article_id=row['barcode'], subject=row['subject'],
                                      supplierArticle=row['supplierArticle'], brand=row['brand'],
                                      category=row['category'], barcode=row['barcode'], techSize=row['techSize'])

    upd_article = article.on_duplicate_key_update(article_id=row['barcode'], subject=row['subject'],
                                                  supplierArticle=row['supplierArticle'], brand=row['brand'],
                                                  category=row['category'], techSize=row['techSize'])

    order = insert(Orders).values(order_id=row['number'], article_id=row['barcode'], number=row['number'],
                                  date=row['date'], lastChangeDate=row['lastChangeDate'], quantity=row['quantity'],
                                  totalPrice=row['totalPrice'], discountPercent=row['discountPercent'],
                                  warehouseName=row['warehouseName'], oblast=row['oblast'],
                                  isCancel=row['isCancel'], cancel_dt=row['cancel_dt'],
                                  price=row['totalPrice']-(row['discountPercent']/100*row['totalPrice']),
                                  week=datetime.strptime(row['date'][0:10], '%Y-%m-%d').isocalendar()[1],
                                  weekday=weekdays[datetime.strptime(row['date'][0:10], '%Y-%m-%d').isoweekday()])

    upd_order = order.on_duplicate_key_update(order_id=row['number'], article_id=row['barcode'],
                                              lastChangeDate=row['lastChangeDate'], quantity=row['quantity'],
                                              isCancel=row['isCancel'], cancel_dt=row['cancel_dt'],
                                              price=row['totalPrice']-(row['discountPercent']/100*row['totalPrice']),
                                              week=datetime.strptime(row['date'][0:10], '%Y-%m-%d').isocalendar()[1],
                                              weekday=weekdays[datetime.strptime(row['date'][0:10],
                                                                                 '%Y-%m-%d').isoweekday()])
    db.session.execute(upd_article)
    db.session.execute(upd_order)
    db.session.commit()
