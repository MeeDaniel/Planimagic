import time

from core import (
    HeightRule,
    Line,
    LockOnLineRule,
    Point,
    RatioRule,
    Segment,
    System,
)
from graphics import App

t = time.time()


def init(system: System):
    """This function calls immediately program starts
    """

    A = Point(1-4, 1-4, name="A", color="#eadb3a")
    B = Point(5-4, 1-4, name="B", color="#ffffff")
    C = Point(0-4, 0-4, name="C", color="#6cec59")
    D = Point(6-4, 6-4, name="D", color="#ffffff")
    E = Point(5-4, 5-4, name="E", color="#ff0000")
    F = Point( -3,   3, name="F", color="#eadb3a")
    G = Point(  3,   3, name="G", color="#eadb3a")
    H = Point(5-4, 5-4, name="H", color="#ff8000")

    yline = Line(F, G, name="yline", color="#eadb3a")
    seg = Segment(A, B, name="seg")
    line = Line(C, D, name="line", color="#ffffff")

    A_lock_on_yline = LockOnLineRule("A_lock_on_line", A, yline)
    one_third_rule = RatioRule("one_third", seg, 1/3, C)
    height_rule = HeightRule("height", E, line, H)

    system.add_point(A)
    system.add_point(B)
    system.add_point(C)
    system.add_point(D)
    system.add_point(E)
    system.add_point(F)
    system.add_point(G)
    system.add_point(H)

    system.add_shape(seg)
    system.add_shape(line)
    system.add_shape(yline)

    system.add_rule(one_third_rule)
    system.add_rule(height_rule)
    system.add_rule(A_lock_on_yline)

def update(system: System, app: App):
    """This function calls every program tick
    """
    global t
    current_time = time.time()
    diff = current_time - t
    tps = 1 / diff
    print(f"{diff=:.6f} {tps=:.2f}")
    t = current_time

def apply_immediately(system: System, app: App):
    """This function calls when user call it during the program run
    """
