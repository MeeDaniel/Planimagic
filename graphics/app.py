from typing import Union, Tuple, List, Callable
import pygame_app as pa
import pygame

from core import System, Point
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
        # === Settings ===
        super().__init__(window, tps, title, window_flags | pygame.SRCALPHA)
        self.system = system
        self.config = config
        self.reload_system_method = reload_system_method
        
        # === Graphics ===
        self.__transparent_surface = pygame.Surface(window, pygame.SRCALPHA)

        # === Logic ===
        self.__grabbed_point: Union[Point, None] = None
    
    def update(self) -> None:
        self.reload_system_method()
        self.move_points()

    def draw(self) -> None:
        self.screen.fill(self.config.BACKGROUND_COLOR)
        self.__transparent_surface.fill((0, 0, 0, 0))

        points = self.system.get_points()
        for name, point in points.items():
            x, y = point.get_pos()
            outer_color = pygame.Color(point.color)
            outer_color.a = 64

            pygame.draw.circle(
                self.__transparent_surface,
                outer_color,
                (x, y),
                self.config.POINT_OUTER_RADIUS
            )

            pygame.draw.circle(
                self.__transparent_surface,
                point.color,
                (x, y),
                self.config.POINT_INNER_RADIUS
            )
        
        self.screen.blit(self.__transparent_surface, (0, 0))

    def move_points(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        mouse_rel = pygame.mouse.get_rel()

        cursor = pygame.SYSTEM_CURSOR_ARROW

        if self.__grabbed_point is None:
            for name, point in self.system.get_points().items():
                if (mouse_pos[0] - point.get_pos()[0]) ** 2 + (mouse_pos[1] - point.get_pos()[1]) ** 2 \
                        <= self.config.POINT_OUTER_RADIUS ** 2:
                    cursor = pygame.SYSTEM_CURSOR_HAND
                    if self.mouse.is_pressed[0]:
                        self.__grabbed_point = point
                    break
        else:
            if self.mouse.is_pressed[0]:
                cursor = pygame.SYSTEM_CURSOR_HAND
                self.__grabbed_point.set_pos(
                    self.__grabbed_point.get_pos()[0] + mouse_rel[0],
                    self.__grabbed_point.get_pos()[1] + mouse_rel[1]
                )
            else:
                self.__grabbed_point = None
        
        pygame.mouse.set_cursor(cursor)
