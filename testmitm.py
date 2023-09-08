import asyncio
import logging
from mitmproxy import ctx
from mitmproxy import http
import MetaTrader5 as mt5
from statistics import mean
import datetime
import models


flow_trade = None


async def main():
    global flow_trade

    # establish connection to the MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    # now connect to another trading account specifying the password
    account = 27138787
    authorized = mt5.login(account, password="228228Aa", server="RoboForex-Pro")
    if not authorized:
        print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

    symbol = "EURUSD"
    point_limit = 0.00004

    spread = models.spread(None, None, None, None, None, None, None, None, None)

    while 1:
        # logging.info("test")
        await asyncio.sleep(0.001)

        if flow_trade is not None:
            infa = mt5.symbol_info_tick(symbol)

            spread.ask = infa.ask
            spread.bid = infa.bid

            dt_object = datetime.datetime.fromtimestamp(infa.time_msc / 1000)
            formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
            spread.time = formatted_date

            spread.avg = mean([spread.ask, spread.bid])
            if spread.prev_avg != None:
                spread.change = spread.avg - spread.prev_avg
                if abs(spread.change) >= point_limit:
                    spread.print_info()
                    if spread.change < 0:
                        msg = '42["openOrder",{"asset":"EURUSD","amount":10,"action":"put","isDemo":1,"requestId":15209040,"optionType":100,"time":60}]'
                    else:
                        msg = '42["openOrder",{"asset":"EURUSD","amount":10,"action":"call","isDemo":1,"requestId":15209040,"optionType":100,"time":60}]'
                    ctx.master.commands.call(
                        "inject.websocket", flow_trade, False, msg.encode()
                    )
                    await asyncio.sleep(10)
                    logging.info("SENT!")
            spread.set_prev()




class MyAddon:
    def __init__(self):
        pass

    def load(self, loader):
        logging.info("MyAddon has been loaded")

    def websocket_message(self, flow: http.HTTPFlow):
        global flow_trade

        last_message = flow.websocket.messages[-1]

        try:
            if '451-["updateAssets",{"_placeholder":true,"num":0}]' in last_message.text: #Find WS stream norm
                flow_trade = flow
                logging.info("Ok flow_trade")
        except AttributeError:
            pass

addons = [MyAddon()]


loop = asyncio.get_event_loop()
loop.create_task(main())