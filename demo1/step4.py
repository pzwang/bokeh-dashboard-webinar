"Step 4: Handle selections - widgets aren't the only thing with event handlers"

execfile("step0.py")

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
ticker1 = Select(value="AAPL", options=STOCKLIST)
ticker2 = Select(value="GOOG", options=STOCKLIST)

# Define the layout
layout = row(column(ticker1, ticker2), plot)

curdoc().add_root(layout)
curdoc().title = "Stock Correlations"

def ticker_update(attribute, old, new):
    t1, t2 = ticker1.value, ticker2.value
    data = get_data(t1, t2)
    datasource.data = ColumnDataSource.from_df(data[['ticker1', 'ticker2', 't1_returns', 't2_returns']])

ticker1.on_change("value", ticker_update)
ticker2.on_change("value", ticker_update)


#-------------------------------------------------------------------------

def selection_change(attrname, old, new):
    t1, t2 = ticker1.value, ticker2.value
    data = get_data(t1, t2)
    selected = datasource.selected['1d']['indices']
    if selected:
        data = data.iloc[selected, :]

    if len(data) > 15:
        text = str(data[[t1, t2, t1+'_returns', t2+'_returns']].describe())
    else:
        text = str(data[[t1, t2, t1+'_returns', t2+'_returns']])
    print text

datasource.on_change('selected', selection_change)

from bokeh.models import BoxSelectTool, LassoSelectTool
plot.select(BoxSelectTool).select_every_mousemove = False
plot.select(LassoSelectTool).select_every_mousemove = False


