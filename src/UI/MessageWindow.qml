import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 1.4
Window {
    id: messageWindow
    width: 400
    height: 600
    color: "#3D3D3D"
    property ListModel messages: ListModel {}
    property var msg
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
            readonly property bool sentByMe: modelData.sender !== window.userData.public_key
            spacing: 10
            Text {
                text: sentByMe ? "You": sender
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
                    text: body
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
        TextArea {
            id: messageText
            height: 150
            width: rectRow.width - 50

        }
        Button {
            height: 40
            width: 40
            text: "Send"
            onClicked: {
                print(messageText.text)
                messageWindow.messages.append({"body": messageText.text, "sender": window.userData.public_key })
                print(messageWindow.messages)
                var messageInfo = {
                    "bit_address": taskWindow.task.task_address,
                    "task_id": taskWindow.task.task_id,
                    "body": messageText.text,
                    "public_key": window.userData.public_key
                }

                messageText.text = ''
                Message.sendMessage(messageInfo)
            }
        }
    }

    Connections {
        target: Message
        onMsgThread: {
            print("TEST: "+ msg.length)
            if(msg.length !== 0){
                var mes = msg[0].messageThread
                for(var i = 0; i<mes.length; i++){
                    messageWindow.messages.append(mes[i].payload)
                    print(msg[i])
                }
            }
        }
    }
    Component.onCompleted:  {
        Message.getMessageThread(window.selectedTask.task_id, window.selectedTask.bit_address)
    }
}
