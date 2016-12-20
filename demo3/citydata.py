import pandas as pd

# The cities5000.txt file is downloaded from 
#    http://www.geonames.org/export/
#
# We will then just pull out the few columns we're interested in
# and save those out to a new file.
df = pd.read_csv("cities5000.txt", sep="\t", header=None, usecols=[1, 4, 5, 14],
        names=["name", "lat", "long", "pop"])

df.to_csv("citypop.csv", sep="\t", index=False)

