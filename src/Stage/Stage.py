import hmac
import hashlib

class Stage():
    """Base class for a boot stage in the device's boot sequence."""
    def __init__(self, image):
        self._image = image
        self._CDI = None
        self._next = None
    
    def set_CDI(self, cdi):
        """Set the Composite Device Identifier for this stage."""
        self._CDI = cdi

    def set_next(self, next):
        """Set the next stage in the boot sequence."""
        self._next = next

    @classmethod
    def get_label(cls):
        """Get the label of the stage."""
        return "Stage"

    @classmethod
    def calculate_CDI(cls, secret, stage_hash):
        """Calculate the Composite Device Identifier using HMAC-SHA256."""
        return hmac.new(secret, stage_hash, digestmod=hashlib.sha256).digest()
    
    @classmethod
    def measure(cls, image):
        """Measure the image by computing its SHA-256 hash."""
        m = hashlib.sha256()
        m.update(image)
        return m.hexdigest().encode('utf-8')
    
    def get_image(self):
        """Get the image associated with this stage."""
        return self._image

    def execute(self):
        """Simulate the execution of this stage by printing its label."""
        print(f"INFO: Execution of the stage... { self.get_label() }")
