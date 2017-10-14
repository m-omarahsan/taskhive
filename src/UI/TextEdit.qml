import QtQuick 2.7
import QtQuick.Controls 2.2


TextArea {
    id: control
    property string descriptionPlaceholder: description.text

    text: descriptionPlaceholder
    background: Rectangle {
        border.color: control.enabled ? "#3F3F3F" : "transparent"
    }
}
