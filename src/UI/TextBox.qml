import QtQuick 2.7
import QtQuick.Controls 2.2


TextArea {
    id: control
    wrapMode: TextEdit.WordWrap
    font.pixelSize: 22
    background: Rectangle {
        border.color: control.enabled ? "#3F3F3F" : "transparent"
    }

}
