from src.Stage.Stage import *
from src.Stage.UEFI_Shim import *

class ROM(Stage):
    """Represents the ROM stage in the boot sequence."""
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