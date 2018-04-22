"""
    Module : chat_bot.py
    Description :
        Main function for chat_bot which monitor discord chat log from user and reply accordingly
        The bot currently support following tasks :
        1. Return crypto ticker price
        2. Return stock price with chart from morning_star database ( which doesn't require API key )
"""

import discord
import crypto
import stock
from graph import candle_stick_plot
import datetime



STOCK_GRAPH_FILE = 'stock.png'

TOKEN = input('Your discord token : ')

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        pass
    # says hello
    elif message.content == '!hello':
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    # get crypto price
    elif message.channel.name == 'crypto':
        if message.content[0] is '!':
            ticker = message.content[1:].upper()
            ticker_info = crypto.get_ticker_cmc(ticker)
            if ticker_info:
                msg = '%s: $%.2f USD / $%.2f BTC / Volume = %d USD' % (ticker, ticker_info['price_usd'], ticker_info['price_btc'], ticker_info['volume'])
            else:
                msg = 'There is no info about this ticker in coinmarketcap yet !!'
            await client.send_message(message.channel, msg)
            # await client.send_file(message.channel, 'test_img.png')

    # get stock price
    elif message.channel.name == 'stock':
        print('debug : %s' % message.content )
        if message.content[0] is '!':
            msg_array  = message.content[1:].upper().split(' ')
            symbol = msg_array[0]
            print(msg_array)
            if len(msg_array) > 1:
                time_frame = msg_array[1]
                if len(msg_array) >= 3:
                    candle_width = msg_array[2].upper()
                else:
                    candle_width = '1D'
                current_time = datetime.datetime.now()
                if time_frame[-1] is 'D':
                    end_date = current_time.strftime('%Y-%m-%d')
                    start_date = (current_time - datetime.timedelta(days= int(time_frame[:-1]))).strftime('%Y-%m-%d')
                elif time_frame[-1] is 'W':
                    end_date = current_time.strftime('%Y-%m-%d')
                    start_date = (current_time - datetime.timedelta(days= int(time_frame[:-1])*7)).strftime('%Y-%m-%d')
                elif time_frame[-1] is 'M':
                    end_date = current_time.strftime('%Y-%m-%d')
                    start_date = (current_time - datetime.timedelta(days= int(time_frame[:-1])*30)).strftime('%Y-%m-%d')
                elif time_frame[-1] is 'Y':
                    end_date = current_time.strftime('%Y-%m-%d')
                    start_date = (current_time - datetime.timedelta(days= int(time_frame[:-1])*365)).strftime('%Y-%m-%d')
                else:
                    start_date = ''
                    end_date = ''
            else:
                start_date = ''
                end_date = ''
                candle_width = '1D'
            print(start_date, end_date)
            try:
                stock_price = stock.get_price(symbol,start_date,end_date)
                # Get stock price
                msg = 'Last Price is %.2f USD' % stock_price.iloc[-1]['Close']
                print(msg)
                # Update candlestick plot
                candle_stick_plot(stock_price, '%s stock price' % symbol, STOCK_GRAPH_FILE, candle_width)
                # Send message and file to discord
                await client.send_message(message.channel, msg)
                await client.send_file(message.channel, STOCK_GRAPH_FILE)
            except:
                msg = 'There is no data about this stock yet !!'
            pass

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)