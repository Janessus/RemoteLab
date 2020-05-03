OUT = 1
BCM = 1
HIGH = 1
LOW = 0

def setmode(val):
    print("Mode = " + str(val))

def setup(pin, val):
    print("Setup: pin=" + str(pin) + ", value=" + str(val))

def output(pin, val):
    print("Output: pin=" + str(pin) + ", value=" + str(val))
