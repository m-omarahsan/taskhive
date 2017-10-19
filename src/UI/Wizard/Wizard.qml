import QtQuick 2.1
import QtQuick.Window 2.2
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.3
import "../"

Window {
    id: wizard
    minimumWidth: 1200
    width: 1200
    height: 800
    minimumHeight: 800
    color: "#3D3D3D"
    visible: false
    title: "Taskhive Wizard"
    property string profileUser: "buyguy"
    property variant portfolioList: ListModel {}
    property variant profiles: ListModel {}
    property variant categories: ListModel {}
    property variant selectedSkills: ListModel {}


    function getCategories(){
        return categories
    }

    Rectangle {
        id: optionsSide
        width: 0.55 * parent.width
        height: parent.height
        color: "transparent"
        StackView {
            anchors.fill: parent
            id: wizardStack
            initialItem: Qt.resolvedUrl('handle.qml')

        }


    }
    Rectangle {
        id: profileExampleSide
        anchors.left: optionsSide.right
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        color: "black"
        RowLayout {
            id: userData
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.topMargin: 50
            height: wizard.height * 0.25
            spacing: 0
            anchors.top: parent.top
            Column {
                width: 30
                height: parent.height
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                Rectangle {
                    width: parent.width
                    height: profileName.height
                    color: "transparent"
                }
                Rectangle {
                    height: 2
                    width: parent.width
                }
            }
            Column
            {
                id: column1
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop;
                Rectangle {
                    id: avatar
                    border.color: "white"
                    border.width: 1
                    height: 150
                    width: 150
                    color: "transparent"
                }
                Row {
                    width: avatar.width
                    height: 25
                    spacing: 10
                    Text {
                        id: fingerprint
                        color: "#fff"
                        text: qsTr("658393102")
                        font.pointSize: 14
                    }
                    Image {
                        sourceSize.height: fingerprint.paintedHeight
                        sourceSize.width: fingerprint.paintedHeight
                        source: "../images/03.svg"
                    }
                }
            }
            Column {
                id: column
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                Layout.fillWidth: true
                Text {
                    id: profileName
                    text: profileUser
                    anchors.left: parent.left
                    anchors.leftMargin: 20
                    font.pointSize: 22
                    color: "#fff"
                }
                Rectangle {
                    height: 2
                    width: parent.width
                }
                Image {
                    id: imgTest
                    sourceSize.width: 300
                    sourceSize.height: 200
                    source: "../images/05.svg"

                }
            }
        }
        StackView {
            id: profileStack
            anchors.top: userData.bottom
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
        }
    }
}
