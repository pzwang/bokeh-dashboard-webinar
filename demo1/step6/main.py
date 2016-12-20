"Step 5: Add a data table"

import pandas as pd

from os.path import dirname, join
DATA_DIR = './daily'

def load_ticker(name):
    fname = join(DATA_DIR, "table_%s.csv" % name.lower())
    data = pd.read_csv(fname, header=None, parse_dates=['date'],
                       names=['date', 'foo', 'o', 'h', 'l', 'c', 'v'])
    data = data.set_index('date')
    # For each tick symbol, compute the returns 
    return pd.DataFrame(
            { name            : data.c, 
              name+'_returns' : data.c.diff()/data.c })

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource 
from bokeh.models.widgets import Select
from bokeh.plotting import figure

def get_data(symbol1, symbol2):
    df1 = load_ticker(symbol1)
    df2 = load_ticker(symbol2)
    data = pd.concat([df1, df2], axis=1)
    data = data.dropna()
    data['ticker1'] = data[symbol1]
    data['ticker2'] = data[symbol2]
    data['t1_returns'] = data[symbol1+'_returns']
    data['t2_returns'] = data[symbol2+'_returns']
    return data

datasource = ColumnDataSource(data=get_data("AAPL", "GOOG"))

# Create the correlation plot
plot = figure(title="Correlation Plot", plot_width=500, plot_height=500,
              tools="pan, wheel_zoom, box_select, lasso_select, tap, reset")
plot.circle("t1_returns", "t2_returns", source=datasource)
plot.title.text_font_size = "25px"
plot.title.align = "center"

STOCKLIST = ['AAPL', 'GOOG', 'INTC', 'BRCM', 'YHOO']
ticker1 = Select(value="AAPL", options=STOCKLIST, title="Stock1")
ticker2 = Select(value="GOOG", options=STOCKLIST, title="Stock2")

def ticker_update(attribute, old, new):
    t1, t2 = ticker1.value, ticker2.value
    data = get_data(t1, t2)
    datasource.data = ColumnDataSource.from_df(data[['ticker1', 'ticker2', 't1_returns', 't2_returns']])

ticker1.on_change("value", ticker_update)
ticker2.on_change("value", ticker_update)

def selection_change(attrname, old, new):
    t1, t2 = ticker1.value, ticker2.value
    data = get_data(t1, t2)
    selected = datasource.selected['1d']['indices']
    if selected:
        data = data.iloc[selected, :]

    table_data.data = ColumnDataSource.from_df(data)
    table_data.data["date"] = data.index

datasource.on_change('selected', selection_change)

from bokeh.models import BoxSelectTool, LassoSelectTool
plot.select(BoxSelectTool).select_every_mousemove = False
plot.select(LassoSelectTool).select_every_mousemove = False

from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
table_data = ColumnDataSource({"date":[], "ticker1":[], "ticker2":[], 
                "t1_returns":[], "t2_returns":[]})
columns = [
        TableColumn(field="date", title="Date", formatter=DateFormatter()),
        TableColumn(field="ticker1", title="Stock1", width=100),
        TableColumn(field="ticker2", title="Stock2", width=100),
        TableColumn(field="t1_returns", title="Stock1 Returns"),
        TableColumn(field="t2_returns", title="Stock2 Returns")]

table = DataTable(source=table_data, columns=columns, width=800)

layout = column(
            row(column(ticker1, ticker2), plot),
            table)

curdoc().add_root(layout)
curdoc().title = "Stock Correlations"


