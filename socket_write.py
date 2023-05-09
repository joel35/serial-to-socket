import asyncio
from time import sleep

from websockets.sync.client import connect


MESSAGE = '7d905807b27e'

def hello():
    with connect("ws://localhost:8765") as websocket:
        while True:
            print(f'{websocket=}')
            websocket.send('7d905807b27e')
            print(f'Sent {MESSAGE} to {websocket.remote_address}')
            message = websocket.recv()
            print(f"Received: {message}")

            sleep(1)

hello()
