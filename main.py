import workspace_manager
from core import init
from custom_config import CustomConfig
from graphics import App

system = init()


workspace_manager.workspace.init(system)


app = App(
    system,
    workspace_manager.workspace.update,
    workspace_manager.reload_workspace,
    config=CustomConfig(),
    title="Planimagic."
)
app.start()
