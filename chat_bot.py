"""
    Module : chat_bot.py
    Description :
        Main function for chat_bot which monitor discord chat log from user and reply accordingly
        The bot currently support following tasks :
        1. Return crypto ticker price


"""

import discord
from crypto import get_ticker_cmc

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
            ticker_info = get_ticker_cmc(ticker)
            if ticker_info:
                msg = '%s: $%.2f USD / $%.2f BTC / Volume = %d USD' % (ticker, ticker_info['price_usd'], ticker_info['price_btc'], ticker_info['volume'])
            else:
                msg = 'There is no info about this ticker in coinmarketcap yet !!'
            await client.send_message(message.channel, msg)
            # await client.send_file(message.channel, 'test_img.png')

    # get stock price
    elif message.channel.name == 'stock':
        if message.content[0] is '!':
            # No support for channel stock yet
            pass

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)