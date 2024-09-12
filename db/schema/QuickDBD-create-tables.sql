-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE post-export changes:
-- (1) re-ordered columns in PopulationGrowth table so years come after the CountryName and other columns (as per ETL data structure).
-- (2) added semi-colon statement terminators.

-- Reference data - list of countries by continent
CREATE TABLE "CountryContinent" (
    "CountryCode" char(3)  NOT NULL ,
    "Continent" varchar(30)  NOT NULL ,
    CONSTRAINT "pk_CountryContinent" PRIMARY KEY (
        "CountryCode"
    )
);

GO

-- World Bank - Population Growth dataset
CREATE TABLE "PopulationGrowth" (
    "CountryCode" char(3)  NOT NULL ,
    "Region" varchar(30)  NOT NULL ,
    "IncomeGroup" varchar(30)  NOT NULL ,
    "CountryName" varchar(50)  NOT NULL ,
    "1960" float  NULL ,
    "1961" float  NULL ,
    "1962" float  NULL ,
    "1963" float  NULL ,
    "1964" float  NULL ,
    "1965" float  NULL ,
    "1966" float  NULL ,
    "1967" float  NULL ,
    "1968" float  NULL ,
    "1969" float  NULL ,
    "1970" float  NULL ,
    "1971" float  NULL ,
    "1972" float  NULL ,
    "1973" float  NULL ,
    "1974" float  NULL ,
    "1975" float  NULL ,
    "1976" float  NULL ,
    "1977" float  NULL ,
    "1978" float  NULL ,
    "1979" float  NULL ,
    "1980" float  NULL ,
    "1981" float  NULL ,
    "1982" float  NULL ,
    "1983" float  NULL ,
    "1984" float  NULL ,
    "1985" float  NULL ,
    "1986" float  NULL ,
    "1987" float  NULL ,
    "1988" float  NULL ,
    "1989" float  NULL ,
    "1990" float  NULL ,
    "1991" float  NULL ,
    "1992" float  NULL ,
    "1993" float  NULL ,
    "1994" float  NULL ,
    "1995" float  NULL ,
    "1996" float  NULL ,
    "1997" float  NULL ,
    "1998" float  NULL ,
    "1999" float  NULL ,
    "2000" float  NULL ,
    "2001" float  NULL ,
    "2002" float  NULL ,
    "2003" float  NULL ,
    "2004" float  NULL ,
    "2005" float  NULL ,
    "2006" float  NULL ,
    "2007" float  NULL ,
    "2008" float  NULL ,
    "2009" float  NULL ,
    "2010" float  NULL ,
    "2011" float  NULL ,
    "2012" float  NULL ,
    "2013" float  NULL ,
    "2014" float  NULL ,
    "2015" float  NULL ,
    "2016" float  NULL ,
    "2017" float  NULL ,
    "2018" float  NULL ,
    "2019" float  NULL ,
    "2020" float  NULL ,
    "2021" float  NULL ,
    "2022" float  NULL ,
    "2023" float  NULL ,
    CONSTRAINT "pk_PopulationGrowth" PRIMARY KEY (
        "CountryName"
    )
);

GO

ALTER TABLE "PopulationGrowth" ADD CONSTRAINT "fk_PopulationGrowth_CountryCode" FOREIGN KEY("CountryCode")
REFERENCES "CountryContinent" ("CountryCode");
GO

