# Import the dependencies.
import numpy as np
import pandas as pd
import json

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request

#################################################
# Database Setup
#################################################

# Create engine using the `DataApi.db` database file
engine = create_engine("sqlite:///db/DataApi.db")

# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the variables to represent the database tables
CountryContinent = Base.classes.CountryContinent
PopulationGrowth = Base.classes.PopulationGrowth

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<h1>Welcome to the Global Data Analysis API</h1>"
        f"<h2>Available Routes:</h2>"

        f"<p><b>/api/v1.0/country-codes</b></br>\
        All country codes sorted alphabetically</p>"

        f"<p><b>/api/v1.0/continents-with-countries</b></br>\
        All continents and countries in them, sorted alphabetically by the respective names</p>"

        f"<p><b>/api/v1.0/population-growth-all-countries-all-years</b></br>\
        A cross-tabulation of population growth percentage by country, by year for all available years</p>"
    )

#------------------------------------------------

@app.route("/api/v1.0/country-codes")
def country_codes():
    """Return a list of all country codes sorted alphabetically"""
    # Query for country codes
    session = Session(bind=engine)
    country_tuples = session.query(CountryContinent.CountryCode).order_by(CountryContinent.CountryCode).all()
    session.close()

    # Convert list of tuples into normal list
    country_codes = list(np.ravel(country_tuples))

    # Return result in JSON format
    return jsonify(country_codes)

#------------------------------------------------

@app.route("/api/v1.0/continents-with-countries")
def continents_with_countries():
    """Return a list of all continents and countries in them, sorted alphabetically by the respective names"""
    # Query for continent/country information
    # NOTE: we use the country name from the population growth table, so that name is consistent with other country name values
    # returned from other endpoints in this API.
    session = Session(bind=engine)
    result_records = session.query(CountryContinent.Continent, PopulationGrowth.CountryName, CountryContinent.CountryCode)\
                            .join(PopulationGrowth, CountryContinent.CountryCode == PopulationGrowth.CountryCode)\
                            .order_by(CountryContinent.Continent, PopulationGrowth.CountryName)\
                            .all()
    session.close()

    # Convert tuples to dataframe taking on column names from the query
    result_df = pd.DataFrame(result_records)

    # Convert to a dictionary and return result
    return result_df.to_dict(orient="records")

#------------------------------------------------

@app.route("/api/v1.0/population-growth-all-countries-all-years")
def population_growth_all():
    """Return a cross-tabulation of population growth percentage by country, by year for all available years"""

    # Query all population growth data
    session = Session(bind=engine)
    population_growth_records = session.query(PopulationGrowth).all()
    session.close()

    # Dynamically convert query results into an equivalent dictionary
    # Reference: https://www.slingacademy.com/article/sqlalchemy-convert-query-results-into-dictionary/
    result_dict = [{column.name: getattr(row, column.name) for column in PopulationGrowth.__table__.columns} for row in population_growth_records]

     # Return result in JSON format
    return result_dict

#------------------------------------------------

# @app.route("/api/v1.0/precipitation")
# def precipitation():
#     """Return all precipitation measurements for the last year of data sorted by date"""

#     session = Session(bind=engine)

#     # Find the most recent measurement date in the data set
#     most_recent_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
#     last_date = dt.date.fromisoformat(most_recent_date_str[0])

#     # Calculate the date one year from the last date in data set
#     one_year_before_last_date = last_date + relativedelta(years=-1)

#     # Query all precipitation for the last year of data
#     precipitation_tuples = session.query(Measurement.date, Measurement.prcp)\
#                             .filter(Measurement.date.between(one_year_before_last_date, last_date))\
#                             .all()
#     session.close()

#     # Convert tuples to dataframe taking on column names 'date' and 'prcp' from the query
#     precipitation_df = pd.DataFrame(precipitation_tuples)

#     # Replace NaN values with zero
#     precipitation_df["prcp"] = precipitation_df["prcp"].fillna(0)

#     # Sort results by date
#     precipitation_df = precipitation_df.sort_values(by=["date"])

#     # Convert to a dictionary and return result
#     return precipitation_df.to_dict(orient="records")

#------------------------------------------------

# @app.route("/api/v1.0/stations")
# def stations():
#     """Return a list of all measurement station identifiers sorted alphabetically"""
#     # Query for station names
#     session = Session(bind=engine)
#     station_tuples = session.query(Station.station).order_by(Station.station).all()
#     session.close()

#     # Convert list of tuples into normal list
#     stations = list(np.ravel(station_tuples))

#     # Return result in JSON format
#     return jsonify(stations)

#------------------------------------------------

# @app.route("/api/v1.0/tobs")
# def tobs():
#     """Return temperature observations of the most-active station for the last year of data"""

#     session = Session(bind=engine)

#     # Determine the most active station
#     most_active_station_tuple = session.query(Station.station, func.count(Measurement.station))\
#         .join(Measurement, Station.station == Measurement.station)\
#         .group_by(Station.station)\
#         .order_by(func.count(Measurement.station).desc())\
#         .first()

