import QtQuick 2.0

Item {
    id: lineEditItem
    property int fontSize: 18
    property bool editable: input1.editable
    property alias text: input1.text
    signal accepted()
    Rectangle {
            anchors.fill: parent
            anchors.bottomMargin: 1
            color: "#DBDBDB"
        }

        Rectangle {
            anchors.fill: parent
            anchors.topMargin: 1
            color: "#FFF"
        }
        Input {
            id: input1
            anchors.fill: parent
            anchors.leftMargin: 4
            anchors.rightMargin: 3
            font.pixelSize: parent.fontSize
            onAccepted: lineEditItem.accepted()
        }

}
