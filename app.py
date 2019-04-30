from flask import Flask, jsonify
import numpy as np
import pandas as pd 
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
engine = create_engine("sqlite:///C:/Users/KerwinH/Documents/Data Analytics/Homework/Advanced Data Retrieval/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app=Flask(__name__)
@app.route("/")
def welcome():
    return(
    f"Welcome to the Climate App!<br>"
    f"Here are all available routes<br>"
    f"/api/v1.0/precipitation<br>"
    f"/api/v1.0/stations<br>"
    f"/api/v1.0/tobs<br>"
    f"/api/v1.0/<start><br>"
    f"/api/v1.0/<start>/<end>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    results= session.query(Measurement.date, Measurement.prcp).all()
    all_precipitation=[]
    for date, prcp in results:
        precipitation_dict={}
        precipitation_dict["date"]=date
        precipitation_dict["prcp"]=prcp
        all_precipitation.append(precipitation_dict)
    
    return jsonify(all_precipitation)
    
@app.route("/api/v1.0/stations")
def stations():
    results=session.query(Station.station).group_by(Station.station).all()
    all_stations=list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    temperature_data=[]
    results=session.query(Measurement.tobs).filter(Measurement.date<='2017-08-23').filter(Measurement.date>='2016-08-23').all()
    temperature_data=list(np.ravel(results))
    return jsonify(temperature_data)

@app.route("/api/v1.0/start")
def start(start_date):
    temp_data=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date>= start_date)
    return jsonify(temp_data)


if __name__ == '__main__':
    app.run(debug=True)