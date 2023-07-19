from ..colors.csrgb_ren import CSRGB
from ..colors.csrgba_ren import CSRGBA

"""renpy
init -1 python:
"""

################################################################################
#
#   Package Internal Functions
#
################################################################################

def _ubyte_to_hex(value: int) -> str:
    return __seg_to_hex(value >> 4) + __seg_to_hex(value & 15)

def _parse_hex(hex: str) -> CSRGB | CSRGBA:
    _validate_hex(hex)

    h = hex[1:]
    l = len(h)

    if l == 3:
        return __short_hex_to_rgb(h)
    elif l == 4:
        return __short_hex_to_rgba(h)
    elif l == 6:
        return __long_hex_to_rgb(h)
    elif l == 8:
        return __long_hex_to_rgba(h)
    else:
        raise Exception('illegal state')

def _validate_hex(hex: str):
    l = len(hex)

    if not (l == 4 or l == 5 or l == 7 or l == 9):
        raise Exception("invalid hex string '{}': must be 4, 5, 7, or 9 characters in length".format(hex))

    if not hex.startswith('#'):
        raise Exception("invalid hex string '{}': must start with a '#' character".format(hex))

    for i in range(1, len(hex)):
        if not __is_hex_digit(hex[i]):
            raise Exception("invalid hex string '{}': character {} ({}) is not a valid hex digit".format(hex, i, hex[i]))


################################################################################
#
#   Module Internal Functions
#
################################################################################

def __seg_to_hex(value: int) -> str:
    if value < 10:
        return chr(value + 48)
    elif value < 16:
        return chr((value - 10) + 97)

def __short_hex_to_rgb(hex: str) -> CSRGB:
    return CSRGB(
        (__hex_to_seg(hex[0]) << 4) | __hex_to_seg(hex[0]),
        (__hex_to_seg(hex[1]) << 4) | __hex_to_seg(hex[1]),
        (__hex_to_seg(hex[2]) << 4) | __hex_to_seg(hex[2]),
    )

def __short_hex_to_rgba(hex: str) -> CSRGBA:
    return CSRGBA(
        (__hex_to_seg(hex[0]) << 4) | __hex_to_seg(hex[0]),
        (__hex_to_seg(hex[1]) << 4) | __hex_to_seg(hex[1]),
        (__hex_to_seg(hex[2]) << 4) | __hex_to_seg(hex[2]),
        (__hex_to_seg(hex[3]) << 4) | __hex_to_seg(hex[3]),
    )

def __long_hex_to_rgb(hex: str) -> CSRGB:
    return CSRGB(
        (__hex_to_seg(hex[0]) << 4) | __hex_to_seg(hex[1]),
        (__hex_to_seg(hex[2]) << 4) | __hex_to_seg(hex[3]),
        (__hex_to_seg(hex[4]) << 4) | __hex_to_seg(hex[5]),
    )

def __long_hex_to_rgba(hex: str) -> CSRGBA:
    return CSRGBA(
        (__hex_to_seg(hex[0]) << 4) | __hex_to_seg(hex[1]),
        (__hex_to_seg(hex[2]) << 4) | __hex_to_seg(hex[3]),
        (__hex_to_seg(hex[4]) << 4) | __hex_to_seg(hex[5]),
        (__hex_to_seg(hex[6]) << 4) | __hex_to_seg(hex[7]),
    )

def __hex_to_seg(hex: str) -> int:
    if '0' <= hex <= '9':
        return ord(hex) - 48
    elif 'A' <= hex <= 'F':
        return ord(hex) - 55
    elif 'a' <= hex <= 'f':
        return ord(hex) - 87
    else:
        raise Exception("invalid hex digit '{}'".format(hex))

def __is_hex_digit(hex: str) -> bool:
    return '0' <= hex <= '9' or 'A' <= hex <= 'F' or 'a' <= hex <= 'f'
