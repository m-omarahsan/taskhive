import QtQuick 2.7
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.2
import QtQuick.Window 2.2
Window {
    id: inboxWindow
    width: 600
    height: 400
    color: "#3D3D3D"

    property ListModel messages: ListModel {}
    ScrollView {
        anchors.top: parent.top
        anchors.bottom: parent.bottom.top
        anchors.leftMargin: 20
        anchors.rightMargin: 20
        anchors.right: parent.right
        anchors.left: parent.left
        frameVisible: false
        horizontalScrollBarPolicy: Qt.ScrollBarAlwaysOff
        verticalScrollBarPolicy: Qt.ScrollBarAlwaysOff
        ListView {
            anchors.fill: parent
            anchors.topMargin: 10
            delegate: inboxList
            spacing: 10
            header: headerInbox
            model: inboxWindow.messages
        }

    }
    Component {
        id: headerInbox
        Rectangle {
            anchors.right: parent.right
            anchors.left: parent.left
            height: 50
            color: "transparent"
            Row {
                anchors.fill: parent
                spacing: 10
                Text {
                    font.pixelSize: 18
                    wrapMode: Text.WordWrap
                    color: "#FFF"
                    text: "Sender"
                }
                Item {
                    width: 2
                    height: parent.height  - 25
                }
                Rectangle {
                    width: 2
                    height: parent.height  - 25
                    color: "#fff"
                }
                Text {
                    font.pixelSize: 18
                    wrapMode: Text.WordWrap
                    color: "#FFF"
                    text: "Message"
                }
            }
        }
    }
    Component {
        id: inboxList
        Rectangle {
            anchors.right: parent.right
            anchors.left: parent.left
            height: 50
            color: "transparent"
            Row {
                anchors.fill: parent
                Text {
                    font.pixelSize: 18
                    wrapMode: Text.WordWrap
                    color: "#FFF"
                    text: fromAddress
                }
                Item {
                    width: 4
                    height: parent.height  - 25
                }
                Text {
                    font.pixelSize: 18
                    wrapMode: Text.WordWrap
                    color: "#FFF"
                    text: body
                }
            }
        }
    }
    Connections {
        target: Message
        onMsgThread: {
            for(var i=0;i<msg.length;i++){
                inboxWindow.messages.append({"fromAddress": msg[i].fromAddress, "body": msg[i].messageThread[0].payload.body})
            }
        }
    }
    Component.onCompleted: {
        Message.getMessageThread(window.selectedTask.task_id)
    }
}
