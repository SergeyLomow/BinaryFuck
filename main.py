import time
import websockets
import json
import asyncio
from statistics import mean
import pyautogui

#1426 477 UP
#1426 552 DOWN

# while 1:
#     # Get the current mouse cursor position
#     x, y = pyautogui.position()
#
#     # Print the x and y coordinates
#     print(f"Mouse position - X: {x}, Y: {y}")

async def main():
    prev_avg_price = -1

    # ws_binance = websockets.connect("wss://stream.binance.com:443/stream?streams=btcusdt@depth20@1000ms")

    pre_chnl = await websockets.connect("wss://api-in.po.market/socket.io/?EIO=4&transport=websocket")
    # time.sleep(1)

    ws_pocket = await websockets.connect("wss://api-us2.po.market/socket.io/?EIO=4&transport=websocket")

    # ws_pocket.send({
    #   "sid": "8N1mV-4W64brsVOlKDcC",
    #   "upgrades": [],
    #   "pingInterval": 25000,
    #   "pingTimeout": 20000,
    #   "maxPayload": 1000000
    # })

    # await ws_pocket.send(""""42["auth",{"session":"a:5:{s:10:\"session_id\";s:32:\"f77d65a215f5725e61146d4b1cd127d5\";s:10:\"ip_address\";s:14:\"159.223.151.31\";s:10:\"user_agent\";s:111:\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36\";s:13:\"last_activity\";i:1694037849;s:9:\"user_data\";s:0:\"\";}72b9021a0cf2732fd143fafd2967e69b","isDemo":1,"uid":67237741}]""")

    while True:
        res = await ws_pocket.recv()
        print(res)
        if res[0]=="0":
            await ws_pocket.send("40")
        elif res[0]=="4":
            stri = '42["auth",{"session":"a:5:{s:10:\\"session_id\\";s:32:\\"f77d65a215f5725e61146d4b1cd127d5\\";s:10:\\"ip_address\\";s:14:\\"159.223.151.31\\";s:10:\\"user_agent\\";s:111:\\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36\\";s:13:\\"last_activity\\";i:1694037849;s:9:\\"user_data\\";s:0:\\"\\";}72b9021a0cf2732fd143fafd2967e69b","isDemo":1,"uid":67237741}]'
            await asyncio.gather(pre_chnl.close(), ws_pocket.send(stri))

        pass


    pass

    # while True:
    #     data_str = await ws_binance.recv()
    #     data = json.loads(data_str)
    #
    #     avg_price = mean([float(data['data']['asks'][0][0]), float(data['data']['bids'][0][0])])
    #     change = (avg_price/prev_avg_price-1) * 100
    #     if prev_avg_price!=-1 and  change > 0.02:
    #         print(change, prev_avg_price, avg_price)
    #         if change<0:
    #             pyautogui.click(1426, 552)
    #         else:
    #             pyautogui.click(1426, 477)
    #
    #         #time.sleep(60)
    #
    #     prev_avg_price = avg_price


asyncio.run(main())
