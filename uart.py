import sys
import serial.tools.list_ports

class Uart:
    def __init__(self, baudrate=115200, fixedcomport=None, flag_simulation=False):
        self.flag_simulation = flag_simulation
        if fixedcomport is None:
            self.portname = self.getPort()
        else:
            self.portname = fixedcomport
        print(self.portname)
        self.baudrate = baudrate
        try:
            self.ser = serial.Serial(port=self.portname, baudrate=self.baudrate, timeout=1)
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            sys.exit(1)

    def getPort(self):
        ports = serial.tools.list_ports.comports()
        commPort = "None"
        if self.flag_simulation == False:
            check_string = "USB"
        else:
            check_string = "com0com"
        for port in ports:
            strPort = str(port)
            print(strPort)
            if check_string in strPort:
                splitPort = strPort.split(" ")
                commPort = splitPort[0]
                break  # Assuming you only need the first matching port
        return commPort

    def processData(self, data):
        segments = data.split("##")
        processed_data = []
        for segment in segments:
            if segment:  # Check if segment is not empty
                clean_segment = segment.replace("!", "").replace("#", "")
                splitData = clean_segment.split(":")
        return splitData

    def readSerial(self):
        mess = self.ser.read_until(b'##').decode("UTF-8")
        if mess:
            return self.processData(mess)
        return None

if __name__ == '__main__':
    uart = Uart(115200, None, True)
    while True:
        uart_data = uart.readSerial()
        if uart_data is not None:
            print(uart_data)

