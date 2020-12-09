import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model, reflect tables
base = automap_base()
base.prepare(engine, reflect=True)

# Save references to tables
station = base.classes.station
measurement = base.classes.measurement

session = Session(engine)

#define max_date (again) - for the query below

max_date=session.query(measurement.date).order_by((measurement.date).desc()).first()
max_date = dt.datetime.strptime(max_date[0], '%Y-%m-%d')

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """Available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prc = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= max_date-dt.timedelta(days=365)).group_by(measurement.date).all()
    return jsonify(prc)

@app.route("/api/v1.0/stations")
def stations():
    stn = session.query(station.name, station.station).all()
    return jsonify(stn)

@app.route("/api/v1.0/tobs")
def tobs():
    tbs = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= max_date-dt.timedelta(days=365)).group_by(measurement.date).all()

    return jsonify(tbs)


@app.route("/api/v1.0/<start>")
def start_date(start):
    temp_from_date = session.query(func.min(measurement.tobs), func.max(measurement.tobs,  func.avg(measurement.tobs))).\
    filter(measurement.date >= start).all()
    return jsonify(temp_from_date)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    temp_from_to_date = session.query(func.min(measurement.tobs), func.max(measurement.tobs,  func.avg(measurement.tobs))).\
    filter(measurement.date >= start).\
    filter(measurement.date <= end).all()
    return jsonify(temp_from_to_date)

if __name__ == '__main__':
    app.run(debug=True)