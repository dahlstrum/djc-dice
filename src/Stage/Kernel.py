from src.Stage.Stage import *

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
