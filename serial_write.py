import sys
from time import sleep

import serial

MESSAGE = 'Hello, world!'

ser = serial.serial_for_url('loop://', timeout=1)
print(f'{ser.name} is open: {ser.is_open}')
ser.write(MESSAGE.encode())
print(f'Wrote {MESSAGE} to {ser.name}')

sleep(1)

result = ser.readall().decode()
print(f'Read {result} from {ser.name}')

ser.close()
