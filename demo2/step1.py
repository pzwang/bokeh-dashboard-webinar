"Step 1. Basic streaming chart"

from numpy import asarray, cumprod, convolve, exp, ones
from numpy.random import lognormal, gamma, uniform

def _create_prices(t):
    last_average = 100 if t==0 else source.data['average'][-1]
    returns = asarray(lognormal(mean.value, stddev.value, 1))
    average =  last_average * cumprod(returns)
    high = average * exp(abs(gamma(1, 0.03, size=1)))
    low = average / exp(abs(gamma(1, 0.03, size=1)))
    delta = high - low
    open = low + delta * uniform(0.05, 0.95, size=1)
    close = low + delta * uniform(0.05, 0.95, size=1)
    return open[0], high[0], low[0], close[0], average[0]

from bokeh.layouts import row, column, gridplot
from bokeh.models import ColumnDataSource, Slider, Select
from bokeh.plotting import curdoc, figure
from bokeh.driving import count

source = ColumnDataSource(dict(
    time=[], average=[], low=[], high=[], open=[], close=[],
    color=[]
))

p = figure(plot_height=500, tools="xpan,xwheel_zoom,xbox_zoom,reset", 
           x_axis_type=None, 
           y_axis_location="right", toolbar_location="left")

p.x_range.follow = "end"
p.x_range.follow_interval = 50
p.x_range.range_padding = 0.05

p.line(x='time', y='average', alpha=0.4, line_width=3, color='deepskyblue', source=source)
p.segment(x0='time', y0='low', x1='time', y1='high', line_width=2, color='gray', source=source)
p.segment(x0='time', y0='open', x1='time', y1='close', line_width=8, color='color', source=source)

mean = Slider(title="mean", value=0, start=-0.01, end=0.01, step=0.001)
stddev = Slider(title="stddev", value=0.04, start=0.01, end=0.1, step=0.01)

curdoc().add_root(column(row(mean, stddev), p, width=1000))

@count()
def update(t):
    open, high, low, close, average = _create_prices(t)
    color = "green" if open < close else "firebrick"
    new_data = dict(
        time=[t],
        open=[open],
        high=[high],
        low=[low],
        close=[close],
        average=[average],
        color=[color],
    )
    close = source.data['close'] + [close]
    source.stream(new_data, 300)

curdoc().add_periodic_callback(update, 100)
curdoc().title = "Streaming Stock Chart"
