"""
    Module : crypto.py
    Description :
        All crypto related sub-function ( ex: get ticker price from exchange ... )
    Functions :
        get_ticker_bittrex
        get_ticker_bitfinex
        get_ticker_binance
        update_cmc_list
        get_cmc_list
        get_ticker_cmc
"""
# Import necessary packages and modules
import requests
import json
import pandas as pd

# Global constants
TICKER_KEYS = ['Bid', 'Ask', 'BaseVolume', 'Last', 'Low', 'High', 'Change']
LIST_EXCHANGE = ['BITTREX', 'BITFINEX', 'BINANCE']
CMC_FILE_NAME = 'cmc_list.csv'

# Functions definitions:
def get_ticker_bittrex(ticker1, ticker2):
    """
    Get crypto ticker information from Bittrex exchange
    :param ticker1: base ticker (ex: USD , USDT , BTC or ETH )
    :param ticker2: target ticker (ex: BTC, LTC, .. )
    :return: A dict includes following price information : 'Bid', 'Ask', 'BaseVolume', 'Last', 'Low', 'High'
    """
    if ticker1.upper() == 'USD':
        ticker1 = 'USDT'
    # Grab ticker from Bittrex
    response = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummary?market=%s-%s' % (ticker1.lower(), ticker2.lower()))
    web_data = json.loads(response.text)
    # Process data
    data = {key: web_data['result'][0][key] for key in TICKER_KEYS[:-1]}
    data['Change'] = ( web_data['result'][0]['Last'] - web_data['result'][0]['PrevDay'] ) / web_data['result'][0]['PrevDay'] * 100
    return data


def get_ticker_bitfinex(ticker1, ticker2):
    """
    Get crypto ticker information from Bitfinex exchange
    :param ticker1: base ticker (ex: USD , USDT , BTC or ETH )
    :param ticker2: target ticker (ex: BTC, LTC, .. )
    :return: A dict includes following price information : 'Bid', 'Ask', 'BaseVolume', 'Last', 'Low', 'High'
    """
    BITFINEX_TICKER_LOC = [1, 3, 8, 7, 10, 9, 6]
    # Bitfinex using USD instead of USDT
    if ticker1.upper() == 'USDT':
        ticker1 = 'USD'
    # Grab ticker from Bitfinex
    response = requests.get('https://api.bitfinex.com/v2/tickers?symbols=t%s%s' % (ticker2.upper(), ticker1.upper()))
    web_data = json.loads(response.text)
    # Process data
    data = {key: web_data[0][BITFINEX_TICKER_LOC[idx]] for idx, key in enumerate(TICKER_KEYS)}
    data['Change'] = data['Change'] * 100
    return data


def get_ticker_binance(ticker1, ticker2):
    """
    Get crypto ticker information from Binance exchange
    :param ticker1: base ticker (ex: USD , USDT , BTC or ETH )
    :param ticker2: target ticker (ex: BTC, LTC, .. )
    :return: A dict includes following price information : 'Bid', 'Ask', 'BaseVolume', 'Last', 'Low', 'High'
    """
    if ticker1.upper() == 'USD':
        ticker1 = 'USDT'
    BINANCE_TICKER_LOC = [7, 9, 15, 5, 13, 12, 2]
    # Grab ticker from Binance
    response = requests.get('https://api.binance.com/api/v1/ticker/24hr?symbol=%s%s' % (ticker2.upper(), ticker1.upper()))
    web_data = json.loads(response.text)
    # Process data
    data = {key: float(list(web_data.values())[BINANCE_TICKER_LOC[idx]]) for idx, key in enumerate(TICKER_KEYS)}
    return data


def update_cmc_list():
    """
    Update coinmarketcap list of ticker excel file defined in global constant section
    :param : None
    :return: Excel file with two columns : Symbol and Name
    """
    response = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=0')
    web_data = json.loads(response.text)
    cmc_symbol = [web_data[idx]['symbol'] for idx in range(len(web_data))]
    cmc_name = [web_data[idx]['id'] for idx in range(len(web_data))]
    cmc_data_frame = pd.DataFrame(data={'Symbol': cmc_symbol, 'Name': cmc_name})
    cmc_data_frame.to_csv(CMC_FILE_NAME, index = None)


def get_cmc_list():
    """
    Get coinmarketcap list of ticker excel file defined in global constant section
    :param : None
    :return: A pandas data frame contains two columns : Symbol and Name
    """
    return pd.read_csv(CMC_FILE_NAME, index_col=False)


