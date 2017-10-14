import QtQuick 2.6
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2

Window {
    height: 800
    width: 1200
    color: "#0c0c0c"
    Text {
        id: windowTitleCreate
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 20
        anchors.topMargin: 20
        text: "Create a task."
        color: "#fff"
        font.pixelSize: 25
    }
    Column {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.rightMargin: 20
        anchors.leftMargin: 20
        anchors.top: windowTitleCreate.bottom
        anchors.topMargin: 10
        spacing: 10
        Text {
            text: "Task Title"
            font.pixelSize: 22
            color: "#fff"
        }
        LineEdit {
            height: 40
            width: parent.width
        }
        Text {
            text: "Task Description"
            font.pixelSize: 22
            color: "#fff"
        }
        LineEdit {
            height: 200
            width: parent.width
        }
        Row{
            id: row
            width: parent.width
            spacing: 10
            Text {
                text: "Payment Methods:"
                anchors.verticalCenter: parent.verticalCenter
                color: "#fff"
                font.pixelSize: 22
                verticalAlignment: Text.AlignVCenter
            }
            Combo {
                model: ["BTC", "DOGE"]
                width: 100
                height: 40
            }
            Text {
                text: "Task Currency:"
                anchors.verticalCenter: parent.verticalCenter
                color: "#fff"
                font.pixelSize: 22
                verticalAlignment: Text.AlignVCenter
            }
            Combo {
                model: ["BTC", "USD"]
                width: 100
                height: 40
            }
            Text {
                text: "Task Cost:"
                anchors.verticalCenter: parent.verticalCenter
                color: "#fff"
                font.pixelSize: 22
                verticalAlignment: Text.AlignVCenter
            }
            LineEdit {
                height: 40
                width: 100
            }
            Datepicker {
                height: 40
                width: 150
                editable: false
            }
        }
    }
}
