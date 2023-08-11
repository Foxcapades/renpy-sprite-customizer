# Copyright 2023 Elizabeth Paige Harper
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# From https://github.com/Foxcapades/renpy-util-hex

from fox_requirement_ren import fox_enforce_int, fox_require_bool, fox_require_str

"""renpy
init -10 python:
"""


################################################################################
##
##   Public Functions
##
################################################################################


def fox_ubyte_to_hex(byte: int, upper: bool = False) -> str:
    """
    UByte to Hex

    Converts the given ubyte value to a hex character pair in a string.

    Arguments
    ---------
    byte : int
        UByte value to convert to hex.  This value must be between 0 and 255
        (inclusive) or an exception will be raised.
    upper : bool
        Flag indicating whether the returned hex should be uppercase.

    Returns
    -------
    str
        A 2 character hex string representing the given ubyte value.
    """
    byte  = fox_enforce_int('byte', byte)
    upper = fox_require_bool('upper', upper)

    if byte > 255 or byte < 0:
        raise Exception('"byte" must be between 0 and 255 (inclusive)')

    return __seg_to_hex(byte >> 4, upper) + __seg_to_hex(byte & 15, upper)


def fox_ubytes_to_hex(bytes: any, prefix: str = '', upper: bool = False) -> str:
    """
    UByte Iterable to Hex

    Takes the given list, tuple, or other iterable and translates the ubyte
    values fetched from that iterable into a singular hex string.

    The iterable is expected to return the ubytes in big-endian order.

    Arguments
    ---------
    bytes : any
        A list, tuple, or other iterable type from which ubyte values will be
        retrieved.
    prefix : str
        Optional prefix that will be prepended to the output hex string.  Common
        examples are '#' or '0x'.
    upper : bool
        Flag indicating whether the returned hex should be uppercase.

    Returns
    -------
    str
        A hex string built from the bytes retrieved from the given list, tuple,
        or iterable.
    """

    fox_require_str('prefix', prefix)
    fox_require_bool('upper', upper)

    if hasattr(bytes, '__iter__'):
        return prefix + __fox_bytes_to_hex(bytes, upper)

    else:
        raise Exception('"bytes" must be a list, tuple, or other iterable of ubyte values.')


def fox_int_to_hex(
    value: int,
    min_width: int = 2,
    prefix: str = '',
    upper: bool = False
) -> str:
    """
    Int to Hex

    Converts the given int value into a hex string with an optional prefix.

    Int values must be greater than or equal to zero.

    Arguments
    ---------
    value : int
        Positive int value to convert to a hex string.
    min_width : int
        Positive int value that specifies the minimum width of the returned hex
        string (minus the prefix).  If the int value is not large enough to meet
        this minimum width, the hex string will be padded with zeros.

        Default = 2
    prefix : str
        Optional prefix value that will be prepended onto the returned hex
        value.  Common examples include '#' and '0x'.

        Default = ''
    upper : bool
        Whether the returned hex string should be uppercased.

        Default = False

    Returns
    -------
    str
        Generated hex string.
    """

    value = fox_enforce_int('value', value)
    if value < 0:
        raise Exception('negative values not supported')

    min_width = fox_enforce_int('min_width', min_width)
    if min_width < 0:
        raise Exception('min_width must be greater than or equal to zero')

    fox_require_str('prefix', prefix)
    fox_require_bool('upper', upper)

    # If the value is zero, then no need to do any math, just return a string
    # of zeros.
    if value == 0:
        return prefix + (0 * min_width)

    out = ''

    # Convert the int value to a hex string.
    while value > 0:
        byte = value & 255
        value = value >> 8

        out = fox_ubyte_to_hex(byte, upper) + out

    # Figure out if we need to pad the string with zeros to get to the target
    # width.
    rem_width = min_width - len(out)

    if rem_width > 0:
        out = ('0' * rem_width) + out

    # Prepend the prefix and return the value.
    return prefix + out


