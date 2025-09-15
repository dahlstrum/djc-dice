from src.Stage.Stage import *
from src.Stage.UEFI import *

class UEFI_Shim(Stage):
    """Represents the UEFI Shim stage in the boot sequence."""
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
