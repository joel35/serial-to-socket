import asyncio
import serial
import websockets
from typing import Any


SERIAL_PORT = '/dev/tty.usbmodem4101'
SERIAL_URL = 'loop://'

async def send_data_to_serial(websocket: websockets.WebSocketClientProtocol, ser: serial.Serial) -> None:
    while True:
        data = await websocket.recv()
        print(f'Sending {data} to {ser.name}')

        data_bytes = bytes.fromhex(data)

        result = ser.write(data_bytes)
        print(f'Wrote {result} bytes to {ser.name}')


def receive_data_from_serial(websocket: websockets.WebSocketClientProtocol, ser: serial.Serial) -> None:
    response = ser.read(128)
    print(f'Received {response} from {ser.name}')
    response_hex = response.hex()
    asyncio.ensure_future(websocket.send(response_hex))
    print(f'Sent {response_hex} to {websocket.remote_address}')


async def bridge(websocket: websockets.WebSocketClientProtocol, path: str) -> None:
    with serial.Serial(SERIAL_PORT, timeout=1) as ser:
        loop = asyncio.get_event_loop()
        loop.add_reader(ser.fileno(), receive_data_from_serial, websocket, ser)
        await send_data_to_serial(websocket, ser)


async def main() -> None:
    async with websockets.serve(bridge, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())