def fox_hex_to_ubytes(value: str, prefix: str = '') -> list[int]:
    """
    Hex to UBytes

    Converts the given hex string into a list of ubyte values.

    Arguments
    ---------
    value : str
        Hex string that will be parsed into a list of ubytes.
    prefix : str
        Prefix that will be stripped off the given value before it is parsed.

    Returns
    -------
    list[int]
        A list of ubyte values parsed from the given hex string.
    """
    fox_require_str('value', value)
    fox_require_str('prefix', prefix)

    value = __fox_trim_and_validate_hex_string(value, prefix)

    if len(value) == 0:
        return []

    o = []
    l = len(value)
    i = 0

    while i < l:
        o.append(__hex_to_byte(value[i], value[i+1]))
        i += 2

    return o


def fox_hex_to_int(value: str, prefix: str = '') -> int:
    """
    Hex to Int

    Converts the given hex string into an int value.  Hex string is considered
    big-endian.

    Arguments
    ---------
    value : str
        Hex string that will be parsed into an int value.
    prefix : str
        Prefix that will be stripped off the given value before it is parsed.

    Returns
    -------
    int
        The int value parsed from the given hex string.
    """

    fox_require_str('value', value)
    fox_require_str('prefix', prefix)

    value = __fox_trim_and_validate_hex_string(value, prefix)

    if len(value) == 0:
        raise Exception('cannot parse an int value from an empty hex string')

    o = 0
    l = len(value)
    i = 0

    while i < l:
        o = (o << 4) | __hex_to_seg(value[i])
        o = (o << 4) | __hex_to_seg(value[i+1])
        i += 2

    return o


def fox_hex_is_valid(hex: str) -> bool:
    """
    Tests if the given string is a valid hex string.  This assumes any prefixes
    have been removed before testing.

    :param hex: String to test.

    :returns: Whether the given value was a valid hex string.
    """
    if not isinstance(hex, str):
        return False

    for c in hex:
        if not __is_hex_digit(c):
            return False

    return True


################################################################################
##
##   Internal Functions
##
################################################################################


def __fox_trim_and_validate_hex_string(value: str, prefix: str = '') -> str:
    if len(prefix) > 0 and value.startswith(prefix):
        value = value[len(prefix):]

    for c in value:
        if not __is_hex_digit(c):
            raise Exception(f"character '{c}' is not a valid hex digit")

    if len(value) % 2 == 1:
        value = '0' + value

    return value



def __fox_bytes_to_hex(bytes: any, upper: bool = False) -> str:
    out = ""

    for byte in bytes:
        out += fox_ubyte_to_hex(byte, upper)

    if len(out) == 0:
        raise Exception('cannot build a hex string without at least one byte')

    return out


def __seg_to_hex(seg: int, upper: bool = False) -> str:
    if seg < 10:
        return chr(seg + 48)
    elif seg < 16:
        return chr((seg - 10) + (65 if upper else 97))
    else:
        raise Exception("illegal state")


def __hex_to_byte(seg1: str, seg2: str) -> int:
    return (__hex_to_seg(seg1) << 4) | __hex_to_seg(seg2)


def __hex_to_seg(hex: str) -> int:
    if '0' <= hex <= '9':
        return ord(hex) - 48
    elif 'A' <= hex <= 'F':
        return ord(hex) - 55
    elif 'a' <= hex <= 'f':
        return ord(hex) - 87
    else:
        raise Exception("invalid hex digit '{}'".format(hex))


def __is_hex_digit(digit: str) -> bool:
    c = ord(digit)
    return 48 <= c <= 57 or 65 <= c <= 70 or 97 <= c <= 102


################################################################################
##
##   Hex Function Unit Tests
##
################################################################################


def _fox_ubyte_to_hex_unit_test():
    tests = [ (0, '00'), (15, '0f'), (240, 'f0'), (255, 'ff') ]
    for test in tests:
        val = fox_ubyte_to_hex(test[0])
        if val != test[1]:
            raise Exception(f'bug in fox_ubyte_to_hex: expected {test[1]}, got {val}')

