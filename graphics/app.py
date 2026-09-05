from collections.abc import Callable

import pygame
import pygame_app as pa

from core import Line, Point, Segment, System

from .camera import Camera
from .exceptions import UnknownShapeType
from .graphics_config import GraphicsConfig


class App(pa.App):
    def __init__(
            self,
            system: System,
            workspace_update_method: Callable[[System, "App"], None],
            workspace_apply_changes_method: Callable[[System, "App"], None],
            config: GraphicsConfig = GraphicsConfig(),  # noqa: B008
            window: tuple[int, int] | list[int]=(1280, 720),
            title: str | None = None,
            window_flags: int = 0
    ):
        # === Settings ===
        super().__init__(window, config.TPS, title, window_flags | pygame.SRCALPHA)
        self.system = system
        self.config = config
        self.workspace_update_method = workspace_update_method
        self.workspace_apply_changes_method = workspace_apply_changes_method
        self.camera = Camera(0, 0, 100)
        
        # === Graphics ===
        pygame.init()
        self.__transparent_surface = pygame.Surface(window, pygame.SRCALPHA)
        self.__label_font = pygame.font.SysFont(self.config.LABEL_FONTNAME, self.config.LABEL_FONTSIZE)

        # === Logic ===
        self.__grabbed_point: Point | None = None
    
    def update(self) -> None:
        self.drag_points()
        self.system.update()
        self.camera_zoom()
        self.workspace_update_method(self.system, self)

    def draw(self) -> None:
        self.screen.fill(self.config.BACKGROUND_COLOR)
        self.__transparent_surface.fill((0, 0, 0, 0))

        self.draw_shapes()
        self.draw_points()
        
        self.screen.blit(self.__transparent_surface, (0, 0))

    # === Logic ===

    def drag_points(self) -> None:
        mouse_rel = pygame.mouse.get_rel()

        cursor = pygame.SYSTEM_CURSOR_ARROW

        if self.__grabbed_point is None:
            for point in self.system.get_points().values():
                if self.is_point_hovered(point):
                    cursor = pygame.SYSTEM_CURSOR_HAND
                    if self.mouse.is_pressed[0]:
                        self.__grabbed_point = point
                    break

            # WARN: Three lines below implements logic absolutely unrelated to point dragging. It should be moved to
            #       other method or the logic of this method should be completely refactored.
            if self.mouse.is_pressed[0]:
                self.camera.x -= mouse_rel[0] / self.camera.scale
                self.camera.y -= mouse_rel[1] / self.camera.scale
        else:
            if self.mouse.is_pressed[0]:
                cursor = pygame.SYSTEM_CURSOR_HAND
                gx, gy = self.__grabbed_point.get_pos()
                self.__grabbed_point.set_pos(
                    gx + mouse_rel[0] / self.camera.scale,
                    gy + mouse_rel[1] / self.camera.scale)
            else:
                self.__grabbed_point = None
        
        pygame.mouse.set_cursor(cursor)

    def camera_zoom(self) -> None:
        scale = 1.5 if self.key.pressed[pygame.K_LSHIFT] else 1.2

        for event in self.events:
            if event.type == pygame.MOUSEWHEEL:
                self.camera.scale *= scale ** event.y
    
    def is_point_hovered(self, point: Point) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        x, y = self.camera.unit2display(*point.get_pos(), self.screen.get_width(), self.screen.get_height())
        return (mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2 \
                        <= self.config.POINT_OUTER_RADIUS ** 2

    # === Draw Rules ===

    def draw_points(self) -> None:
        points = self.system.get_points()
        for point in points.values():
            _x, _y = point.get_pos()
            outer_color = pygame.Color(point.color)
            outer_color.a = 64

            if point is self.__grabbed_point or self.__grabbed_point is None and self.is_point_hovered(point):
                self.draw_grabbed_point(point)
            else:
                self.draw_default_point(point)

    def draw_grabbed_point(self, point: Point) -> None:
        x, y = point.get_pos()
        screen_x, screen_y = self.camera.unit2display(x, y, self.screen.get_width(), self.screen.get_height())

        color = pygame.Color(point.color)
        if not point.is_active():
            color.a //= 4

        outer_color = pygame.Color(color)
        outer_color.a //= 4

        pygame.draw.circle(
            self.__transparent_surface,
            outer_color,
            (screen_x, screen_y),
            self.config.POINT_OUTER_RADIUS
        )
        pygame.draw.circle(
            self.__transparent_surface,
            color,
            (screen_x, screen_y),
            self.config.POINT_INNER_GRABBED_RADIUS
        )

        label_surface = self.__label_font.render(point.get_label(), self.config.LABEL_ANTIALIAS, color)

        # TODO: make better alignment
        label_rect = label_surface.get_rect(centerx=screen_x, bottom=screen_y-self.config.POINT_LABEL_OFFSET)

        self.__transparent_surface.blit(label_surface, label_rect)

    def draw_default_point(self, point: Point) -> None:
        x, y = point.get_pos()
        screen_x, screen_y = self.camera.unit2display(x, y, self.screen.get_width(), self.screen.get_height())

        color = pygame.Color(point.color)
        if not point.is_active():
            color.a //= 4

        pygame.draw.circle(
            self.__transparent_surface,
            color,
            (screen_x, screen_y),
            self.config.POINT_INNER_DEFAULT_RADIUS
        )

        label_surface = self.__label_font.render(point.get_label(), self.config.LABEL_ANTIALIAS, color)

        # TODO: make better alignment
        label_rect = label_surface.get_rect(centerx=screen_x, bottom=screen_y-self.config.POINT_LABEL_OFFSET)

        self.__transparent_surface.blit(label_surface, label_rect)

    def draw_shapes(self) -> None:
        shapes = self.system.get_shapes()
        for name, shape in shapes.items():
            if isinstance(shape, Segment):
                self.draw_segment(shape)
            elif isinstance(shape, Line):
                self.draw_line(shape)
            else:
                raise UnknownShapeType(name)
    
    def draw_segment(self, segment: Segment):
        color = pygame.Color(segment.color)
        color.a = 128

        if not segment.is_active():
            color.a //= 4

        from_, to = segment.get_key_points()
        pygame.draw.line(
            self.__transparent_surface,
            color,
            self.camera.unit2display(*from_.get_pos(), self.screen.get_width(), self.screen.get_height()),
            self.camera.unit2display(*to.get_pos(), self.screen.get_width(), self.screen.get_height())
        )

    def draw_line(self, line: Line):
        color = pygame.Color(line.color)
        color.a = 128

        if not line.is_active():
            color.a //= 4
        
        from_, to = line.get_key_points()
        from_x, from_y = from_.get_pos()
        to_x, to_y = to.get_pos()

        screen_width, screen_height = self.__transparent_surface.get_size()
        screen_left_bound, screen_top_bound = self.camera.display2unit(0, 0, screen_width, screen_height)
        screen_right_bound, screen_bottom_bound = self.camera.display2unit(
                                                               screen_width, screen_height, screen_width, screen_height)

        # Task: find BEGIN=(begin_x, begin_y) and END=(end_x, end_y) points to draw the line. These points shall lay on edges of the screen
        #
        # My solution:
        # Firstly note, that the screen has four edges: left bound, top bound, right bound, and bottom bound. Each of
        # these bounds can be represented as segments or a lines. Let call these lines left line, top line, right line,
        # and bottom line respectively. Given line either parallel to some of these lines or intersect all of them.
        # 
        # The first case is very simple, it is described in the code below (two edge cases).
        # 
        # The second case is a bit harder. Let define intersection points of the given line with the left, top, right,
        # and bottom lines as (left_x, left_y), (top_x, top_y), (right_x, right_y), and (bottom_x, bottom_y). Obviously,
        #
        # left_x = screen_left_bound
        # top_y = screen_top_bound
        # right_x = screen_right_bound
        # bottom_y = screen_bottom_bound
        #
        # To find left_y let consider the given line in the parametric form:
        #
        # P_x = from_x + (to_x - from_x) * t
        # P_y = from_y + (to_y - from_y) * t
        # Where P = (P_x, P_y) ∈ the given line
        #
        # P_x = left_x ⟺ t = (left_x - from_x) / (to_x - from_x) ⟺
        # P_y = from_y + (to_y - from_y) * (left_x - from_x) / (to_x - from_x) ⟺
        # left_y = from_y + (to_y - from_y) * (left_x - from_x) / (to_x - from_x) ⟺
        # left_y = from_y + (to_y - from_y) * (screen_left_bound - from_x) / (to_x - from_x)
        #
        # Similarly,
        # right_y = from_y + (to_y - from_y) * (screen_right_bound - from_x) / (to_x - from_x)
        # top_x = from_x + (to_x - from_x) * (screen_top_bound - from_y) / (to_y - from_y)
        # bottom_x = from_x + (to_x - from_x) * (screen_bottom_bound - from_y) / (to_y - from_y)
        #
        # If intersection point with left line is out of the screen, then our BEGIN point is on the top or bottom line.
        # Likewise for the right line

        begin_x, begin_y = None, None
        end_x, end_y = None, None

        if (from_y == to_y): # Edge case: line is horizontal
            begin_x, begin_y = screen_left_bound, from_y
            end_x, end_y = screen_right_bound, to_y
        elif (from_x == to_x): # Edge case: line is vertical
            begin_x, begin_y = from_x, screen_top_bound
            end_x, end_y = to_x, screen_bottom_bound
        else:
            left_y = from_y + (to_y - from_y) * (screen_left_bound - from_x) / (to_x - from_x)
            right_y = from_y + (to_y - from_y) * (screen_right_bound - from_x) / (to_x - from_x)

            if (left_y < screen_top_bound and right_y < screen_top_bound) or \
                    (left_y > screen_bottom_bound and right_y > screen_bottom_bound):
                return # No need to draw

            if screen_top_bound <= left_y <= screen_bottom_bound:
                begin_x = screen_left_bound
                begin_y = left_y
            elif left_y < screen_top_bound:
                top_x = from_x + (to_x - from_x) * (screen_top_bound - from_y) / (to_y - from_y)
                begin_x = top_x
                begin_y = screen_top_bound
            else:
                bottom_x = from_x + (to_x - from_x) * (screen_bottom_bound - from_y) / (to_y - from_y)
                begin_x = bottom_x
                begin_y = screen_bottom_bound
            
            if screen_top_bound <= right_y <= screen_bottom_bound:
                end_x = screen_right_bound
                end_y = right_y
            elif right_y < screen_top_bound:
                top_x = from_x + (to_x - from_x) * (screen_top_bound - from_y) / (to_y - from_y)
                end_x = top_x
                end_y = screen_top_bound
            else:
                bottom_x = from_x + (to_x - from_x) * (screen_bottom_bound - from_y) / (to_y - from_y)
                end_x = bottom_x
                end_y = screen_bottom_bound
        
        pygame.draw.line(
            self.__transparent_surface,
            color,
            self.camera.unit2display(begin_x, begin_y, self.screen.get_width(), self.screen.get_height()),
            self.camera.unit2display(end_x, end_y, self.screen.get_width(), self.screen.get_height())
        )
