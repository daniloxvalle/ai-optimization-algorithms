# BELOW ARE SOME LINKS TO REAL-WORLD PROBLEMS.
# JUST CHOOSE A **`DATA DOWNLOAD`** LINK, SET THE URL VARIABLE BELOW, AND RUN THE ALGORITHM.

# WESTERN SAHARA
# 29 CITIES
# The optimal tour has length: 27.603
# POINTS PHOTO: HTTP://WWW.MATH.UWATERLOO.CA/TSP/WORLD/WIPOINTS.HTML
# SOLUTION PHOTO: HTTP://WWW.MATH.UWATERLOO.CA/TSP/WORLD/WITOUR.HTML
# Data Download: http://www.math.uwaterloo.ca/tsp/world/wi29.tsp

# Djibouti dataset
# 38 cities
# The optimal tour has length: 6.656
# Points Photo: http://www.math.uwaterloo.ca/tsp/world/djpoints.html
# Solution Photo: http://www.math.uwaterloo.ca/tsp/world/djtour.html
# Data Download: http://www.math.uwaterloo.ca/tsp/world/dj38.tsp

# Qatar
# 194 cities
# The optimal tour has length: 9.352
# Points Photo: http://www.math.uwaterloo.ca/tsp/world/qapoints.html
# Solution Photo: http://www.math.uwaterloo.ca/tsp/world/qatour.html
# Data Download: http://www.math.uwaterloo.ca/tsp/world/qa194.tsp

# Uruguay
# 734 cities
# The optimal tour has length: 79.114
# Points Photo: http://www.math.uwaterloo.ca/tsp/world/uypoints.html
# Solution Photo: http://www.math.uwaterloo.ca/tsp/world/uytour.html
# Data Download: http://www.math.uwaterloo.ca/tsp/world/uy734.tsp

import pandas as pd

URL_CITY_COORDINATES = "https://www.math.uwaterloo.ca/tsp/world/wi29.tsp"

df_coordinates = pd.read_table(
    URL_CITY_COORDINATES,
    skiprows=7,  # ignore the first 7 lines with information
    names=["X", "Y"],  # column names
    sep=" ",  # column separator
    index_col=0,  # use col=0 as index (city names)
    skipfooter=1,  # ignore the last line (EOF)
    engine="python",  # to use the parser with skipfooter without warning
)

# uncomment the line below to check if the data was read correctly
# print(df_coordinates)
