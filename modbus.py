import serial
import time


class ModbusRTUDevice:

    def __init__(self):
        """
        initial the ModbusDevice
        :param :
        :return:
        """
        self.rs485 = None

    def crc16(data: bytes, poly: hex = 0xA001):
        """
        Modbus CRC16 calculation
        :param data:
        :return crc16:
        """
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

        crc16 = crc.to_bytes(2, 'little')  # CRC_16 Bigendian format

        return crc16

    def begin(self, port: str, baudrate: int):
        """
        Initialize the RS485 port
        :param port:
        :param baudrate:
        :return :
        """
        self.rs485 = serial.Serial()
        self.rs485.port = port
        self.rs485.baudrate = baudrate
        self.rs485.open()

    def close(self):
        """
        Close the connection of RS485 port
        :param :
        :return :
        """
        if self.rs485 is not None:
            if self.rs485.isOpen():
                self.rs485.close()

    def readRawData(self, slave_id: int, func_code: int, register: int):
        """
        Read data from modbus register
        :param :
        :return :
        """
        rx_data = []
        slave_id_bytes = slave_id.to_bytes(1, 'big')
        func_code_bytes = func_code.to_bytes(1, 'big')
        pdu_register = register.to_bytes(2, 'big')

        length = b'\x00\x01'

        tx_data = b''.join([slave_id_bytes, func_code_bytes, pdu_register, length])
        crc = self.crc16(tx_data)
        tx_data = b''.join([tx_data, crc])

        self.rs485.write(tx_data)
        time.sleep(0.05)
        print(tx_data)
        print("waiting rx data")
        while ~self.rs485.in_waiting:
            if self.rs485.in_waiting:
                break

        while self.rs485.in_waiting > 0:
            rx_data.append(self.rs485.read())

        # print(tx_data)
        print(rx_data)

        return rx_data
