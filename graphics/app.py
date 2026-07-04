from typing import Union, Tuple, List, Callable
import pygame_app as pa
import pygame

from core import System
from .graphics_config import GraphicsConfig


class App(pa.App):
    def __init__(
            self,
            system: System,
            reload_system_method: Callable,
            config: GraphicsConfig = GraphicsConfig(),
            window: Union[Tuple[int, int], List[int]]=(1280, 720),
            tps:int=60,
            title: Union[str, None] = None,
            window_flags: int = 0
    ):
        super().__init__(window, tps, title, window_flags | pygame.SRCALPHA)
        self.system = system
        self.config = config
        self.reload_system_method = reload_system_method
    
    def update(self) -> None:
        self.reload_system_method()
    
    def draw(self) -> None:
        points = self.system.get_points()
        for name, point in points.items():
            x, y = point.get_pos()
            outer_color = pygame.Color(point.color)
            outer_color.a = 128

            pygame.draw.circle(
                self.screen,
                outer_color,
                (x, y),
                self.config.POINT_OUTER_RADIUS
            )

            pygame.draw.circle(
                self.screen,
                point.color,
                (x, y),
                self.config.POINT_INNER_RADIUS
            )
