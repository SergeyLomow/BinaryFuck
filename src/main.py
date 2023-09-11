import asyncio
import logging
from mitmproxy import ctx
from mitmproxy import http
import MetaTrader5 as mt5
from statistics import mean
import datetime
import models
from mitmproxy import command


class PocketOption:
    def __init__(self):
        self.started_loop = False
        self.trade_ws = None
        self.pair_mt5 = "EURUSD"
        self.pair_pocket = "EURUSD"
        self.expiration_time = 60
        self.sleep_after_trade = 20
        self.point_min = 6

        #INIT mt5
        if not mt5.initialize():
            logging.info("initialize() failed, error code =", mt5.last_error())
            quit()

        account = 27138787
        authorized = mt5.login(account, password="228228Aa", server="RoboForex-Pro")
        if not authorized:
            logging.info(("failed to connect at account #{}, error code: {}".format(account, mt5.last_error())))


    def load(self, loader):
        logging.info("PocketOption has been loaded")

    def websocket_message(self, flow: http.HTTPFlow):
        if not self.started_loop:
            self.started_loop = True
            loop = asyncio.get_event_loop()
            loop.create_task(self.main())

        try:
            last_message = flow.websocket.messages[-1]
            if '451-["updateAssets",{"_placeholder":true,"num":0}]' in last_message.text: #Find WS stream
                self.trade_ws = flow
                logging.info("trade_ws updated")
        except AttributeError:
            pass

    async def main(self):
        logging.info("Started loop!")

        point_limit = await self.get_precision() * self.point_min

        spread = models.spread(None, None, None, None, None, None, None, None, None)

        while 1:
            await asyncio.sleep(0.001)

            if self.trade_ws is not None:
                infa = mt5.symbol_info_tick(self.pair_mt5)

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
                            mode = "put"
                        else:
                            mode = "call"
                        msg = '42["openOrder",{"asset":"' + self.pair_pocket + '","amount":10,"action":"'+mode+'","isDemo":1,"requestId":15209040,"optionType":100,"time":' + str(
                            self.expiration_time) + '}]'
                        ctx.master.commands.call(
                            "inject.websocket", self.trade_ws, False, msg.encode()
                        )
                        logging.info("Send "+mode)
                        await asyncio.sleep(self.sleep_after_trade)
                spread.set_prev()

    async def get_precision(self):
        digits = mt5.symbol_info(self.pair_mt5).digits
        res = 10**(-digits)
        return res

    # @command.command("pocketoption.test")
    # def test(self) -> None:
    #     logging.info("AAAA")

addons = [PocketOption()]

if __name__ == "__main__":
    pocket_option = PocketOption()
    asyncio.run(pocket_option.get_precision())

