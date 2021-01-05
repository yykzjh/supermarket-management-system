# coding:utf-8

from flask import (Flask, request, current_app, redirect, url_for, abort, Response, make_response,
    jsonify, session, g, render_template, flash, Blueprint)

from werkzeug.routing import BaseConverter
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField)
from wtforms.validators import (DataRequired, EqualTo)
from flask_cors import CORS



app = Flask(__name__,template_folder="../templates",static_folder="../static") # type:Flask

CORS(app,  resources={r"/*": {"origins": "*"}}, supports_credentials=True)