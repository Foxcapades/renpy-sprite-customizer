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

# From https://github.com/Foxcapades/renpy-util-requirement

"""renpy
init -25 python:
"""


def fox_enforce_int(name: str, value: int | float) -> int:
    """
    Enforce Int

    Enforces that the given numeric value is an int.  If the value is a float it
    will be converted to an int and returned.  If it is already an int it will
    be returned directly.  If it is anything else an exception will be raised.

    Arguments
    ---------
    name : str
        Name of the value being tested.  This name is used in the exception if
        it is raised.
    value : int | float
        Value that must be or will be converted to an int.

    Returns
    -------
    int
        The input value if it was an int, or the value converted to an int if it
        was a float.
    """
    if isinstance(value, int):
        return value
    elif isinstance(value, float):
        return int(value)
    else:
        raise Exception(f'"{name}" must be a numeric value')


def fox_require_int(name: str, value: int) -> int:
    """
    Require Int

    Requires that the given value is an int.  If it is anything else an
    exception will be raised.

    Arguments
    ---------
    name : str
        Name of the value being tested.  This name is used in the exception if
        it is raised.
    value : int
        Value that must be an int.

    Returns
    -------
    int
        The input value if it was an int.
    """
    if isinstance(value, int):
        return value
    else:
        raise Exception(f'"{name}" must be an int value')


def fox_require_float(name: str, value: float) -> float:
    """
    Require Float

    Requires that the given value is an float.  If it is anything else an
    exception will be raised.

    Arguments
    ---------
    name : str
        Name of the value being tested.  This name is used in the exception if
        it is raised.
    value : float
        Value that must be an float.

    Returns
    -------
    float
        The input value if it was an float.
    """
    if isinstance(value, float):
        return value
    else:
        raise Exception(f'"{name}" must be a float value')


def fox_require_bool(name: str, value: bool) -> bool:
    """
    Require Boolean

    Requires that the given value is a bool.  If it is anything else an
    exception will be raised.

    Arguments
    ---------
    name : str
        Name of the value being tested.  This name is used in the exception if
        it is raised.
    value : bool
        Value that must be a bool.

    Returns
    -------
    bool
        The input value if it was a bool.
    """
    if isinstance(value, bool):
        return value
    else:
        raise Exception(f'"{name}" must be a boolean value')


def fox_require_str(name: str, value: str) -> str:
    """
    Require String

    Requires that the given value is a string.  If it is anything else an
    exception will be raised.

    Arguments
    ---------
    name : str
        Name of the value being tested.  This name is used in the exception if
        it is raised.
    value : str
        Value that must be a string.

    Returns
    -------
    str
        The input value if it was a string.
    """
    if isinstance(value, str):
        return value
    else:
        raise Exception(f'"{name}" must be a string value')
