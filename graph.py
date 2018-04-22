from math import pi
from bokeh.plotting import figure
import datetime
from bokeh.io import export_png

# Plot candle stick
def candle_stick_plot(data, title = 'Stock', filename = 'candlestick.png', candle_width = 1):
    """
    Plot candle stick based on pandas data frame which includes columns : Date, Close, Open, High, Low
    :param data     :   pandas data
    :param title    :   Title of the plot
    :param filename :   Bokeh png file
    :return:
    """
    inc = data['Close'] > data['Open']
    dec = data['Open'] > data['Close']
    w = candle_width * 24*60*60*1000 # one day in ms
    #TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    TOOLS = "save"
    x_range = [min(data['Date'])- datetime.timedelta(days=1), max(data['Date'])+ datetime.timedelta(days=1)]
    y_range = max(data['High']) - min(data['Low'])
    y_range = [min(data['Low']) - y_range/10, max(data['High']) + y_range/10]
    p = figure(x_axis_type="datetime", tools = TOOLS, plot_width=1000, title = title, x_range = x_range, y_range = y_range)
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3
    p.segment(data['Date'], data['High'], data['Date'], data['Low'], color="black")
    # Green candle - green bar black line. Red - red bar black line. White background
    p.vbar(data['Date'][inc], w, data['Open'][inc], data['Close'][inc], fill_color="#41f479", line_color="black")
    p.vbar(data['Date'][dec], w, data['Open'][dec], data['Close'][dec], fill_color="#F2583E", line_color="F2583E")
    # Remove all toolbars and logo
    p.toolbar.logo = None
    p.toolbar_location = None
    export_png(p, filename=filename)