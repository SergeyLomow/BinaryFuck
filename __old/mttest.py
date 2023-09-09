import MetaTrader5 as mt5

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
ask_price = mt5.symbol_info_tick(symbol).ask
bid_price = mt5.symbol_info_tick(symbol).bid

print(ask_price, bid_price)

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()