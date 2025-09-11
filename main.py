
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

import hmac
import hashlib
import string

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

class Fuse():
    __chars = string.ascii_uppercase + string.digits
    __secret = ""
    _blown = False

    def __init__(self):
        print("INFO: initializing fuse...")
        self._blown = False

    @property
    def is_blown(self):
        return self._blown

    @property
    def read(self):
        return self.__secret

    def blow(self):
        if self._blown:
            print("WARN: fuse already blown!")
        if not self._blown:
            print("INFO: blowing fuse...")
            self._blown = True

            print("INFO: generating RSA key for device secret...")
            self.__secret = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            ).private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )

class Stage():
    def __init__(self, image):
        self._image = image
        self._CDI = None
        self._next = None
    
    def set_CDI(self, cdi):
        self._CDI = cdi

    def set_next(self, next):
        self._next = next

    @classmethod
    def get_label(cls):
        return "Stage"

    @classmethod
    def calculate_CDI(cls, secret, stage_hash):
        return hmac.new(secret, stage_hash, digestmod=hashlib.sha256).digest()
    
    @classmethod
    def measure(cls, image):
        m = hashlib.sha256()
        m.update(image)
        return m.hexdigest().encode('utf-8')
    
    def get_image(self):
        return self._image

    def execute(self):
        print(f"INFO: Execution of the stage... { self.get_label() }")

class ROM(Stage):
    def __init__(self):
        super().__init__('ROM_image')
    
    @classmethod
    def get_label(cls):
        return "ROM"
    
    @classmethod
    def calculate_CDI(cls, secret, stage_hash):
        return super(ROM, cls).calculate_CDI(secret, stage_hash)

    @classmethod
    def measure(cls, image):
        return super(ROM, cls).measure(image)

    def set_CDI(self, cdi):
        super().set_CDI(cdi)

    def set_next(self, next):
        super().set_next(next)
    
    def get_next(self):
        if self._next == None or self._next =='':
            self._next = UEFI_Shim()
        return self._next

    def get_image(self):
        return super().get_image()



class UEFI_Shim(Stage):
    def __init__(self):
        super().__init__('UEFI_shim_image')
    
    @classmethod
    def get_label(cls):
        return "UEFI_Shim"

    @classmethod
    def calculate_CDI(cls, secret, stage_hash):
        return super(UEFI_Shim, cls).calculate_CDI(secret, stage_hash)

    @classmethod
    def measure(cls, image):
        return super(UEFI_Shim, cls).measure(image)

    def get_next(self):
        if self._next == None or self._next =='':
            self._next = UEFI()
        return self._next

    def get_image(self):
        return super().get_image()


class UEFI(Stage):
    def __init__(self):
        super().__init__('UEFI_image')

    @classmethod
    def get_label(cls):
        return "UEFI"

    @classmethod
    def calculate_CDI(cls, secret, stage_hash):
        return super(UEFI, cls).calculate_CDI(secret, stage_hash)

    @classmethod
    def measure(cls, image):
        return super(UEFI, cls).measure(image)
    
    def get_next(self):
        if self._next == None or self._next =='':
            self._next = Kernel()
        return self._next


class Kernel(Stage):
    def __init__(self):
        super().__init__('kernel_image')

    @classmethod
    def get_label(cls):
        return "kernel"

    @classmethod
    def calculate_CDI(cls, secret, stage_hash):
        return super(Kernel, cls).calculate_CDI(secret, stage_hash)

    @classmethod
    def measure(cls, image):
        return super(Kernel, cls).measure(image)

    def get_next(self):
        if self._next == None or self._next =='':
            self._next = None
        return self._next



if __name__ == "__main__":
    deviceA = MockDevice()
    resultCDI = deviceA.boot()
    print("INFO: Device boot complete!")
    print(f"DEBUG: CDI: { resultCDI }")
