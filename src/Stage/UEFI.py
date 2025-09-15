from src.Stage.Stage import *
from src.Stage.Kernel import *

class UEFI(Stage):
    """Represents the UEFI stage in the boot sequence."""
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