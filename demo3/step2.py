
execfile("step1.py")

from bokeh.models import HoverTool

hover = HoverTool(tooltips=[
            ("Name", "@name"),
            ("Pop", "@pop")])

plot.add_tools(hover)

