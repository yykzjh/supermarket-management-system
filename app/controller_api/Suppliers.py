from flask import Blueprint, request
from sqlalchemy import (or_, func)

app_suppliers = Blueprint("app_suppliers", __name__)