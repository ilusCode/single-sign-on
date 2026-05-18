from enum import Enum

class FlowMode(Enum):
    """
    Enum representing the available flow modes for encryption.

    PSWD_AES_256_CBC: Password-based AES 256 CBC encryption.
    USR_AES_256_CBC: User-based AES 256 CBC encryption.
    """
    PSWD_AES_256_CBC = "PSWD_AES_256_CBC"
    USR_AES_256_CBC = "USR_AES_256_CBC"