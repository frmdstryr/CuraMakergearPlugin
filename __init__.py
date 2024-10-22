# Copyright (c) 2024 Jairus Martin
# Cura is released under the terms of the LGPLv3 or higher.
from cura.CuraApplication import CuraApplication
from cura.MachineAction import MachineAction
from .leveling_action import BedLevelMachineAction
from .filament_action import FilamentLoadingAction
from . import usb_log

def getMetaData():
    return {}


def add_supported_action(app: CuraApplication, definition_id: str, action: MachineAction):
    # Cannot use mgr.addSupportedAction since it may not be added until later..
    mgr = app.getMachineActionManager()
    if definition_id not in mgr._supported_actions:
        mgr._supported_actions[definition_id] = []
    actions = mgr._supported_actions[definition_id]
    if action.getKey() not in actions:
        actions.append(action)


def register(app: CuraApplication):
    usb_log.install()
    mgr = app.getMachineActionManager()
    machine_actions = [
        BedLevelMachineAction(),
        FilamentLoadingAction()
    ]
    for action in machine_actions:
        add_supported_action(app, "makergear_m2", action)
    return {"machine_action": machine_actions}
