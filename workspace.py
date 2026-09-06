from core import (
    CrossPointRule,
    HeightRule,
    Line,
    LockOnLineRule,
    Point,
    RatioRule,
    Segment,
    System,
)
from graphics import App


def init(system: System):
    """This function calls immediately program starts
    """

    A = Point(-1,     name="A", color="#eadb3a")
    B = Point( 1, -3, name="B", color="#ffffff")
    C = Point(        name="C", color="#6cec59")
    D = Point( 2,  2, name="D", color="#ffffff")
    E = Point( 1,  1, name="E", color="#ff0000")
    F = Point(-3,  3, name="F", color="#eadb3a")
    G = Point( 3,  3, name="G", color="#eadb3a")
    H = Point(        name="H", color="#ff8000")
    I = Point(        name="I", color="#0b5bbd")

    yline =  Line(F, G, name="yline", color="#eadb3a")
    seg = Segment(A, B, name="seg")
    line =   Line(C, D, name="line",  color="#ffffff")

    LockOnLineRule(None, A, yline)
    RatioRule(None, seg, 1/3, C)
    HeightRule(None, E, line, H)
    CrossPointRule(None, yline, line, I)

def update(system: System, app: App):
    """This function calls every program tick
    """

def apply_immediately(system: System, app: App):
    """This function calls when user call it during the program run
    """
