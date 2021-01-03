from flask import Blueprint, request
from sqlalchemy import (or_, func)
from app.models import db


app_on_sales = Blueprint("app_on_sales", __name__)


