"Step 2: Add drop-downs"

execfile("step0.py")

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Select
from bokeh.plotting import figure

apple = load_ticker("AAPL")
google = load_ticker("GOOG")
data = pd.concat([apple, google], axis=1)

datasource = ColumnDataSource(data)

# Create the correlation plot
plot = figure(title="Correlation Plot", plot_width=500, plot_height=500)
plot.circle("AAPL_returns", "GOOG_returns", size=2, source=datasource)
plot.title.text_font_size = "25px"
plot.title.align = "center"

STOCKLIST = ['AAPL', 'GOOG', 'INTC', 'BRCM', 'YHOO']
ticker1 = Select(value="AAPL", options=STOCKLIST)
ticker2 = Select(value="GOOG", options=STOCKLIST)

# Define the layout
layout = row(column(ticker1, ticker2), plot)

curdoc().add_root(layout)
curdoc().title = "Stock Correlations"


