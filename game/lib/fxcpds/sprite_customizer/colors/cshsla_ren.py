from .cshsl_ren import CSHSL
from .csrgba_ren import CSRGBA

"""renpy
init python:
"""

class CSHSLA(CSHSL):
    def __init__(self, hue, saturation, lightness, alpha):
        super().__init__(hue, saturation, lightness)
        CSHSL._validate_percent('alpha', alpha)
        self._a = alpha

    ############################################################################
    #
    #   Properties
    #
    ############################################################################

    @property
    def alpha(self) -> float:
        return self._a

    ############################################################################
    #
    #   Public Methods
    #
    ############################################################################

    def set_alpha(self, alpha: float):
        CSHSL._validate_percent('alpha', alpha)
        self._a = alpha

    def to_hsl(self):
        return CSHSL(self._h, self._s, self._l)

    def to_rgba(self):
        tmp = self._to_rgb()
        return CSRGBA(tmp[0], tmp[1], tmp[2], int(self._a * 255))
