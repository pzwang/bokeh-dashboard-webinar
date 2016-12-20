
import os
import pandas as pd
from bokeh.io import curdoc
from bokeh.models.glyphs import Circle
from bokeh.models import (Range1d, ColumnDataSource,
    PanTool, WheelZoomTool, 
    GMapPlot, GMapOptions)


# The world_cities dataset in bokeh.sampledata doesn't actually have
# populations, so we grabbed our own copy of the dataset that does.
#
# from bokeh.sampledata.world_cities import data as citydata

citydata = pd.read_csv("citypop.csv", sep="\t")

# Google Maps now requires an API key. You can find out how to get one here:
# https://developers.google.com/maps/documentation/javascript/get-api-key
GMAP_API_KEY = os.environ["GMAP_API_KEY"]

plot = GMapPlot(
    x_range=Range1d(-160, 160),
    y_range=Range1d(-80, 80),
    plot_width=1000,
    plot_height=500,
    map_options=GMapOptions(lat=15, lng=0, zoom=2),
    api_key=GMAP_API_KEY,
    webgl=True,
)

circle = Circle(x="long", y="lat", size=5, line_color=None, 
            fill_color='firebrick', fill_alpha=0.4)
plot.add_glyph(ColumnDataSource(citydata), circle)
plot.add_tools(PanTool(), WheelZoomTool())

curdoc().add_root(plot)
curdoc().title = "Map of Cities >5000 Population"


