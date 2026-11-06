import json, os

from serial_port import SerialPort


class Voltronic:
    def __init__(self):
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'sensors.json')
        with open(file_path) as json_file:
            self.sensors = json.load(json_file)

        self.port = SerialPort()

    def poll(self, queries):
        try:
            for query in queries:
                self.update(query)
            return True
        except (ValueError, IndexError, KeyError, TypeError) as e:
            print(f"Inverter polling error: {e}", flush=True)
            return False

    def update(self, query):
        query_bytes = query_to_bytes(query)
        response = self.require(query_bytes)
        self.unpack_data(query, response)

    def require(self, query_bytes):
        return self.port.request(query_bytes)

    def print_sensors(self):
        for query in self.sensors:
            for sensor in self.sensors[query]:
                value = self.sensors[query][sensor].get('value', None)
                print(f"{sensor}: {value}")

    def unpack_data(self, query, data):
        types = {"str": str, "float": float, "int": int}
        try:
            print("👉data", data)
            data = data[0]

            data = data.decode('latin1').strip()[1:-2].split(" ")
            sensors = self.sensors.get(query, {})
            for sensor, sensor_info in sensors.items():
                index = sensor_info['index']

                if sensor == 'warnings':
                    value = get_warning(data[index])
                else:
                    type_func = types[sensor_info['type']]
                    value = type_func(data[index])
                sensors[sensor]['value'] = value

        except Exception as e:
            print(f"Error unpacking data: {e}, query: {query}, data: {data}")
            raise


def get_warning(data):
    warnings_list = [
        "", "Inverter fault", "Bus over fault", "Bus under fault", "Bus soft fail fault",
        "Line fail warning", "OPV short warning", "Inverter voltage too low fault",
        "Inverter voltage too high fault", "Over temperature fault", "Fan locked fault",
        "Battery voltage too high fault", "Battery low alarm warning", "Reserved",
        "Battery under shutdown warning", "Reserved", "Overload fault", "EEPROM fault",
        "Inverter over current fault", "Inverter soft fail fault", "Self test fail fault",
        "OP DC voltage over fault", "Battery open fault", "Current sensor fail fault",
        "Battery short fault", "Power limit warning", "PV voltage high warning",
        "MPPT overload fault", "MPPT overload warning", "Battery too low to charge warning",
        "", "",
    ]
    bit_string = data.rjust(32, '0')
    return ', '.join([warnings_list[i] for i, bit in enumerate(bit_string) if bit == '1'])


def query_to_bytes(query):
    command_bytes = bytearray(query.encode())
    crc_high, crc_low = crc(command_bytes)
    ba = bytearray([crc_high, crc_low, 13])
    command_bytes.extend(ba)
    return command_bytes


def crc(data_bytes):
    """
    Calculates CRC for supplied data_bytes
    """
    crc = 0
    da = 0
    crc_ta = [
        0x0000,
        0x1021,
        0x2042,
        0x3063,
        0x4084,
        0x50A5,
        0x60C6,
        0x70E7,
        0x8108,
        0x9129,
        0xA14A,
        0xB16B,
        0xC18C,
        0xD1AD,
        0xE1CE,
        0xF1EF,
    ]

    for c in data_bytes:
        if type(c) == str:
            c = ord(c)
        da = ((crc >> 8) & 0xFF) >> 4
        crc = (crc << 4) & 0xFFFF

        index = da ^ (c >> 4)
        crc ^= crc_ta[index]

        da = ((crc >> 8) & 0xFF) >> 4
        crc = (crc << 4) & 0xFFFF

        index = da ^ (c & 0x0F)
        crc ^= crc_ta[index]

    crc_low = crc & 0xFF
    crc_high = (crc >> 8) & 0xFF

    if crc_low == 0x28 or crc_low == 0x0D or crc_low == 0x0A or crc_low == 0x00:
        crc_low += 1
    if crc_high == 0x28 or crc_high == 0x0D or crc_high == 0x0A or crc_high == 0x00:
        crc_high += 1

    crc = crc_high << 8
    crc += crc_low
    return [crc_high, crc_low]