def get_ticker_cmc(ticker):
    """
    Get coinmarketcap ticker price , volume in USD and BTC
    :param : ticker
    :return: A dictionary includes following keys : volume, price_usd and price_btc
    """
    try:
        cmc_data_frame = get_cmc_list()
    except:
        # For 1st time run or excel file which stores coinmarketcap list doesn't exist, update the file first
        update_cmc_list()
        cmc_data_frame = get_cmc_list()

    # Check whether ticker supported by coin market cap. It will return empty if there is no support
    ticker_name = cmc_data_frame[cmc_data_frame['Symbol'] == ticker]['Name']
    if ticker_name.empty:
        return []
    else:
        ticker_name = ticker_name.iloc[0]
        # Now retrieve ticker information from coin market cap
        response = requests.get('https://api.coinmarketcap.com/v1/ticker/%s' % ticker_name)
        web_data = json.loads(response.text)
        return web_data[0]

        #return {    'volume': float(web_data[0]['24h_volume_usd']),
        #            'price_usd': float(web_data[0]['price_usd']),
        #            'price_btc': float(web_data[0]['price_btc'])}


def get_price(ticker1='USDT', ticker2='BTC', exchange='BITTREX'):
    """
    Get crypto ticker information from inputted exchange
    :param ticker1: base ticker (ex: USD , USDT , BTC or ETH )
    :param ticker2: target ticker (ex: BTC, LTC, .. )
    :param exchange: exchange. (Supported exchange is in LIST_EXCHANGE described in constant section )
    :return: A dict includes following price information : 'Bid', 'Ask', 'BaseVolume', 'Last', 'Low', 'High'
    """
    exchange = exchange.upper()
    if exchange == 'BITTREX':
        return get_ticker_bittrex(ticker1, ticker2)
    elif exchange == 'BITFINEX':
        return get_ticker_bitfinex(ticker1, ticker2)
    elif exchange == 'BINANCE':
        return get_ticker_binance(ticker1, ticker2)


def get_price_summary(ticker1='USDT', ticker2='BTC'):
    """
    Get crypto ticker information from all supported exchange defined in constant section
    :param ticker1: base ticker (ex: USD , USDT , BTC or ETH )
    :param ticker2: target ticker (ex: BTC, LTC, .. )
    :return: A dict includes following price information : 'Bid', 'Ask', 'BaseVolume', 'Last', 'Low', 'High'
    """
    data = {}
    pd.options.display.float_format = '{:,.2f}'.format
    for exchange in LIST_EXCHANGE:
        data[exchange] = list(get_price(ticker1, ticker2, exchange).values())
    data = pd.DataFrame(data, index=TICKER_KEYS)
    return data


def watch_price(list_ticker, exchange):
    """
    Get price information for a list of ticker from inputted exchange
    :param list_ticker: list of ticker
    :param exchange   : list of exchange
    :return: A pandas data frame which has following indexes :  'Total coins', 'Price (sts)', 'Volume (sts)', 'BTC', 'Price (USD)', 'USD'
             and columns defined by inputted list of ticker
    """
    pd.options.display.float_format = '{:,.2f}'.format
    # Convert to BTC
    if isinstance(exchange,str):
        usd_price = get_price('USDT', 'BTC', exchange)['Last']
        data = {key: [balance,
                      get_price('BTC', key, exchange)['Last'] * 100000000,
                      get_price('BTC', key, exchange)['BaseVolume'],
                      get_price('BTC', key, exchange)['Last'] * balance,
                      get_price('BTC', key, exchange)['Last'] * usd_price,
                      get_price('BTC', key, exchange)['Last'] * usd_price * balance]
                for key, balance in list_ticker.items()}
    elif len(exchange) == 1:
        usd_price = get_price('USDT', 'BTC', exchange[0])['Last']
        data = {key: [balance[0],
                      get_price('BTC', key, exchange[0])['Last'] * 100000000,
                      get_price('BTC', key, exchange[0])['BaseVolume'],
                      get_price('BTC', key, exchange[0])['Last'] * balance,
                      get_price('BTC', key, exchange[0])['Last'] * usd_price,
                      get_price('BTC', key, exchange[0])['Last'] * usd_price * balance]
                for key, balance in list_ticker.items()}
    else:
        data = {}
        for idx in range(len(exchange)):
            usd_price = get_price('USDT', 'BTC', exchange[idx])['Last']
            key = list(list_ticker.keys())[idx]
            balance = list(list_ticker.values())[idx]
            price_btc = get_price('BTC', key, exchange[idx])['Last']
            volume_btc = get_price('BTC', key, exchange[idx])['BaseVolume']
            data[key] = [ balance,
                          price_btc * 100000000,
                          volume_btc,
                          price_btc * balance,
                          price_btc * usd_price,
                          price_btc * usd_price * balance]

    data = pd.DataFrame(data, index=['Total coins', 'Price (sts)', 'Volume (sts)', 'BTC', 'Price (USD)', 'USD'])
    return data
