from typing import Union, Tuple, List, Callable
import pygame_app as pa
import pygame

from core import System, Point, Segment
from .graphics_config import GraphicsConfig
from .exceptions import UnknownShapeType


class App(pa.App):
    def __init__(
            self,
            system: System,
            workspace_update_method: Callable,
            workspace_apply_changes_method: Callable,
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
        self.workspace_update_method = workspace_update_method
        self.workspace_apply_changes_method = workspace_apply_changes_method
        
        # === Graphics ===
        self.__transparent_surface = pygame.Surface(window, pygame.SRCALPHA)

        # === Logic ===
        self.__grabbed_point: Union[Point, None] = None
    
    def update(self) -> None:
        self.workspace_update_method(self.system)
        self.move_points()

    def draw(self) -> None:
        self.screen.fill(self.config.BACKGROUND_COLOR)
        self.__transparent_surface.fill((0, 0, 0, 0))

        self.draw_shapes()
        self.draw_points()
        
        self.screen.blit(self.__transparent_surface, (0, 0))

    # === Logic ===

    def move_points(self) -> None:
        mouse_rel = pygame.mouse.get_rel()

        cursor = pygame.SYSTEM_CURSOR_ARROW

        if self.__grabbed_point is None:
            for name, point in self.system.get_points().items():
                if self.is_point_hovered(point):
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
    
    def is_point_hovered(self, point: Point) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        return (mouse_pos[0] - point.get_pos()[0]) ** 2 + (mouse_pos[1] - point.get_pos()[1]) ** 2 \
                        <= self.config.POINT_OUTER_RADIUS ** 2

    # === Draw Rules ===

    def draw_points(self) -> None:
        points = self.system.get_points()
        for name, point in points.items():
            x, y = point.get_pos()
            outer_color = pygame.Color(point.color)
            outer_color.a = 64

            if point is self.__grabbed_point or self.__grabbed_point is None and self.is_point_hovered(point):
                self.draw_grabbed_point(point)
            else:
                self.draw_default_point(point)

    def draw_grabbed_point(self, point: Point) -> None:
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
            self.config.POINT_INNER_GRABBED_RADIUS
        )

    def draw_default_point(self, point: Point) -> None:
        pygame.draw.circle(
            self.__transparent_surface,
            point.color,
            point.get_pos(),
            self.config.POINT_INNER_DEFAULT_RADIUS
        )

    def draw_shapes(self) -> None:
        shapes = self.system.get_shapes()
        for name, shape in shapes.items():
            if isinstance(shape, Segment):
                self.draw_segment(shape)
            else:
                raise UnknownShapeType(name)
    
    def draw_segment(self, segment: Segment):
        color = pygame.Color(segment.color)
        color.a = 128
        from_, to = segment.get_key_points()
        pygame.draw.line(self.__transparent_surface, color, from_.get_pos(), to.get_pos())
