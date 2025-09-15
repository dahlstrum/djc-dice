from src.Device.Fuse import *
from src.Stage.ROM import *

class MockDevice():
    __secret = None
    current_stage = None

    def __init__(self):
        print("INFO: initializing device...")

        otp = Fuse()
        otp.blow()
        self.__secret = DeviceSecret(otp)
        

    def boot(self):
        rom = ROM()
        self.current_stage = rom

        # execute the special case first stage (ROM)
        self.current_stage.execute()

        # Use ROM to measure next boot stage
        next_stage_measurement = ROM.measure(self.current_stage.get_next().get_image().encode('utf-8'))
        print(f"INFO: { self.current_stage.get_label() } taking measurement of next stage { self.current_stage.get_next().get_label() }: { next_stage_measurement }")

        # temporarily stored device UDS for initial CDI calculation
        temp_uds = self.__secret.read

        cdi = ROM.calculate_CDI(temp_uds, next_stage_measurement)
        # delete uds from memory and lock device secret
        del temp_uds
        self.__secret.lock()

        
        # rom.set_CDI(cdi.hex())
        rom.set_CDI(cdi)
       
        while(self.current_stage.get_next() != None):
            print(f'INFO: \tStage: { self.current_stage.get_next().get_label() }; CDI: { cdi.hex() } ')
            self.current_stage = self.current_stage.get_next()
            self.current_stage.execute()

            if self.current_stage.get_next() != None:
                next_stage_measurement = self.current_stage.measure(self.current_stage.get_next().get_image().encode('utf-8'))
                print(f"INFO: { self.current_stage.get_label() } taking measurement of next stage { self.current_stage.get_next().get_label() }: { next_stage_measurement }")
                # use current stage to calculate next CDI
                cdi = self.current_stage.calculate_CDI(cdi, next_stage_measurement)
        
        return cdi.hex()
    
class DeviceSecret():
    __UDS = r''
    
    def __init__(self, fuse):
        if len(self.__UDS) == 0 or self.__UDS == None:
            print("INFO: setting UDS")
            self.__UDS = fuse.read

        print("INFO: initializing device secret object store")
        self.can_read_latch = True

    def lock(self):
        print("INFO: locking UDS")
        self.can_read_latch = False

    @property
    def read(self):
        if self.can_read_latch:
            return self.__UDS
        
        elif not self.can_read_latch:
            raise Exception('ERROR: Device Secret is not readable')
        
        Exception('ERROR: latch in unknown state')