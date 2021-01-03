from flask import Blueprint, request
from sqlalchemy import (or_, func)
from app.models import db


app_stocks = Blueprint("app_stocks", __name__)


