from flask import Flask, jsonify
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


engine= create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page....")
    return(
        f"Wecome to the 'Home' page<br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def percipitation():
    prcp = session.query(Measurement.date, Measurement.prcp).all()
    all_prcp = []
    for x in prcp:
        x_dict = {}
        x_dict[x.date] = x.prcp
        all_prcp.append(x_dict)
    
    return jsonify(all_prcp)

    

@app.route("/api/v1.0/stations")
def station():
    stations = session.query(Measurement.station).distinct().all()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temperature():
    last_date_query = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    last_date = last_date_query.date

    year_ago = (dt.datetime.strptime(last_date,'%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= year_ago).all()
    tobs = list(np.ravel(results))
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start,end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)