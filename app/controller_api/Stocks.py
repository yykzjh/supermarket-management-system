from flask import Blueprint, request
from sqlalchemy import (or_, func)

app_stocks = Blueprint("app_stocks", __name__)