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
    """List all available API routes"""
    return (
        f"<h1>Welcome to the Global Data Analysis API</h1>"
        f"<h2>Available Routes:</h2>"

        f"<h3><u>Reference Data</u></h3>"

        f"<p><b>/api/v1.0/country-codes</b></br>\
        All country codes sorted alphabetically</p>"

        f"<p><b>/api/v1.0/continents-with-countries</b></br>\
        All continents and countries in them, sorted alphabetically by the respective names</p>"

        f"<h3><u>Population Growth Data</u></h3>"

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

#################################################
# Support for invocation from the command line
#################################################
if __name__ == "__main__":
    app.run(debug=False)