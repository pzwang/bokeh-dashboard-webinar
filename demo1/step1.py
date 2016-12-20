"Step 1: get a basic interactive plot"

execfile("step0.py")

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

apple = load_ticker("AAPL")
google = load_ticker("GOOG")
data = pd.concat([apple, google], axis=1)

datasource = ColumnDataSource(data)

# Create the correlation plot
plot = figure(title="Correlation Plot", plot_width=500, plot_height=500)
plot.circle("AAPL_returns", "GOOG_returns", source=datasource)

plot.title.text_font_size = "25px"
plot.title.align = "center"

curdoc().add_root(plot)
curdoc().title = "Stock Correlations"


