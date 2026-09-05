from dataclasses import dataclass


@dataclass
class GraphicsConfig:
    # === General ===
    TPS = 60
    
    # === Sizes ===
    POINT_INNER_DEFAULT_RADIUS = 7
    POINT_INNER_GRABBED_RADIUS = 5
    POINT_OUTER_RADIUS = 13
    POINT_LABEL_OFFSET = 16

    # === Colors ===
    BACKGROUND_COLOR = "#171717"

    # === Fonts ===
    LABEL_FONTNAME = "Fira Code"
    LABEL_FONTSIZE = 24
    LABEL_ANTIALIAS = True # Affects perfomance. Turn off if you have many objects in your system and it is laggy
