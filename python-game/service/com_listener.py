import serial


class Listener:
    def __init__(self):
        self.port = None
        self.serial_speed = None

        self.arduino = None
        self.is_connected = False

    def connection(self, port, serial_speed):
        connection_flag = True
        try:
            self.port = port
            self.serial_speed = int(serial_speed)
            self.arduino = serial.Serial(port=self.port, baudrate=self.serial_speed)
        except Exception as e:
            connection_flag = False
            print(e)
        finally:
            self.is_connected = connection_flag

    def read_data(self):
        data = [650, 162]
        if self.is_connected:
            try:
                eeg = self.arduino.readline().decode("utf-8").strip('\r\n').split(',')
                if len(eeg) == 2:
                    data = eeg
            except Exception as e:
                self.is_connected = False
                print(e)
        return int(data[1])
