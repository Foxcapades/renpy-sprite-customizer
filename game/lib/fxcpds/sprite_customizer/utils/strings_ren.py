"""renpy
init -1 python:
"""


def _require_key_string(name: str, value: any) -> str:
    value = _require_non_empty_string(name, value)

    if not __is_word_char(value[0]):
        raise Exception(f'"{name}" must begin with a letter or an underscore')

    for i in range(1, len(value)):
        if not __is_key_safe_char(value[i]):
            raise Exception(f'"{name}" contains an illegal character at position {i}')

    return value


def _require_non_empty_string(name: str, value: any) -> str:
    value = _require_string(name, value).strip()

    if len(value) < 1:
        raise Exception(f'"{name}" must not be blank')

    return value


def _require_string(name: str, value: any) -> str:
    if not isinstance(value, str):
        raise Exception(f'"{name}" must be a string value')

    return value


def __is_key_safe_char(c: str) -> bool:
    return __is_word_char(c) or __is_dec_digit(c)


def __is_word_char(c: str) -> bool:
    o = ord(c)
    return 65 <= o <= 90 or o == 95 or 97 <= o <= 122


def __is_dec_digit(c: str) -> bool:
    return 48 <= ord(c) <= 57
