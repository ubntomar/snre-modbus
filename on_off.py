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