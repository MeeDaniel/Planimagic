from typing import Union, Tuple, Sequence
from pygame import Color


RGBAOutput = Tuple[int, int, int, int]
ColorValue: Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]