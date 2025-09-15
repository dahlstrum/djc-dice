import hmac
import hashlib

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
