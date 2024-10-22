
# Copyright (c) 2018 Ultimaker B.V.
# Copyright (c) 2024 Jairus Martin
# Cura is released under the terms of the LGPLv3 or higher.

from enum import Enum
from typing import Optional, List

from cura.MachineAction import MachineAction
from cura.PrinterOutput.PrinterOutputDevice import PrinterOutputDevice
from cura.PrinterOutput.Models.PrinterOutputModel import PrinterOutputModel

from UM.FlameProfiler import pyqtSlot

from UM.Application import Application
from UM.i18n import i18nCatalog
from UM.Logger import Logger
catalog = i18nCatalog("cura")


class FilamentLoadingAction(MachineAction):
    """A simple action to handle manual bed leveling procedure for
    printers that don't have it on the firmware.
    """

    def __init__(self):
        super().__init__("FilamentLoading", catalog.i18nc("@action", "Load / unload filament"))
        self._qml_url = "filament_action.qml"

    def _execute(self):
        pass

    @property
    def app(self):
        return Application.getInstance()

    @pyqtSlot()
    def load_filament(self):
        dev = self.get_device()
        if not dev:
            Logger.log("e", "Can't load filament. The printer connection seems to have been lost.")
            return
        dev.sendCommand("M701")

    @pyqtSlot()
    def unload_filament(self):
        dev = self.get_device()
        if not dev:
            Logger.log("e", "Can't unload filament. The printer connection seems to have been lost.")
            return
        dev.sendCommand("M702")

    def get_device(self) -> Optional[PrinterOutputDevice]:
        # TODO: How can USBPrinterOutputDevice be imported from a plugin?
        for dev in self.app.getOutputDeviceManager().getOutputDevices():
            if (
                isinstance(dev, PrinterOutputDevice)
                and "USBPrinterOutputDevice" in str(type(dev))
            ):
                return dev

