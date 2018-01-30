import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQml 2.2
Item {
    id: item1
    property variant subCategory: wizard.categories.sub_categories
    Rectangle {
        anchors.fill: parent
        color: "transparent"
        Text {
                id: title
                anchors.left: parent.left
                anchors.top: parent.top
                text: qsTr("Startup Wizard")
                font.pixelSize: 42
                font.bold: true
                color: "#fff"
                anchors.margins: {
                    left: 20
                }
            }
        Text {
            id: extra
            anchors.top: title.bottom
            text: qsTr("What are you good at?")
            font.pixelSize: 38
            color: "#fff"
            anchors.leftMargin: 20
            anchors.left: parent.left
        }
        Text {
            id: uniqueHandleText
            text: qsTr("Let's choose your skills.")
            anchors.top: extra.bottom
            font.pixelSize: 32
            color: "#fff"
            anchors.leftMargin: 20
            anchors.left: parent.left
        }
        TabBar {
            id: frame
            anchors.right: parent.right
            anchors.left: parent.left
            anchors.top: uniqueHandleText.bottom
            anchors.topMargin: 100
            height: 180
            background: Rectangle {
                color: "#737373"
            }
            Repeater {
                model: wizard.categories

                TabButton {
                    id: tabData
                    property bool selected: false
                    text: modelData.name
                    font.pixelSize: 18
                    height: parent.height
                    width: 200
                    background: Rectangle {
                        border.color: "transparent"
                        color: tabData.checked ? "#BD9CBE": "#737373"
                    }
                    contentItem: Rectangle {
                        height: tabData.height
                        width: tabData.width
                        color: "transparent"
                        Text {
                            id: textContent
                            text: tabData.text
                            font: tabData.font
                            width: parent.width
                            color: "#FEFEFE"
                            anchors.horizontalCenter: parent.horizontalCenter
                            anchors.verticalCenter: parent.verticalCenter
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            wrapMode: Text.WordWrap
                        }
                        Image {
                            source: "../images/07.svg"
                            sourceSize.height: 40
                            sourceSize.width: 40
                            visible: tabData.selected ? true: false
                            anchors.left: textContent.right
                            anchors.leftMargin: 5
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }
                }

            }
        }

        StackLayout {
            id: stack1
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: buttons.top
            anchors.top: frame.bottom
            currentIndex: frame.currentIndex
            Repeater {
                model: wizard.categories

                Item {
                    id: homeTab

                        TabBar {
                            id: homeTabTab
                            anchors.right: parent.right
                            anchors.left: parent.left
                            anchors.top: parent.top
                            height: 180
                            background: Rectangle {
                                color: "#958096"
                            }
                            Repeater {
                                model: modelData.sub_categories
                                TabButton {
                                    property bool selected: false
                                    id: currentTab
                                    text: modelData.name
                                    font.pixelSize: 18
                                    height: parent.height
                                    width: 200
                                    background: Rectangle {
                                        border.color: "transparent"
                                        color: currentTab.checked ? "#958096": "#8D758E"
                                    }
                                    contentItem: Rectangle {
                                        height: currentTab.height
                                        width: currentTab.width
                                        color: "transparent"
                                        Text {
                                            id: textContent2
                                            text: currentTab.text
                                            font: currentTab.font
                                            width: parent.width
                                            color: "#FEFEFE"
                                            anchors.horizontalCenter: parent.horizontalCenter
                                            anchors.verticalCenter: parent.verticalCenter
                                            wrapMode: Text.WordWrap
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        Image {
                                            source: "../images/07.svg"
                                            sourceSize.height: 40
                                            sourceSize.width: 40
                                            visible: currentTab.selected ? true: false
                                            anchors.left: textContent2.right
                                            anchors.leftMargin: 5
                                            anchors.verticalCenter: parent.verticalCenter
                                        }
                                        MouseArea {
                                            anchors.fill: parent
                                            onDoubleClicked: {
                                                currentTab.selected = true
                                                var found = false;
                                                var someText = frame.itemAt(stack1.currentIndex).text;
                                                print(someText)
                                                for(var i = 0; i<wizard.selectedSkills.count; i++){
                                                    if(wizard.selectedSkills.get(i).name === someText){
                                                        wizard.selectedSkills.get(i).sub_categories.append({"name":currentTab.text});
                                                        wizard.skills.push({"name": someText})
                                                        found = true;
                                                    }
                                                }
                                                if(!found){
                                                    print(currentTab.text)
                                                    wizard.selectedSkills.append({"name":someText, "sub_categories":[{"name":currentTab.text}]})
                                                }
                                                print(window.selectedSkills)
                                            }
                                        }
                                    }
                                }
                            }
                        }
                }
                }
            }
        Rectangle{
            id: buttons
            height: wizard.height * 0.10
            anchors.right: parent.right
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            color: "transparent"
            anchors.margins: {
                left: 20
                right: 20
            }
            ForwardButton {
                id: confirmButton
                anchors.right: parent.right
                onClicked: {
                    wizardStack.push(Qt.resolvedUrl('portfolio.qml'))
                    profileStack.push(Qt.resolvedUrl('profilePortfolio.qml'))
                }
            }
            BackButton {
                id: back
                anchors.leftMargin: 0
            }
        }
    }
}


