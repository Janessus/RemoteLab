import time

# import RPi.GPIO as GPIO
import mockGPIO as GPIO


class Port:
    def __init__(self):
        self.value = 0
        self.pinMapping = list()

    def setMapping(self, pinList):
        self.pinMapping = pinList
        GPIO.setmode(GPIO.BCM)

        for pin in self.pinMapping:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def setValue(self, value):
        i = 0
        for pin in self.pinMapping:
            GPIO.output(pin, (1 if ((value & (1 << i)) > 0) else 0))
            i += 1


class AtMegaModule:
    def __init__(self):
        self.port = Port()

    def getPort(self):
        return self.port

    def update(self, value):
        self.port.setValue(value)


'''
Keyboard Button Index
    0  1  2
    3  4  5
    6  7  8
    9 10 11
'''
class KeyBoard(AtMegaModule):
    def input(self, number):
        pass


class Buttons(AtMegaModule):
    def input(self, number):
        self.port.setValue(number)
        time.sleep(.5)
        self.port.setValue(0)


class Switches(AtMegaModule):
    def input(self, number):
        self.port.setValue(self.port.value ^ number)


class AtMega2561:
    def __init__(self):
        # self.keyBoard = KeyBoard()
        self.switches = Switches()
        self.buttons = Buttons()

        # define rpi-pins for mappings to Port, map -> rpi_pin to listIndex=PinOnAtmegaPort
        # left to right: rpi Pin24 = AtMegaPin0 ...
        switchMapping = [24, 25, 8, 7, 12, 16, 20, 21]
        buttonMapping = [4, 17, 27, 22, 5, 6, 13, 19]

        self.switches.port.setMapping(switchMapping)
        self.buttons.port.setMapping(buttonMapping)
