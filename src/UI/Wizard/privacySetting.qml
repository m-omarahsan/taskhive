import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.2
import QtQuick.Controls.Styles 1.4
Item{
    Rectangle {
        id: mainText
        color: "transparent"
        anchors.fill: parent
        Text {
            id: title
            anchors.left: parent.left
            anchors.top: parent.top
            text: qsTr("Startup Wizard")
            font.pointSize: 42
            font.bold: true
            color: "#fff"
            anchors.leftMargin: 20
        }
        Text {
            id: generalText
            anchors.top: title.bottom
            text: qsTr("Take back your privacy.")
            font.pointSize: 38
            color: "#fff"
            anchors.left: parent.left
            anchors.leftMargin: 20
        }
        Text {
            id: uniqueCustomizeText
            text: qsTr("Choose your privacy model.")
            font.pointSize: 32
            color: "#fff"
            anchors.left: parent.left
            anchors.top: generalText.bottom
            anchors.leftMargin: 20
        }
        Column {
            id: privacyOptions
            anchors.top: uniqueCustomizeText.bottom
            anchors.topMargin: 50
            anchors.right: parent.right
            anchors.left: parent.left
            spacing: 5
            ExclusiveGroup { id: privacyExclusive }

            RowLayout {
                anchors.right: parent.right
                anchors.rightMargin: 0
                anchors.left: parent.left
                anchors.leftMargin: -70
                Image {
                    source: "../images/11.svg"
                    height: 40
                    width: 40
                }
                CustomRadioButton {
                    radioLabel: qsTr("Pseudonymous")
                    Layout.preferredWidth: 230
                    exclusiveGroup: privacyExclusive
                }
                Text {
                    text: qsTr("Your interactions are limited for mutual protection, and you may only transact in cryptocurrencies.")
                    Layout.fillWidth: true
                    font.pointSize: 14
                    color: "#fff"
                    wrapMode: Text.WordWrap

                }
            }
            RowLayout {
                anchors.right: parent.right
                anchors.left: parent.left
                anchors.leftMargin: -70
                Rectangle {
                    color: "#00B4A1"
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    Layout.minimumWidth: parent.width
                    Layout.minimumHeight: fake.height
                    RowLayout {
                        anchors.right: parent.right
                        anchors.left: parent.left
                        Image {
                            source: "../images/12.svg"
                            height: 40
                            width: 40
                        }
                        CustomRadioButton {
                            radioLabel: qsTr("Private")
                            Layout.preferredWidth: 230
                            exclusiveGroup: privacyExclusive
                        }
                        Text {
                            text: qsTr("Your profile contains only what you want it to, and you can choose what payment methods fit your needs, including those which reveal your personal identity.")
                            Layout.fillWidth: true
                            font.pointSize: 14
                            color: "#fff"
                            wrapMode: Text.WordWrap

                        }
                    }
                }
            }
            RowLayout {
                id: fake
                anchors.right: parent.right
                anchors.left: parent.left
                anchors.leftMargin: -70
                visible: false
                    Image {
                        source: "../images/12.svg"
                        height: 40
                        width: 40
                    }
                    CustomRadioButton {
                        radioLabel: qsTr("Private")
                        Layout.preferredWidth: 230

                    }
                    Text {
                        text: qsTr("Your profile contains only what you want it to, and you can choose what payment methods fit your needs, including those which reveal your personal identity.")
                        Layout.fillWidth: true
                        font.pointSize: 14
                        color: "#fff"
                        wrapMode: Text.WordWrap

                    }

            }

        }
    }


    MessageDialog {
        id: warningDialogOpt
        text: "Please select an option to continue."
        standardButtons: StandardButton.Ok
        title: "Option not selected"
        icon: StandardIcon.Warning
    }

    Rectangle {
        id: buttons
        height: wizard.height * 0.10
        anchors.right: parent.right
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        anchors.margins: {
            left: 20
            right: 20
        }
        color: "transparent"
        ForwardButton {
            id: confirmButton
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            wizardStackURL:'privacySetting.qml'
            onClicked: {
                wizardStack.push(Qt.resolvedUrl('privacySetting.qml'))
                if(privacyExclusive.current){
                    wizardStack.push(Qt.resolvedUrl('privacySetting.qml'))
                    mainStack.push(Qt.resolvedUrl('finishedProfile.qml'))
                    var profileData = {
                        "categories": wizard.skills,
                        "handle": wizard.handle,
                        "privacy_level": privacyExclusive.current.radioLabel,
                    }
                    CreateProfile.create(profileData)
                }else {
                    warningDialogOpt.open()
                }

            }

        }

        BackButton {
            id: back
            anchors.left: parent.left
        }
    }
}