#     most_active_station_id = most_active_station_tuple[0]

#     # Find the most recent observation date for this station
#     most_recent_date_str = session.query(func.max(Measurement.date))\
#         .filter(Measurement.station == most_active_station_id)\
#         .one()

#     # Convert to a date type and calculate the date one year earlier
#     last_date = dt.date.fromisoformat(most_recent_date_str[0])
#     one_year_before_last_date = last_date + relativedelta(years=-1)

#     # Define a query to retrieve the temperature observation data for this station
#     last12months_tobs_tuples = session.query(Measurement.tobs)\
#                                 .filter(Measurement.date.between(one_year_before_last_date, last_date))\
#                                 .filter(Measurement.station == most_active_station_id)\
#                                 .all()

#     session.close()

#     # Convert list of tuples into normal list
#     last12months_tobs = list(np.ravel(last12months_tobs_tuples))

#     # Return result in JSON format
#     return jsonify(last12months_tobs)

#------------------------------------------------

# @app.route("/api/v1.0/<start>")
# def min_avg_max_temperatures_from(start):
#     """Calculate MIN, AVG, and MAX temperature for all dates greater than or equal to the specified start date."""
#     try:
#         # Convert the supplied start date from string to date type
#         start_date = dt.date.fromisoformat(start)
#     except:
#         # Date conversion error: return error description to the caller; set HTTP status code 400 'Bad request'
#         return {"error": f"Start date {start} is not a valid date in yyyy-mm-dd format"}, 400
#     else:
#         # Calculate the min/avg/max temperature statistics for observations from the given start date (inclusive)
#         session = Session(bind=engine)
#         tobs_statistics_tuple = session.query(func.min(Measurement.tobs).label("TMIN"),\
#                                               func.avg(Measurement.tobs).label("TAVG"),\
#                                               func.max(Measurement.tobs).label("TMAX"))\
#                                 .filter(Measurement.date >= start_date)\
#                                 .all()
#         session.close()

#         # Convert tuple to dataframe taking on column names from the query
#         tobs_statistics_df = convert_min_avg_max_query_result_to_dataframe(tobs_statistics_tuple)

#         # Return result in JSON format
#         return format_min_avg_max_temperatures_as_json(tobs_statistics_df)

#------------------------------------------------

# @app.route("/api/v1.0/<start>/<end>")
# def min_avg_max_temperatures_from_to(start, end):
#     """Calculate MIN, AVG, and MAX temperature for all dates from the specified start date to the specified end date, inclusive."""
#     try:
#         # Convert the supplied dates from string to date type
#         start_date = dt.date.fromisoformat(start)
#         end_date = dt.date.fromisoformat(end)
#     except:
#         # Date conversion error: return error description to the caller; set HTTP status code 400 'Bad request'
#         return {"error": f"Start date {start} and/or End date {end} is not a valid date in yyyy-mm-dd format"}, 400
#     else:
#         # Calculate the min/avg/max temperature statistics for observations from the given start date to end date (inclusive)
#         session = Session(bind=engine)
#         tobs_statistics_tuple = session.query(func.min(Measurement.tobs).label("TMIN"),\
#                                               func.avg(Measurement.tobs).label("TAVG"),\
#                                               func.max(Measurement.tobs).label("TMAX"))\
#                                 .filter(Measurement.date >= start_date)\
#                                 .filter(Measurement.date <= end_date)\
#                                 .all()
#         session.close()

#         # Convert tuple to dataframe taking on column names from the query
#         tobs_statistics_df = convert_min_avg_max_query_result_to_dataframe(tobs_statistics_tuple)

#         # Return result in JSON format
#         return format_min_avg_max_temperatures_as_json(tobs_statistics_df)

#################################################
# Utility functions
#################################################

# def convert_min_avg_max_query_result_to_dataframe(tobs_statistics_tuple):
#     # Convert tuple to dataframe taking on column names from the query
#     tobs_statistics_df = pd.DataFrame(tobs_statistics_tuple)

#     # If the query returned a non-null record (i.e. data was found for the given start date), then round the results to 2 decimal places
#     if tobs_statistics_df["TMIN"][0] != None:
#         tobs_statistics_df = tobs_statistics_df.round(2)

#     return tobs_statistics_df

#------------------------------------------------

# def format_min_avg_max_temperatures_as_json (temperatures_df):
#     # Return result in JSON format:
#     # - as labelled key:value pairs if the API endpoint's query string (if any) specified "dict"ionary mode, or
#     # - as a list of three values (in MIN-AVG-MAX order) otherwise.
#     if request.args.get("mode") == "dict":
#         return temperatures_df.to_dict(orient="records")
#     else:
#         return jsonify(temperatures_df.iloc[0].to_list())

#################################################
# Support for invocation from the command line
#################################################
if __name__ == "__main__":
    app.run(debug=False)