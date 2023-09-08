import time
import websockets
import json
import asyncio
from statistics import mean
import pyautogui

async def main():
    prev_avg_price = -1

    # pre_chnl = await websockets.connect("wss://api-in.po.market/socket.io/?EIO=4&transport=websocket")
    #
    ws_pocket = await websockets.connect("wss://api-us2.po.market/socket.io/?EIO=4&transport=websocket")

    while True:
        res = await ws_pocket.recv()
        print(res)

        cmd = int(res.split('{')[0])

        if cmd == 0:
            await ws_pocket.send("40")
        elif cmd == 40:
            #       42["auth",{"session":"a:4:{s:10:\\"session_id\\";s:32:\\"3697be85251954980997097ec9f027ee\\";s:10:\\"ip_address\\";s:15:\\"137.184.211.230\\";s:10:\\"user_agent\\";s:111:\\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36\\";s:13:\\"last_activity\\";i:1694163265;}2d38e39243fe5b4396350e88aa089dfc","isDemo":1,"uid":67215701}]
            stri = '42["auth",{"session":"a:4:{s:10:\\"session_id\\";s:32:\\"3697be85251954980997097ec9f027ee\\";s:10:\\"ip_address\\";s:15:\\"77.234.216.36\\";s:10:\\"user_agent\\";s:111:\\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36\\";s:13:\\"last_activity\\";i:1694163265;}2d38e39243fe5b4396350e88aa089dfc","isDemo":1,"uid":67215701}]'
            await ws_pocket.send(stri)

asyncio.run(main())
