import QtQuick 2.7
import QtQuick.Controls 2.2
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
                font.pointSize: 42
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
            font.pointSize: 38
            color: "#fff"
            anchors.leftMargin: 20
            anchors.left: parent.left
        }
        Text {
            id: uniqueHandleText
            text: qsTr("Let's choose your skills.")
            anchors.top: extra.bottom
            font.pointSize: 32
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
            height: 100
            background: Rectangle {
                color: "#737373"
            }
            Repeater {
                model: wizard.categories

                TabButton {
                    id: tabData
                    property bool selected: false
                    text: modelData.name
                    width: Math.max(100, frame.width / wizard.categories.length)
                    font.pointSize: 18
                    height: parent.height
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
                            color: "#FEFEFE"
                            anchors.horizontalCenter: parent.horizontalCenter
                            anchors.verticalCenter: parent.verticalCenter
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
                            height: 100
                            background: Rectangle {
                                color: "#958096"
                            }
                            Repeater {
                                model: modelData.sub_categories
                                TabButton {
                                    property bool selected: false
                                    id: currentTab
                                    text: modelData.name
                                    font.pointSize: 18
                                    width: Math.max(100, currentTab.width / modelData.length)
                                    height: parent.height
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
                                            color: "#FEFEFE"
                                            anchors.horizontalCenter: parent.horizontalCenter
                                            anchors.verticalCenter: parent.verticalCenter
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
                                    }
                                }
                            }
                        }
                        StackLayout {
                            id: stack3
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: homeTabTab.bottom
                            anchors.bottom: parent.bottom
                            currentIndex: homeTabTab.currentIndex
                            Repeater {
                                model: modelData.sub_categories
                                Item {
                                    TabBar {
                                        id: tabBar
                                        anchors.right: parent.right
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        height: 100
                                        background: Rectangle {
                                            color: "#483E48"
                                        }
                                        Repeater {
                                            model: modelData.sub_categories
                                            TabButton {

                                                property bool selected: false
                                                id: tab2
                                                text: modelData.name
                                                width: Math.max(100, tab2.width / modelData.length)
                                                font.pointSize: 18
                                                height: parent.height
                                                background: Rectangle {
                                                    border.color: "transparent"
                                                    color: tab2.checked ? "#483E48": "#655665"
                                                }
                                                contentItem: Rectangle {
                                                    height: tab2.height
                                                    width: tab2.width
                                                    color: "transparent"
                                                    Flow {
                                                        anchors.left: parent.left
                                                        spacing: 5
                                                        anchors.leftMargin: (parent.width - textContent3.contentWidth - spacing) / 2
                                                        anchors.top: parent.top
                                                        anchors.topMargin: (parent.height - textContent3.contentHeight - spacing) /2
                                                        anchors.fill: parent
                                                        Text {
                                                            id: textContent3
                                                            text: tab2.text
                                                            font: tab2.font
                                                            color: "#FEFEFE"

                                                        }
                                                        Image {
                                                            source: "../images/07.svg"
                                                            sourceSize.height: 30
                                                            sourceSize.width: 30
                                                            visible: tab2.selected ? true: false

                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    StackLayout {
                                        id: stack2
                                        anchors.left: parent.left
                                        anchors.right: parent.right
                                        anchors.top: tabBar.bottom
                                        anchors.bottom: parent.bottom
                                        currentIndex: tabBar.currentIndex
                                        Repeater {
                                            model: modelData.sub_categories
                                            Item {
                                                anchors.fill: parent
                                                TabBar {
                                                    id: lv4Tab
                                                    anchors.right: parent.right
                                                    anchors.left: parent.left
                                                    anchors.top: parent.top
                                                    height: 100
                                                    background: Rectangle {
                                                        color: "#2D272E"
                                                    }
                                                    Repeater {
                                                        model: modelData.sub_categories
                                                        TabButton {
                                                            id: lv4TabButton
                                                            property bool selected: false
                                                            text: modelData.name
                                                            width: Math.max(100, lv4Tab.width / modelData.length)
                                                            font.pointSize: 18
                                                            height: parent.height
                                                            background: Rectangle {
                                                                border.color: "transparent"
                                                                color: lv4TabButton.checked ? "#2D272E": "#39313A"
                                                            }
                                                            contentItem: Rectangle {
                                                                height: lv4TabButton.height
                                                                width: lv4TabButton.width
                                                                color: "transparent"

                                                                Flow {
                                                                    anchors.left: parent.left
                                                                    spacing: 5
                                                                    anchors.leftMargin: (parent.width - textContent4.contentWidth - spacing) / 2
                                                                    anchors.top: parent.top
                                                                    anchors.topMargin: (parent.height - textContent4.contentHeight - spacing) /2
                                                                    anchors.fill: parent
                                                                    Text {
                                                                        id: textContent4
                                                                        text: lv4TabButton.text
                                                                        font: lv4TabButton.font
                                                                        color: "#FEFEFE"

                                                                    }
                                                                    Image {
                                                                        source: "../images/07.svg"
                                                                        sourceSize.height: 30
                                                                        sourceSize.width: 30
                                                                        visible: lv4TabButton.selected ? true: false

                                                                    }
                                                                }

                                                            }
                                                            MouseArea {
                                                                anchors.fill: lv4TabButton
                                                                acceptedButtons: Qt.RightButton
                                                                onClicked: {
                                                                    if(mouse.button == Qt.RightButton){
                                                                        menu.x = mouseX
                                                                        menu.y = mouseY
                                                                        menu.open()
                                                                        tabBar.itemAt(stack2.currentIndex).selected = true
                                                                        homeTabTab.itemAt(stack3.currentIndex).selected = true
                                                                        frame.itemAt(stack1.currentIndex).selected = true
                                                                        parent.selected = true
                                                                    }
                                                                }
                                                            }
                                                            Menu {
                                                                id: menu
                                                                y: lv4TabButton.height
                                                                MenuItem {
                                                                    text: "Add this category."
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                                Rectangle {
                                                    anchors.fill: parent
                                                    color: "#2D272E"
                                                    visible: modelData.sub_categories ? false: true
                                                    Text {
                                                        text: "No subcategories available."
                                                        font.pointSize: 18
                                                        color: "#FEFEFE"
                                                        horizontalAlignment: Text.AlignHCenter
                                                        verticalAlignment: Text.AlignVCenter
                                                    }
                                                }
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
                wizardStackURL: 'portfolio.qml'
                profileStackURL: 'profilePortfolio.qml'
            }
            BackButton {
                id: back
                anchors.leftMargin: 0
            }
        }
    }
}


