# Project Title: Global data analysis API
Data Analytics Boot Camp - Project 3

Slides: https://docs.google.com/presentation/d/1QuK3O8G-P0fPEqNZbSi0aKoBhZVnk_J-3CgCmaurGuE/edit?usp=sharing

## Team members (Group 6)
Kenneth Le, Kurai Monica Matiki, Eric Tran, Greg Presneill

## Project Overview and Rationale
This project aims to provide a reliable, scalable API solution that supports analysts investigating global data statistics and trends over time.

The initial dataset focuses on world population growth. Understanding global population growth is crucial for policy making, economic planning, and resource management. By analysing population data, we help governments, organisations, and researchers to draw insights and make data-driven decisions.

Analysts could use the data to explore questions such as:
1. How has the global population growth rate changed over the past decade?
2. What are the trends in population growth across different continents and countries?
3. Which regions are experiencing the highest and lowest growth rates?
4. How do demographic factors such as age distribution and urbanization rates correlate with population growth patterns?
5. What are the projected population trends for the next few decades?

## Ethical considerations

- Source datasets (World Bank Group) Terms of Use
    - https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets
    - https://creativecommons.org/licenses/by/4.0/

## How to use the API

The API will return JSON data for queries such as:
- World population growth % by year (for all countries in the dataset)
- Country population growth % by year
- Country population growth % by decade
- Population growth % by continent by year

---

# Proposed Solution design

![System Design initial sketch](SystemDesignSketch_v3.png)

# Implementation notes

For this project, we chose the 'Data Engineering' track.

## Datasets to Be Used
- World Bank population growth dataset
    - https://data.worldbank.org/indicator/SP.POP.GROW?end=2023&name_desc=false&start=1961&view=chart&year=2023
    - Sample of source data:
        - ![A sample of the source data](SampleSourceData.png)
    - Metadata:
        - ![Metadata about the population growth source data](Metadata_PopulationGrowth.png)

## Rough Breakdown of Tasks
1. Extract data (World Bank dataset)
1. Data cleansing
1. Data/schema validation
1. Transform data as required to match database schema
1. Load data into database
1. Design API endpoints
1. Develop queries to allow end users to extract data through the API
1. Summary for presentation.

## Other details
Database choice: relational database (SQL) as we are dealing with tabular data.

Collections: at least two tables are needed
1. Countries: Contains information on countries/continents
2. Population data: Contains historical and current population statistics.

Number of records: The database will have at least 100 records.

ETL Workflow
1. Data extraction – extract raw data from publicly available databases
such as the World Bank datasets available as CSV files or via APIs.
2. Data transformation – Clean and normalise the data to ensure
consistency, convert data measurements to standard units if
needed, add derived fields like growth percentages.
3. Data Load – insert the transformed data into a SQL database.
Data Display
Flask API – develop a Flask API to serve the data in JSON format.

## Ethical Consideration 
The project utilizes publicly available, open-source datasets from trusted organizations such as the World Bank. We carefully verify the accuracy and reliability of these datasets before incorporating them into our system.

1. Copyright and Fair Use: The dataset has been reviewed for copyright protections, and its use complies with the applicable fair use or licensing agreements.

2. Intended Use Documentation: The intended usage of the dataset, both present and future, has been documented to ensure compliance with the terms of use.

3. Data Collection Verification: The dataset's collection process has been investigated to confirm that it was sourced from authorized and legitimate providers.


