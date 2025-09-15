from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

class Fuse():
    """Simulate a hardware fuse that can be blown to generate a device secret."""
    __secret = ""
    _blown = False

    def __init__(self):
        print("INFO: initializing fuse...")
        self._blown = False

    @property
    def is_blown(self):
        """Return a boolean indicating if the fuse has been blown."""
        return self._blown

    @property
    def read(self):
        """Read the device secret"""
        return self.__secret

    def blow(self):
        """Blow the fuse to generate and store the device secret."""
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
