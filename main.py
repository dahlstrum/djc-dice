from src.Stage.Stage import *
from src.Stage.ROM import *
from src.Device.Device import *

if __name__ == "__main__":
    deviceA = MockDevice()
    resultCDI = deviceA.boot()
    print("INFO: Device boot complete!")
    print(f"DEBUG: CDI: { resultCDI }")
