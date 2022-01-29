from flask import Flask, render_template
from webapp.model import db, Articles, Orders
from datetime import datetime
from sqlalchemy import func


def create_app():
    app = Flask(__name__)  # Создаем flask приложение (__name__ - имя текущего файла)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')  # Привязываем функцию обрабодчик к пути на сайте
    def index():
        title = 'Отчет по заказам'
        orders_sum = db.session.query(func.sum(Orders.price).label('total')).filter(
            Orders.week == datetime.now().isocalendar()[1]).group_by(Orders.weekday).order_by('weekday')
        orders_data = Orders.query.filter(Orders.week == datetime.now().isocalendar()[1])

        return render_template('index.html', page_title=title, orders=orders_data, orders_sum=orders_sum)
    return app
