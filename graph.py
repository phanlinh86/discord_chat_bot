from math import pi
from bokeh.plotting import figure
import datetime
from bokeh.io import export_png
import numpy as np
import matplotlib.pyplot as plt
import six

# Plot candle stick
def candle_stick_plot(data, title = 'Stock', filename = 'candlestick.png', candle_width = '1D'):
    """
    Plot candle stick based on pandas data frame which includes columns : Date, Close, Open, High, Low
    :param data     :   pandas data
    :param title    :   Title of the plot
    :param filename :   png file name
    :return:
    """
    dict_convert_candle_width = {'D':1, 'W':7 , 'M' : 30, 'Y' : 365}
    candle_width_per_day = int(candle_width[:-1]) * dict_convert_candle_width[candle_width[-1]]
    w = candle_width_per_day * 24*60*60*1000 * 0.9 # one day in ms
    # Re sample data based on candle width
    temp = data.set_index(data['Date']).resample(candle_width)
    data_resample = temp[['Close']].last()
    data_resample['Open'] = temp['Open'].first()
    data_resample['High'] = temp['High'].max()
    data_resample['Low'] = temp['Low'].min()
    data_resample['Volume'] = temp['Volume'].sum()
    data = data_resample.dropna().reset_index()
    #TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    inc = data['Close'] > data['Open']
    dec = data['Open'] > data['Close']
    TOOLS = "save"

    x_range = [min(data['Date'])- datetime.timedelta(days=candle_width_per_day), max(data['Date'])+ datetime.timedelta(days=candle_width_per_day)]
    y_range = max(data['High']) - min(data['Low'])
    y_range = [min(data['Low']) - y_range/10, max(data['High']) + y_range/10]
    p = figure(x_axis_type="datetime", tools = TOOLS, plot_width=1000, title = title, x_range = x_range, y_range = y_range)
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3
    p.segment(data['Date'], data['High'], data['Date'], data['Low'], color="black")
    # Green candle - green bar black line. Red - red bar black line. White background
    p.vbar(data['Date'][inc], w, data['Open'][inc], data['Close'][inc], fill_color="#41f479", line_color="black")
    p.vbar(data['Date'][dec], w, data['Open'][dec], data['Close'][dec], fill_color="#F2583E", line_color="black")
    # Remove all toolbars and logo
    p.toolbar.logo = None
    p.toolbar_location = None
    export_png(p, filename=filename)


def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0, file_name = 'test.png',
                     ax=None, **kwargs):
    """
    Render pandas table into matplotlib figure
    :param data:            Pandas data frame
    :param col_width:       Column width
    :param row_height:      Height of row
    :param font_size:       Font size
    :param header_color:    Header color
    :param row_colors:      Row color
    :param edge_color:      Edge color
    :param bbox:
    :param header_columns:
    :param file_name:
    :param ax:
    :param kwargs:
    :return:
    """
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    plt.savefig(file_name)
    return ax

