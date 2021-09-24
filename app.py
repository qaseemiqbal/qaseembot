import json, config
import re
from flask import Flask,request,jsonify
app = Flask(__name__)
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *

request_client = RequestClient(api_key=config.API_KEY, secret_key=config.API_SECRET)
coins = {
    "ETHUSDT":"None",
    "BTCUSDT":"None",
    "ADAUSDT":"None",
    "DOGEUSDT":"None",
}
lavs = {
    "ETHUSDT":"20",
    "BTCUSDT":"20",
    "ADAUSDT":"20",
    "DOGEUSDT":"20",
}
lastOrder = {
    "ETHUSDT":"0",
    "BTCUSDT":"0",
    "ADAUSDT":"0",
    "DOGEUSDT":"0",
}
def close_order(coin):
    try:
        if lastOrder[coin] != "0":
            print(lastOrder[coin])
            result = request_client.cancel_order(coin, lastOrder[coin])
            lastOrder[coin] = "0"
            print(result)
        return True
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False
    return True
def order(coin,amount,leve,position):
    if coins[coin] != position :
        result = request_client.get_balance()
        print(result)
        try:
            close_order(coin)
        except Exception as e:
            print("an exception occured - {}".format(e))
        try:
            lavs[coin] = leve
            result = request_client.change_initial_leverage(coin, lavs[coin])

        except Exception as e:
            print("an exception occured - {}".format(e))
        try:
            result = request_client.change_margin_type(coin, marginType=FuturesMarginType.ISOLATED)

        except Exception as e:
            print("an exception occured - {}".format(e))
        try:
            if  position.lower() == "long":
                result = request_client.post_order(symbol=coin, side=OrderSide.BUY, ordertype=OrderType.MARKET, quantity=amount)
                print(result)
                coins[coin] = position
                lastOrder[coin] = getattr(result,'orderId')
                
            if  position.lower() == "short":
                result = request_client.post_order(symbol=coin, side=OrderSide.SELL, ordertype=OrderType.MARKET, quantity=amount)
                print(result)
                coins[coin] = position
                lastOrder[coin] = getattr(result,'orderId')
        except Exception as e:
            print("an exception occured - {}".format(e))
    return True
@app.route('/')
def main_view():
    return 'Hello from loseb k.!'
@app.route('/tradehook',methods=['POST'])
def webhook():
    resData = json.loads(request.data)
    print(resData)
    order_response = order(resData['coin'],resData['quantity'],resData['leverage'],resData['positionSide'])
    print(order_response)
    if resData['passkey'] != config.WEBHOOK_PASS:
        return {
            "code":"error",
            "message":"Invalid"
        }
    return {
        "code":"success",
        "message" : "We are good here"
    } 
    
"""
 
import config
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *

request_client = RequestClient(api_key=config.API_KEY, secret_key=config.API_SECRET)
result = request_client.get_account_information()
print(result)
print("canDeposit: ", result.canDeposit)
print("canWithdraw: ", result.canWithdraw)
print("feeTier: ", result.feeTier)
print("maxWithdrawAmount: ", result.maxWithdrawAmount)
print("totalInitialMargin: ", result.totalInitialMargin)
print("totalMaintMargin: ", result.totalMaintMargin)
print("totalMarginBalance: ", result.totalMarginBalance)
print("totalOpenOrderInitialMargin: ", result.totalOpenOrderInitialMargin)
print("totalPositionInitialMargin: ", result.totalPositionInitialMargin)
print("totalUnrealizedProfit: ", result.totalUnrealizedProfit)
print("totalWalletBalance: ", result.totalWalletBalance)
print("updateTime: ", result.updateTime)
print("=== Assets ===")
PrintMix.print_data(result.assets)
print("==============")
print("=== Positions ===")
PrintMix.print_data(result.positions)
print("==============") """

""" import json, config
from binance.client import Client
from binance.enums import *
client = Client(config.API_KEY,config.API_SECRET,testnet=True)

account_balance = client.get_asset_balance(asset='USDT')
print(account_balance)
account_trades = client.get_my_trades(symbol='ETHUSDT')
print(account_trades)
account_orders = client.get_all_orders(symbol='ETHUSDT')
print(account_orders)

order = client.futures_create_order(symbol='ETHUSDT', side='BUY', type='MARKET', quantity=10)
print(order)  """