import logging
from pymodbus.client import ModbusSerialClient

# Configuración del logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Parámetros de configuración
baudrate = 9600
port = '/dev/ttyUSB0'
stopbits = 1
parity = 'N'
bytesize = 8
timeout = 1

# Dirección Modbus del dispositivo y registros de control
unit_id = 1
register_load_control = 0x010A     # Control de la carga (encendido/apagado)
register_battery_voltage = 0x0101  # Voltaje de la batería
register_solar_current = 0x0108    # Corriente desde los paneles solares al controlador
register_battery_current = 0x0105  # Corriente hacia los dispositivos conectados (carga)
register_load_status = 0x0120      # Estado de la carga (encendida/apagada)
# Leer voltajes de carga y desconexión
register_boost_voltage = 0xE008    # Boost Charging Voltage
register_lvd = 0xE00D              # Low Voltage Disconnect
register_lvr = 0xE00B              # Low Voltage Reconnect

#
new_lvr_value = 126  #  escalado (en décimas de voltio)
new_lvd_value = 119  #  escalado (en décimas de voltio)


client = ModbusSerialClient(
    port=port,
    baudrate=baudrate,
    stopbits=stopbits,
    parity=parity,
    bytesize=bytesize,
    timeout=timeout
)

# Conexión
if client.connect():
    print("Conexión establecida con éxito.")
    import time

    logging.debug("Enviando comando para encender la carga...")
    response_on = client.write_register(register_load_control, 1, slave=unit_id)
    if not response_on.isError():
        print("Carga encendida con éxito.")
    else:
        print(f"Error al encender la carga: {response_on}")

    time.sleep(5)

    # logging.debug("Enviando comando para apagar la carga...")
    # response_off = client.write_register(register_load_control, 0, slave=unit_id)
    # if not response_off.isError():
    #     print("Carga apagada con éxito.")
    # else:
    #     print(f"Error al apagar la carga: {response_off}")
    time.sleep(10)
    # Leer el voltaje de la batería
    result = client.read_holding_registers(register_battery_voltage, count=1)
    if not result.isError():
        battery_voltage = result.registers[0] / 10.0
        logging.info(f"Voltaje de la batería: {battery_voltage} V")
    else:
        logging.error(f"Error al leer el voltaje de la batería: {result}")

    # Leer la corriente de carga de los paneles solares
    result = client.read_holding_registers(register_solar_current, count=1)
    if not result.isError():
        solar_current = result.registers[0] / 100.0  # La corriente está en centésimas de amperio
        logging.info(f"Corriente de carga generada en los paneles solares: {solar_current} A")
    else:
        logging.error(f"Error al leer la corriente de carga generada los paneles solares: {result}")

    # Leer la corriente de descarga de la batería
    result = client.read_holding_registers(register_battery_current, count=1)
    if not result.isError():
        battery_current = result.registers[0] / 100.0  # La corriente está en centésimas de amperio
        logging.info(f"Corriente hacia los dispositivos conectados (carga): {battery_current} A")
    else:
        logging.error(f"Error al leer la Corriente hacia los dispositivos conectados (carga): {result}")

    # Leer el estado de la carga
    result = client.read_holding_registers(register_load_status, count=1)
    if not result.isError():
        load_status = result.registers[0]  # Registro completo de 16 bits
        high_byte = (load_status >> 8) & 0xFF  # Extraemos los 8 bits altos
        load_on = (high_byte & 0x80) >> 7  # Bit 7 indica encendido/apagado

        if load_on:
            logging.info("La carga está encendida.")
        else:
            logging.info("La carga está apagada.")
        logging.debug(f"Datos del registro: {bin(load_status)}")
    else:
        logging.error(f"Error al leer el estado de la carga: {result}")
    


    # Leer Boost Voltage
    result_boost = client.read_holding_registers(register_boost_voltage, count=1)
    if not result_boost.isError():
        boost_voltage = result_boost.registers[0] / 10.0  # Dividimos entre 10 para obtener voltios
        logging.info(f"Boost Voltage: {boost_voltage} V")

    # Leer LVD
    result_lvd = client.read_holding_registers(register_lvd, count=1)
    if not result_lvd.isError():
        lvd_voltage = result_lvd.registers[0] / 10.0
        logging.info(f"Low Voltage Disconnect (LVD): {lvd_voltage} V")

    # Leer LVR
    result_lvr = client.read_holding_registers(register_lvr, count=1)
    if not result_lvr.isError():
        lvr_voltage = result_lvr.registers[0] / 10.0
        logging.info(f"Low Voltage Reconnect (LVR): {lvr_voltage} V")

    # Modificar el valor de LVR
    response_lvr = client.write_register(register_lvr, new_lvr_value, slave=unit_id)
    if not response_lvr.isError():
        logging.info(f"Se ha actualizado el Low Voltage Reconnect (LVR) a {new_lvr_value/10} con éxito.")
    else:
        logging.error(f"Error al actualizar el valor de LVR: {response_lvr}")    
    time.sleep(5)

    # Leer LVR
    result_lvr = client.read_holding_registers(register_lvr, count=1)
    if not result_lvr.isError():
        lvr_voltage = result_lvr.registers[0] / 10.0
        logging.info(f"Low Voltage Reconnect (LVR): {lvr_voltage} V")    

    # Modificar el valor de LVD
    response_lvd = client.write_register(register_lvd, new_lvd_value, slave=unit_id)
    if not response_lvd.isError():
        logging.info(f"Se ha actualizado el Low Voltage Disconnect (LVD) a {new_lvd_value/10} con éxito.")
    else:
        logging.error(f"Error al actualizar el valor de LVD: {response_lvd}")    