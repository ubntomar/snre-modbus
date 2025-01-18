# Proyecto SRNE ML2440

Este proyecto se encarga de la comunicación con un dispositivo Modbus a través de un puerto serie para controlar y monitorear diferentes parámetros.

## Requisitos

- Python 3.x
- Biblioteca `pymodbus`
- Permisos para acceder al puerto serie
- Tener en cuenta que se debe convertir la señal tipo rs232 del ML2440 usando   un módulo  MAX232 para generar  ttl y luego con otro módulo cnvertir ttl a usb y así se establece la comunicación al PC.
## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/srne.git
   cd srne




Claro, aquí tienes un ejemplo de un archivo `README.md` para tu proyecto:

```markdown
# Proyecto SRNE

Este proyecto se encarga de la comunicación con un dispositivo Modbus a través de un puerto serie para controlar y monitorear diferentes parámetros.

## Requisitos

- Python 3.x
- Biblioteca `pymodbus`
- Permisos para acceder al puerto serie

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/srne.git
   cd srne
   ```

2. Instala las dependencias:
   ```bash
   pip install pymodbus
   ```

## Uso

1. Asegúrate de tener permisos para acceder al puerto serie:
   ```bash
   sudo usermod -aG dialout $USER
   ```

2. Ejecuta el script:
   ```bash
   sudo python3 srne.py
   ```

## Configuración

El archivo 

srne.py

 contiene varios parámetros de configuración que puedes ajustar según tus necesidades:

- `baudrate`: Velocidad de comunicación en baudios.
- `port`: Puerto serie al que está conectado el dispositivo.
- `stopbits`, `parity`, `bytesize`, `timeout`: Otros parámetros de configuración del puerto serie.
- 

unit_id

: Dirección Modbus del dispositivo.
- `register_*`: Direcciones de los registros Modbus para diferentes parámetros.

## Ejemplo de Código

```python
import logging
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

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
register_load_control = 0x010A
register_battery_voltage = 0x0101

client = ModbusClient(
    port=port,
    baudrate=baudrate,
    stopbits=stopbits,
    parity=parity,
    bytesize=bytesize,
    timeout=timeout
)

# Conexión
if client.connect():
    logging.info(f"Conexión exitosa con baudrate: {baudrate}")
    try:
        # Leer el voltaje de la batería
        result = client.read_holding_registers(register_battery_voltage, count=1, unit=unit_id)
        if not result.isError():
            battery_voltage = result.registers[0] / 100.0
            logging.info(f"Voltaje de la batería: {battery_voltage} V")
        else:
            logging.error(f"Error al leer el voltaje de la batería: {result}")

        # Control de carga (ejemplo: encender la carga)
        load_control_value = 1  # 1 para encender, 0 para apagar
        result = client.write_register(register_load_control, load_control_value, unit=unit_id)
        if not result.isError():
            logging.info(f"Control de carga establecido a: {load_control_value}")
        else:
            logging.error(f"Error al establecer el control de carga: {result}")

    except Exception as e:
        logging.error(f"Excepción durante la comunicación Modbus: {e}")
    finally:
        client.close()
else:
    logging.error(f"Error con baudrate {baudrate}: No se pudo conectar al puerto {port}")
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que desees realizar.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
```

