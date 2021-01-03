from flask import Blueprint, request
from sqlalchemy import (or_, func)
from app.models import db


app_purchase_orders = Blueprint("app_purchase_orders", __name__)


