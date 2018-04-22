"""
    Module : stock.py
    Description :
        All stock related sub-function ( ex: get ticker price from exchange ... )
    Functions :

"""
# Import necessary packages and modules
import pandas_datareader as pdr


def get_price(symbol, start_date = '', end_date = ''):
    # If date not defined, get default 5 years of data
    if not start_date:
        data = pdr.get_data_morningstar(symbol).reset_index()
    else :
        data = pdr.get_data_morningstar(symbol, start_date, end_date).reset_index()
    return data

