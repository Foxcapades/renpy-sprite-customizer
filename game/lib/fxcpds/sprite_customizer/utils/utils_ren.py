"""renpy
init -1 python:
"""


def _sc_validator_hex_color_char(c: str) -> bool:
    """
    Tests whether the given character is a valid hex digit.

    Arguments
    ---------
    c : str
        Character to test.

    Returns
    -------
    bool
        Whether the given character was a valid hex digit.
    """
    return '0' <= c <= '9' or 'a' <= c <= 'f' or 'A' <= c <= 'F'


def sc_validator_hex_color(text: str) -> bool:
    """
    Hex color string validator for use with SCValidatableTextOption instances.
    Verifies that the given input string resembles a valid hex color code.

    Arguments
    ---------
    text : str
        String to test.

    Returns
    -------
    bool
        Whether the given value was a valid hex color string.
    """
    if not isinstance(text, str):
        return False

    l = len(text)

    if not (l == 4 or l == 7 or l == 9):
        return False

    if not text.startswith("#"):
        return False

    for i in range(1, l):
        if not _sc_validator_hex_color_char(text[i]):
            return False

    return True
