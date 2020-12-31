from flask import (Flask, request, current_app, redirect, url_for, abort, Response, make_response,
    jsonify, session, g, render_template, flash)
from werkzeug.routing import BaseConverter
import json
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField)
from wtforms.validators import (DataRequired, EqualTo)


app=Flask(__name__) 



@app.route('/')      
def first_flask():    
    return 'Hello World'

@app.route('/index',methods=["GET","POST"])
def index():
    # name = request.form.get("name")
    # age = request.form.get("age")
    city = request.args.get("city")
    data = request.json.get("name")

    return "city=%s , data=%s" % (city, data)


if __name__ == '__main__':
    app.run(debug=True)         

    