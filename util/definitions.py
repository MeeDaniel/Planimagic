from collections.abc import Sequence
from typing import Union

from pygame import Color

RGBAOutput = tuple[int, int, int, int]
ColorValue = Union[Color, int, str, tuple[int, int, int], RGBAOutput, Sequence[int]] # Copied from pygame._common  # noqa: UP007
