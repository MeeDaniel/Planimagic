import workspace_manager
from core import System
from graphics import App

system = System()


workspace_manager.workspace.init(system)


app = App(
    system,
    workspace_manager.workspace.update,
    workspace_manager.reload_workspace,
    title="Graphics Smart.",
    tps=120
)
app.start()
