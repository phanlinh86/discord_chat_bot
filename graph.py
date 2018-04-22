from math import pi
from bokeh.plotting import figure
from bokeh.io import export_png

# Plot candle stick
def candle_stick_plot(data, title = 'Stock', filename = 'candlestick.html'):
    inc = data['Close'] > data['Open']
    dec = data['Open'] > data['Close']
    w = 24*60*60*1000 # half day in ms
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = title)
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3
    p.segment(data['Date'], data['High'], data['Date'], data['Low'], color="black")
    p.vbar(data['Date'][inc], w, data['Open'][inc], data['Close'][inc], fill_color="#D5E1DD", line_color="black")
    p.vbar(data['Date'][dec], w, data['Open'][dec], data['Close'][dec], fill_color="#F2583E", line_color="black")
    export_png(p, filename=filename)