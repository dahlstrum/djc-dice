from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

class Fuse():
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
