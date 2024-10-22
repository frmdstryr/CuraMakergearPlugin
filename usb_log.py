# Copyright (c) 2024 Jairus Martin
# Released under the terms of the LGPLv3 or higher.
from UM.Logger import Logger
from serial import Serial

_default_write = Serial.write
_default_readline = Serial.readline


def write(self: Serial, data: bytes):
    Logger.log("i", f"Sent: {self.port}: {data}")
    _default_write(self, data)


def readline(self: Serial) -> bytes:
    line = _default_readline(self)
    if line:
        Logger.log("i", f"Read: {self.port}: {line}")
    return line


def install():
    Serial.write = write
    Serial.readline = readline
