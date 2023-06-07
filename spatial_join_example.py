# -*- coding: utf-8 -*-
"""
Created on Fri May 12 11:37:33 2023

@author: p432534
"""

from census import Census
from us import states
import keyring
from pygris.geocode import geolookup
from pygris import tracts
import pandas as pd 
import geopandas as gpd
from shapely.geometry import Point

# I could have a bunch of .env files or .cfg files, but I use keyring to limit code being in shared network drive spaces
# Request an API key here: https://api.census.gov/data/key_signup.html
CENSUS_API_KEY = keyring.get_password('Census','NA')
# Use my Census API key to get unfettered access to data
c = Census(CENSUS_API_KEY)

# Example pulling specific CENSUS VARIABLES
c.acs5.get(('NAME', 'B25034_010E'),
          {'for': 'state:{}'.format(states.MD.fips)})

c.acs5.get(('NAME', 'B25034_010E'),
          {'for': 'state:{}'.format(states.WA.fips)})

# State listing Example
for fips, abbr in states.mapping('fips', 'abbr').items():
    print(f'{fips} : {abbr}')



# Download all tract geographies in the US
us_tracts = tracts(year=2020, cb = True, cache = True)

# Test MPE tracts for 2020
print(us_tracts.loc[us_tracts['GEOID'].str.contains('530330073')][['GEOID']])

# look at XY coordinates from MPE
input_dict = { 
    'id'        : ['MPE',],
    'X'         : [-122.329926,],
    'Y'         : [47.616245,],
    }

'''
    INFO: YOU CAN REPLACE THIS input_df WITH ANY SET OF XY COORDINATES
    CSV requires the following (case sensitive):
        1. id
        2. X
        3. Y
        
    replace the "input_df  = pd.DataFrame(input_dict)" with the following two lines
    input_csv = r'//path/to/csv/'
    input_df = pd.read_csv(input_csv)
'''
input_df = pd.DataFrame(input_dict)

# make sure the geometry is detected
gdf = gpd.GeoDataFrame(
    input_df, geometry=gpd.points_from_xy(input_df['X'], input_df['Y']))

# name the shapes _shp and  perform a spatial merge (sjoin)
joined_df= gdf.sjoin(us_tracts, how='inner')


print(joined_df.info())
print(joined_df.drop(columns=['geometry']).head())
