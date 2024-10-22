# Cura Makergear M2 Plugin

A Cura plugin that adds machine actions to do bed leveling and
filament loading/unloading for the Makergear M2.

It also patches the serial port to add logging (disable by commenting out the `usb_log.install()` line).

## Local Installation

Either download or clone the repo into `.local/share/cura/<version>/plugins/` or
download/clone it and create a symlink into that folder.

Then restart cura.

Example:
```
ln -s /home/user/projects/CuraMakergearPlugin/ /home/user/.local/share/cura/5.6/plugins/CuraMakergearPlugin
```

# Usage

The machine actions can be found by connecting the printer and
