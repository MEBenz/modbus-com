from modbus import ModbusRTUDevice

aircon = ModbusRTUDevice()

aircon.begin('port name', 19200)

aircon.readRawData(slave_id=1, func_code=3, register=1)
