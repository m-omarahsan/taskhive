import QtQuick 2.0
import QtQuick.Controls 1.4
LineEdit {
    id: item2
    property bool editable: item2.editable
    Calendar {
        id: calendar
        frameVisible: false
        anchors.top: parent.bottom
        anchors.left: parent.left
        onClicked: {
            item2.text = date
        }
    }
    MouseArea {
        anchors.fill: parent
        onClicked: {
            calendar.frameVisible = true
        }
    }
}
