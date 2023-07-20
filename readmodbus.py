""""
grid_voltage
dec : 303 -> 012F
off : 40001 + 303 = 40304 -> 9d70

length = 0008


0103012f0001
01039d700001

0103012f0008
01039d700008

0103012f0001B43F
01039d700001AA7D

0103012f00087439
01039d7000086A7B
"""

from os import read
import serial
import time
import struct


def readI2C(self, command):
    if self.STM32 != 0:
        rx_data = []
        self.STM32.write(bytes([command]))
        time.sleep(0.3)
        while ~self.STM32.in_waiting:
            if self.STM32.in_waiting:
                break

        while self.STM32.in_waiting > 0:
            rx_data.append(self.STM32.read())

        return rx_data
    else:
        rx_data = [b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00',
                   b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00']
        return rx_data


def readModbus(register: int):
    '''
    slave_id = 0x01
    parity = Even
    '''
    rx_data = []
    slave_id = b'\x02'  # Slave ID = 0x01
    func_code = b'\x04'  # Read holding register 0x03
    pdu_register = register.to_bytes(2, 'big')
    length = b'\x00\x01'

    tx_data = b''.join([slave_id, func_code, pdu_register, length])
    crc = crc16(tx_data)
    tx_data = b''.join([tx_data, crc])

    rs485.write(tx_data)
    time.sleep(0.05)
    print(tx_data)
    print("wating rx data")
    while ~rs485.in_waiting:
        if rs485.in_waiting:
            break

    while rs485.in_waiting > 0:
        rx_data.append(rs485.read())

    # print(tx_data)
    print(rx_data)

    return rx_data

    # return tx_data


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


def modbus_4bytedata_decoder(data: list):
    decode_data = 0

    # int(big) :                >i
    decode_data = struct.unpack('>i', b''.join(data))
    print('int(big) :                ' + str(decode_data[0]))

    # int(little) :             <i
    decode_data = struct.unpack('<i', b''.join(data))
    print('int(little) :             ' + str(decode_data[0]))

    # unsigned int(big) :       >I
    decode_data = struct.unpack('>I', b''.join(data))
    print('unsigned int(big) :       ' + str(decode_data[0]))

    # unsigned int(little) :    <I
    decode_data = struct.unpack('<I', b''.join(data))
    print('unsigned int(little) :    ' + str(decode_data[0]))

    # long(big) :               >l
    decode_data = struct.unpack('>l', b''.join(data))
    print('long(big) :               ' + str(decode_data[0]))

    # long(little) :            <l
    decode_data = struct.unpack('<l', b''.join(data))
    print('long(little) :            ' + str(decode_data[0]))

    # unsigned long(big) :      >L
    decode_data = struct.unpack('>L', b''.join(data))
    print('unsigned long(big) :      ' + str(decode_data[0]))

    # unsigned long(little) :   <L
    decode_data = struct.unpack('<L', b''.join(data))
    print('unsigned long(little) :   ' + str(decode_data[0]))

    # float(big) :              >f
    decode_data = struct.unpack('>f', b''.join(data))
    print('float(big) :              ' + str(decode_data[0]))

    # float(little) :           <f
    decode_data = struct.unpack('<f', b''.join(data))
    print('float(little) :           ' + str(decode_data[0]))

    # # reverse
    # print('')
    # print('reverse')
    # decode_data1 = rx_data[3:5]
    # decode_data2 = rx_data[5:7]
    # decode_data = decode_data2 + decode_data1
    # decode_data = struct.unpack('>f', b''.join(decode_data))
    # print('Float(big) : ' + str(decode_data[0]))

    # decode_data1 = rx_data[3:5]
    # decode_data2 = rx_data[5:7]
    # decode_data = decode_data2 + decode_data1
    # decode_data = struct.unpack('<f', b''.join(decode_data))
    # print('Float(little) : ' + str(decode_data[0]))

    # decode_data1 = rx_data[3:5]
    # decode_data2 = rx_data[5:7]
    # decode_data = decode_data2 + decode_data1
    # decode_data = struct.unpack('>I', b''.join(decode_data))
    # print('Int(big) : ' + str(decode_data[0]))

    # decode_data1 = rx_data[3:5]
    # decode_data2 = rx_data[5:7]
    # decode_data = decode_data2 + decode_data1
    # decode_data = struct.unpack('<I', b''.join(decode_data))
    # print('Int(little) : ' + str(decode_data[0]))


def find_dynamic_addr(register: int):
    rx_data1 = readModbus(register)
    time.sleep(1)
    rx_data2 = readModbus(register)
    time.sleep(1)
    rx_data3 = readModbus(register)
    time.sleep(1)
    rx_data4 = readModbus(register)

    if (rx_data1 == rx_data2) & (rx_data1 == rx_data3) & (rx_data1 == rx_data3) & (rx_data1 == rx_data4):
        print(str(register) + ' : Static')
    else:
        print(str(register) + ' : Dynamic')
        # print(rx_data4)
        # modbus_4bytedata_decoder(rx_data4[3:7])


if __name__ == "__main__":
    rs485 = serial.Serial()
    # rs485.port = '/dev/tty.usbserial-A10KMET7'
    rs485.port = 'COM60'
    rs485.baudrate = 19200
    # rs485.parity = serial.PARITY_EVEN
    rs485.open()

    # print(rs485.name)
    # rs485.close()
    # readModbus(0,0)
    # get_crc = crc_16(b'\x01\x03\x01\x2f\x00\x01')
    # print(get_crc)
    # tx_data = b'\x01\x03\x01\x2f\x00\x01'
    # get_crc = crc16(tx_data)
    # print('0x' + get_crc.hex().upper())

    # tx_data = b''.join([tx_data, get_crc])
    # print('0x' + tx_data.hex().upper())

    # '''
    # Convert int to unit16_t
    # '''
    # i = 1130
    # tx_data = i.to_bytes(2, 'big')
    # print('0x' + tx_data.hex().upper())

    print('Start scanning')
    # Read holding register
    # Not found at 40000 to 42268
    # Not found at 1 to 999
    # Scan from 1000 to 9999 : Found at 1000,1001,1002,1003,1004,1005,1010
    # Scan from 10000 to 19999
    # Scan from 20000 to 65535 : Found at 65000-65027
    #
    # Read input register 0x04
    # Scan from 0 to 65535 : Found at 1000-1211, 2000-2010, 3650-3656, 65535

    # i = 65004
    # j = 0
    # err = [b'\x01', b'\x83', b'\x02', b'\xc0', b'\xf1']
    # while i < 65050:
    #     rx_data = readModbus(i)
    #     #print(str(i) + ',0x' + rx_data.hex().upper())

    #     if rx_data == [b'\x01', b'\x83', b'\x02', b'\xc0', b'\xf1']:
    #     #if rx_data == [b'\x01', b'\x84', b'\x02', b'\xc2', b'\xc1']:
    #         #print(str(i))
    #         pass
    #     else :
    #         print('')
    #         print(str(i) + '    Loop : ' + str(j))
    #         j = j + 1
    #         print(rx_data)

    #         modbus_4bytedata_decoder(rx_data[3:7])

    #     time.sleep(1)
    #     i = i + 1

    start_address = 100
    stop_address = 120
    fc01_err = [b'\x01', b'\x81', b'\x01', b'\x81', b'\x90']
    fc02_err = [b'\x01', b'\x82', b'\x01', b'\x81', b'`']
    fc03_err = [b'\x01', b'\x83', b'\x02', b'\xc0', b'\xf1']
    fc04_err = [b'\x01', b'\x84', b'\x02', b'\xc2', b'\xc1']

    while start_address <= stop_address:
        rx_data = readModbus(start_address)  # Request modbus data

        if rx_data == fc03_err:
            # Function code 03 read error
            print("fc03")
            # pass
        elif rx_data == fc04_err:
            # Function code 03 read error
            print("fc04")
            # pass
        elif rx_data == fc01_err:
            # Function code 01 read error
            print("fc01")
        # pass
        elif rx_data == fc02_err:
            # Function code 02 read error
            print("fc02")
        # pass
        else:
            # find_dynamic_addr(start_address)
            print("return data")
            # pass

        start_address = start_address + 1

    rs485.close()
    print('Done scanning')