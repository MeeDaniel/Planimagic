import importlib

import workspace  # noqa: F401
from core import System
from graphics import App


def reload_workspace(system: System, app: "App"):
    importlib.import_module("workspace").apply_immediately(system, app)
