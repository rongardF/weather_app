'''
Created on 6. nov 2022

@author: User
'''

import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///weather.db"
app.config["DEBUG"]=True

db=SQLAlchemy(app)

class City(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), nullable=False)

@app.route("/",  methods=["GET", "POST"])
def index():
    if request.method=="POST": # if user entered into form
        new_city=request.form.get("city") # get the user entered name
        if new_city: # check that inserted city exsist
            new_city_obj=City(name=new_city) # add new city into database
            db.session.add(new_city_obj)
            db.session.commit()
        
    cities = City.query.all()
    
    url='https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=bdb6d2c126afb08f855eb1e6cce28b6e'
    weather_data=[]
    
    for city in cities:
        r=requests.get(url.format(city.name)).json() # get data from API

        weather={'city': city.name ,"temperature": r["main"]["temp"], "description": r["weather"][0]["description"],"icon": r["weather"][0]["icon"]} # extract data
        weather_data.append(weather)
        
    return render_template("weather.html", weather_data=weather_data) # insert data into template and render