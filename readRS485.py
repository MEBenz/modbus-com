from os import read
import serial
import time
import struct
import xlwings as xw
from xlwings.utils import rgb_to_int
import pandas as pd


def crc16(data: bytes, poly: hex = 0xA001):
    '''
        CRC-16 MODBUS HASHING ALGORITHM
    '''
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = ((crc >> 1) ^ poly
                   if (crc & 0x0001)
                   else crc >> 1)

    # hv = hex(crc).upper()[2:]
    # blueprint = '0000'
    # return (blueprint if len(hv) == 0 else blueprint[:-len(hv)] + hv)

    hv = crc.to_bytes(2, 'little')  # CRC_16 Bigendian format

    return hv


if __name__ == "__main__":
    '''
    RS485 setting
        Baud rate : 19200
        Parity : EVENT
    '''
    rs485 = serial.Serial()
    rs485.port = '/dev/tty.usbserial-A10KMET7'
    rs485.baudrate = 19200
    rs485.parity = serial.PARITY_EVEN
    rs485.open()

    while True:
        modbus_data = []
        rx_data = []
        try:
            while rs485.in_waiting > 0:
                rx_data.append(rs485.read())
                print(rx_data)

            for x in modbus_data:
                # print(x)
                register = struct.unpack('>H', b''.join(x[2:4]))
                print(register)

            print('')
            print('')

            time.sleep(5)


        except KeyboardInterrupt:
            rs485.close()
            print('Exit')