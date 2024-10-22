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

class State(Enum):
    RESET = 0
    XMIN_YMIN = 1
    XMAX_YMIN = 2
    XMIN_YMAX = 3
    XMAX_YMAX = 4

class BedLevelMachineAction(MachineAction):
    """A simple action to handle manual bed leveling procedure for
    printers that don't have it on the firmware.
    """

    def __init__(self):
        super().__init__("MakergearBedLeveling", catalog.i18nc("@action", "Level build plate"))
        self._qml_url = "leveling_action.qml"
        self.state = State.RESET

    def _execute(self):
        pass

    def _reset(self):
        self.state = State.RESET

    @property
    def app(self):
        return Application.getInstance()

    @pyqtSlot()
    def startBedLeveling(self):
        self.state = State.RESET

        dev = self.getPrinter()
        if not dev:
            Logger.log("e", "Can't start bed levelling. The printer connection seems to have been lost.")
            return
        dev.sendCommand("G90") # Set abs
        dev.sendCommand("G20") # Set units mm
        dev.sendCommand("G28") # Home all
        dev.sendCommand("G0 X0 Y0 Z10")

    def getPrinter(self) -> Optional[PrinterOutputDevice]:
        # TODO: How can USBPrinterOutputDevice be imported from a plugin?
        for dev in self.app.getOutputDeviceManager().getOutputDevices():
            if (
                isinstance(dev, PrinterOutputDevice)
                and "USBPrinterOutputDevice" in str(type(dev))
            ):
                return dev

    @pyqtSlot()
    def moveToNextLevelPosition(self):
        dev = self.getPrinter()
        if not dev: #No output devices. Can't move.
            Logger.log("e", "Can't move to the next position. The printer connection seems to have been lost.")
            return
        Logger.log("d", f"Bed leveling state: {self.state}")
        settings = self.app.getGlobalContainerStack()
        machine_width = settings.getProperty("machine_width", "value")
        machine_depth = settings.getProperty("machine_depth", "value")
        edge_offset = 10
        xmin = edge_offset
        ymin = edge_offset
        xmax = machine_width - edge_offset
        ymax = machine_depth - edge_offset
        safe_z = 10
        if self.state == State.RESET:
            # Goto xmin, ymin
            dev.sendCommand(f"G0 Z{safe_z}") # Lift
            dev.sendCommand(f"G0 X{xmin} Y{ymin} Z{safe_z}") # Goto next corner
            dev.sendCommand("G0 Z0") # Drop
            self.state = State.XMIN_YMIN
        elif self.state == State.XMIN_YMIN:
            dev.sendCommand(f"G0 Z{safe_z}") # Lift
            dev.sendCommand(f"G0 X{xmax} Y{ymin} Z{safe_z}") # Goto next corner
            dev.sendCommand("G0 Z0") # Drop
            self.state = State.XMAX_YMIN
        elif self.state == State.XMAX_YMIN:
            dev.sendCommand(f"G0 Z{safe_z}") # Lift
            dev.sendCommand(f"G0 X{xmin} Y{ymax} Z{safe_z}") # Goto next corner
            dev.sendCommand("G0 Z0") # Drop
            self.state = State.XMIN_YMAX
        elif self.state == State.XMIN_YMAX:
            dev.sendCommand(f"G0 Z{safe_z}") # Lift
            dev.sendCommand(f"G0 X{xmax} Y{ymax} Z{safe_z}") # Goto next corner
            dev.sendCommand("G0 Z0") # Drop
            self.state = State.XMAX_YMAX
        elif self.state == State.XMAX_YMAX:
            dev.sendCommand(f"G0 Z{safe_z}") # Lift
            dev.sendCommand(f"G0 X0 Y0 {safe_z}")
            self.state == State.RESET
            self.setFinished()