_fox_ubyte_to_hex_unit_test()


def _fox_ubytes_to_hex_unit_test():
    input = [ 0, 15, 240, 255 ]
    value = fox_ubytes_to_hex(input, '0x', True)

    if value != '0x000FF0FF':
        raise Exception(f'bug in fox_ubytes_to_hex: expected "0x000FF0FF", got {value}')

_fox_ubytes_to_hex_unit_test()


def _fox_int_to_hex_unit_test():
    val = fox_int_to_hex(255)
    if val != 'ff':
        raise Exception(f'bug in fox_int_to_hex: expected "ff", got {val}')

    val = fox_int_to_hex(255, 6, '#', True)
    if val != '#0000FF':
        raise Exception(f'bug in fox_int_to_hex: expected "#0000FF", got {val}')

    val = fox_int_to_hex(65535)
    if val != 'ffff':
        raise Exception(f'bug in fox_int_to_hex: expected "ffff", got {val}')

    val = fox_int_to_hex(4294967295)
    if val != 'ffffffff':
        raise Exception(f'bug in fox_int_to_hex: expected "ffffffff", got {val}')

_fox_int_to_hex_unit_test()


def _fox_hex_to_ubytes_unit_test():
    input = 'FFffFF'
    tests = [ 255, 255, 255 ]
    value = fox_hex_to_ubytes(input)
    if len(value) != len(tests):
        raise Exception(f'bug in fox_hex_to_ubytes: expected byte list length of {len(tests)}, got {len(value)}')
    for i in range(len(tests)):
        if value[i] != tests[i]:
            raise Exception(f'bug in fox_hex_to_ubytes: expected byte list entry {i} to be {tests[i]}, got {value[i]}')
    input = '#FFf00F00'
    tests = [ 255, 240, 15, 0 ]
    value = fox_hex_to_ubytes(input, '#')
    if len(value) != len(tests):
        raise Exception(f'bug in fox_hex_to_ubytes: expected byte list length of {len(tests)}, got {len(value)}')
    for i in range(len(tests)):
        if value[i] != tests[i]:
            raise Exception(f'bug in fox_hex_to_ubytes: expected byte list entry {i} to be {tests[i]}, got {value[i]}')

_fox_hex_to_ubytes_unit_test()


def _fox_hex_to_int_unit_test():
    input = '0xFFffFFff'
    value = fox_hex_to_int(input, '0x')
    if value != 4294967295:
        raise Exception(f'bug in fox_hex_to_int: expected 4294967295, got {value}')
    pass

_fox_hex_to_int_unit_test()


def _fox__hex_to_byte_unit_test():
    val = __hex_to_byte('f', 'f')
    if val != 255:
        raise Exception(f'bug in __hex_to_byte: expected 255, got {val}')
    val = __hex_to_byte('0', 'f')
    if val != 15:
        raise Exception(f'bug in __hex_to_byte: expected 15, got {val}')
    val = __hex_to_byte('0', '0')
    if val != 0:
        raise Exception(f'bug in __hex_to_byte: expected 0, got {val}')

_fox__hex_to_byte_unit_test()


def _fox__hex_to_seg_unit_test():
    tests = [
        ('f', 15), ('e', 14), ('d', 13), ('c', 12), ('b', 11), ('a', 10),
        ('9', 9), ('8', 8), ('7', 7), ('6', 6), ('5', 5), ('4', 4), ('3', 3),
        ('2', 2), ('1', 1), ('0', 0)
    ]

    for test in tests:
        val = __hex_to_seg(test[0])
        if val != test[1]:
            raise Exception(f'bug in __hex_to_seg: expected {test[1]}, got {val}')
        val = __hex_to_seg(test[0].upper())
        if val != test[1]:
            raise Exception(f'bug in __hex_to_seg: expected {test[1]}, got {val}')

_fox__hex_to_seg_unit_test()
