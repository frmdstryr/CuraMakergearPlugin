// Copyright (c) 2024 Jairus Martin
// Cura is released under the terms of the LGPLv3 or higher.

import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3

import UM 1.5 as UM
import Cura 1.1 as Cura


Cura.MachineAction
{
    UM.I18nCatalog { id: catalog; name: "cura"; }

    anchors.fill: parent

    Item
    {
        id: bedLevelMachineAction
        anchors.top: parent.top
        anchors.topMargin: UM.Theme.getSize("default_margin").height * 3
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.width * 3 / 4

        UM.Label
        {
            id: pageTitle
            width: parent.width
            text: catalog.i18nc("@title", "Load / unload filament")
            wrapMode: Text.WordWrap
            font: UM.Theme.getFont("medium")
        }


        Row
        {
            id: bedlevelingWrapper
            anchors.top: bedlevelingText.bottom
            anchors.topMargin: UM.Theme.getSize("default_margin").height * 3
            anchors.horizontalCenter: parent.horizontalCenter
            width: childrenRect.width
            spacing: UM.Theme.getSize("default_margin").width

            Cura.ActionButton
            {
                id: loadFilamentButton
                text: catalog.i18nc("@action:button", "Load filament")
                onClicked:
                {
                    manager.load_filament()
                }
            }

            Cura.ActionButton
            {
                id: unloadFilamentButton
                text: catalog.i18nc("@action:button", "Unload filament")
                onClicked:
                {
                    manager.unload_filament()
                }
            }
        }
    }
}
