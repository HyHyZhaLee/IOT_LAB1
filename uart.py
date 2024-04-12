import sys
import serial.tools.list_ports

class Uart:
    def __init__(self, baudrate=115200, fixedcomport=None, flag_simulation=False):
        self.flag_simulation = flag_simulation
        self.buffer = []
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
        data = data.replace("!", "")
        data = data.replace("#", "")
        splitData = data.split(":")
        self.buffer.append(splitData)

    def readSerial(self):
        bytesToRead = self.ser.inWaiting()
        if (bytesToRead > 0):
            mess = self.ser.read(bytesToRead).decode("UTF-8")
            while ("#" in mess) and ("!" in mess):
                start = mess.find("!")
                end = mess.find("#")
                self.processData(mess[start:end + 1])
                if (end == len(mess)):
                    mess = ""
                else:
                    mess = mess[end + 1:]
        return self.buffer

    def writeSerial(self, data):
        try:
            self.ser.write(data.encode("UTF-8"))
        except serial.SerialException as e:
            print(f"Error writing to serial port: {e}")

    def clearData(self):
        # Assuming you process data elsewhere and know which to remove
        self.buffer = []  # Resetting the buffer, implement more nuanced clearing as needed

if __name__ == '__main__':
    uart = Uart(115200, None, True)
    while True:
        uart_data = uart.readSerial()
        if len(uart_data) > 0 :
            for data in uart_data:
                print(data)
                uart.clearData()

