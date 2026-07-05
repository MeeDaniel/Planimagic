from dataclasses import dataclass


@dataclass
class GraphicsConfig:
    # === Sizes ===
    POINT_INNER_DEFAULT_RADIUS = 7
    POINT_INNER_GRABBED_RADIUS = 5
    POINT_OUTER_RADIUS = 13

    # === Colors ===
    BACKGROUND_COLOR = "#171717"
