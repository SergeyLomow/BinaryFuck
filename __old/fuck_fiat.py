import MetaTrader5 as mt5
from statistics import mean
import pyautogui
import datetime
import models

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
point_limit = 0.00005

spread = models.spread(None, None, None, None, None, None, None, None, None)

while True:
    infa = mt5.symbol_info_tick(symbol)

    spread.ask = infa.ask
    spread.bid = infa.bid

    dt_object = datetime.datetime.fromtimestamp(infa.time_msc/1000)
    formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
    spread.time = formatted_date

    spread.avg = mean([spread.ask, spread.bid])
    if spread.prev_avg != None:
        spread.change = spread.avg - spread.prev_avg
        if abs(spread.change) >= point_limit:
            spread.print_info()
            if spread.change<0:
                pyautogui.click(1426, 552)
            else:
                pyautogui.click(1426, 477)

    spread.set_prev()

# # shut down connection to the MetaTrader 5 terminal
# mt5.shutdown()