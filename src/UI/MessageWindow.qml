import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 1.4
Window {
    id: messageWindow
    width: 400
    height: 600
    color: "#3D3D3D"
    property ListModel messages: ListModel {}
    ScrollView {
        anchors.top: parent.top
        anchors.bottom: rectRow.top
        anchors.right: parent.right
        anchors.left: parent.left
        frameVisible: false
        horizontalScrollBarPolicy: Qt.ScrollBarAlwaysOff
        verticalScrollBarPolicy: Qt.ScrollBarAlwaysOff
        ListView {
            anchors.fill: parent
            anchors.topMargin: 10
            delegate: message
            spacing: 10
            model: messageWindow.messages
        }

    }
    Component {
        id: message
        Column{
            anchors.right: parent.right
            anchors.left: parent.left
            readonly property bool sentByMe: modelData.sender !== "You"
            spacing: 10
            Text {
                text: sender
                font.pixelSize: 18
                color: "#fff"
                anchors.left: sentByMe ? parent.left: undefined
                anchors.leftMargin: 20
                anchors.right: !sentByMe ? parent.right: undefined
                anchors.rightMargin: 20

            }
            Rectangle {
                anchors.right: parent.right
                anchors.left: parent.left
                height: childrenRect.height

                radius: 4
                anchors.rightMargin: 20
                anchors.leftMargin: 20
                Text {
                    text: messageText
                    anchors.right: parent.right
                    anchors.rightMargin: 10
                    anchors.leftMargin: 10
                    anchors.left: parent.left
                    font.pixelSize: 18
                    wrapMode: Text.WordWrap
                }
            }
        }
    }
    Row {
        id: rectRow
        anchors.right: parent.right
        anchors.left: parent.left
        anchors.bottomMargin: 20
        anchors.bottom: parent.bottom
        anchors.leftMargin: 20
        anchors.rightMargin: 20
        spacing: 10
        TextBox {
            id: messageText
            height: 150
            width: rectRow.width - 50

        }
        Button {
            height: 40
            width: 40
            text: "Send"
            onClicked: {
                messageWindow.messages.append({"messageText": messageText.text, "sender": "You"})
                messageInfo = {
                    "bit_address": taskWindow.selectedTask.task_address,
                    "task_id": taskWindow.selectedTask.task_id
                }

                messageText.clearText()
            }
        }
    }
}
