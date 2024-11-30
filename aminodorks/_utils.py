from os import urandom
from hashlib import sha1
from typing import Final
from hmac import HMAC, new
from functools import reduce
from msgspec import json

from base64 import (
    b64encode,
    b64decode
)


PREFIX: Final[bytes] = bytes.fromhex("19")
DEVICE_KEY: Final[bytes] = bytes.fromhex("E7309ECC0953C6FA60005B2765F99DBBC965C8E9")
SIGNATURE_KEY: Final[bytes] = bytes.fromhex("DFA5ED192DDA6E88A12FE12130DC6206B1251E44")

def generate_signature(data: bytes) -> str:
    return b64encode(PREFIX + new(
        SIGNATURE_KEY, data, sha1
        ).digest()
    ).decode("utf-8")

def generate_device_id() -> str:
    identifier: bytes = PREFIX + urandom(20)
    mac: HMAC = new(DEVICE_KEY, identifier, sha1) 
    return f"{identifier.hex()}{mac.hexdigest()}".upper()

def decode_session_id(session_id: str) -> dict:
    return json.decode(b64decode(reduce(lambda a, e: a.replace(*e), ("-+", "_/"), session_id + "=" * (-len(session_id) % 4)).encode())[1:-20].decode())

def session_id_to_user_id(session_id: str) -> str: return decode_session_id(session_id)["2"]
