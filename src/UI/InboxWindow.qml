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
            model: inboxWindow.messages
        }

    }
    Component {
        id: inboxList
        Rectangle {
            anchors.right: parent.right
            anchors.left: parent.left
            height: 100
            Row {
                anchors.fill: parent
                Text {
                    font.pixelSize: 18
                    wrapMode: Text.WordWrap
                    color: "#FFF"
                    text: sender
                }
            }
        }
    }
    Component.onCompleted: {
        Message.getInbox()
    }
}
