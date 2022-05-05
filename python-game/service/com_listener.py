import serial


class Listener:
    def __init__(self):
        self.port = None
        self.serial_speed = None

        self.arduino = None
        self.is_connected = False

        # For test
        # self.file1 = open('/Users/markguranov/Downloads/resource/BettaGame.dat', 'r')
        # self.lines = self.file1.readlines()
        # self.line = 0

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
        # data = self.lines[self.line].replace('\n', '').split('\t')
        # self.line += 1
        data = [650, 2.16]
        if self.is_connected:
            try:
                eeg = self.arduino.readline().decode("utf-8").strip('\r\n').split(',')
                if len(eeg) == 2:
                    data = eeg
            except Exception as e:
                self.is_connected = False
                print(e)
                self.connection(self.port, self.serial_speed)

        return float(data[1])
