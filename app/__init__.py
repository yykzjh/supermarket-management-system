from app.models import db
from app.config import app

from app.controller_api.Users import app_users
from app.controller_api.Goods import app_goods
from app.controller_api.HistoryOders import app_history_orders
from app.controller_api.OnSales import app_on_sales
from app.controller_api.PurchaseOders import app_purchase_orders
from app.controller_api.Stocks import app_stocks
from app.controller_api.Suppliers import app_suppliers


app.register_blueprint(app_goods, url_prefix="/Goods")
app.register_blueprint(app_history_orders, url_prefix="/HistoryOrders")
app.register_blueprint(app_on_sales, url_prefix="/OnSales")
app.register_blueprint(app_purchase_orders, url_prefix="/PurchaseOrders")
app.register_blueprint(app_stocks, url_prefix="/Stocks")
app.register_blueprint(app_suppliers, url_prefix="/Suppliers")
app.register_blueprint(app_users, url_prefix="/Users")