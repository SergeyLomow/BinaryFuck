import time
import websockets
import json
import asyncio
from statistics import mean
import pyautogui

# while 1:
#     # Get the current mouse cursor position
#     x, y = pyautogui.position()
#
#     # Print the x and y coordinates
#     print(f"Mouse position - X: {x}, Y: {y}")

async def main():
    ws_binance = await websockets.connect("wss://stream.binance.com:443/stream?streams=btcusdt@depth20@1000ms")

    prev_avg_price = -1
    while True:
        data_str = await ws_binance.recv()
        data = json.loads(data_str)

        avg_price = mean([float(data['data']['asks'][0][0]), float(data['data']['bids'][0][0])])
        if prev_avg_price == -1:
            prev_avg_price = avg_price
            continue
        change = (avg_price/prev_avg_price-1) * 100
        if prev_avg_price!=-1 and  abs(change) > 0.005:
            print(change, prev_avg_price, avg_price)
            if change<0:
                pyautogui.click(1730, 1011)

            else:
                pyautogui.click(806, 639)

            #time.sleep(60)

        prev_avg_price = avg_price

asyncio.run(main())