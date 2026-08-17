import importlib

import workspace  # noqa: F401
from core import System


def reload_workspace(system: System):
    importlib.import_module("workspace").apply_immediately(system)
