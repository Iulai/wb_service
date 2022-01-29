from webapp import create_app
from webapp.wb_orders_data import orders_for_date
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    orders_for_date(datetime.now() - timedelta(days=7))
