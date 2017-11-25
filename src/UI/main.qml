import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.2
import QtQuick.Window 2.1
ApplicationWindow {
        id: window
        minimumWidth: 1200
        minimumHeight: 800
        width: 1200
        height: 800
        color: "#0c0c0c"
        title: "Taskhive"
        visible: true
        flags: Qt.WindowSystemMenuHint | Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.WindowMaximizeButtonHint
        property variant tasks: []
        property variant requests: []
        property variant offers: []
        property variant selectedTask: ListModel
        property variant userData: {"guest": true}
         function updateList(taskList){
             print(taskList)
         }
        TopBar {
            id: toolbar
            width: window.width
            height: window.height * 0.15
        }
        Rectangle {
            id: requests
            height: window.height * 0.40
            width: parent.width
            anchors.top: toolbar.bottom
            color: "transparent"

            Rectangle {
                color: "transparent"
                id: requestsTitle
                anchors.top: parent.top
                width: parent.width
                height: 45
                anchors.topMargin: 50
                Item {
                    anchors.leftMargin: 30
                    anchors.rightMargin: 30
                    anchors.left: requestsTitle.left
                    anchors.right: requestsTitle.right
                    width: parent.width - 20
                    height: parent.height
                    anchors.top: parent.top
                    anchors.topMargin: 0
                    Text {
                        id: requestsText
                        anchors.left: parent.left
                        text: qsTr("Requests")
                        font.pixelSize: 22
                        color: "#fff"
                    }
                    Row {
                        id: filter
                        anchors.right: parent.right
                        height: parent.height
                        spacing: 20
                        Image {
                            id: iconAdd
                            source: "images/icon-add.svg"
                            MouseArea {
                                anchors.fill: parent
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    if(userData.guest){
                                        warningDialog.open()
                                    }
                                    else {
                                        var createTaskComponent = Qt.createComponent("CreateTask.qml")
                                        var create_task = createTaskComponent.createObject(window)
                                        print(createTaskComponent.errorString())
                                        create_task.show()
                                    }
                                }
                            }
                        }
                        Image {
                            id: iconFilter
                            source: "images/icon-filter.svg"
                        }
                    }
                }
                Rectangle {
                    anchors.bottom: requestsTitle.bottom
                    height: 1
                    width: parent.width
                }
            }
            Component {
                id: taskComponent
                Rectangle {
                    id: parentContent
                    anchors.right: parent.right
                    anchors.left: parent.left
                    color: "transparent"
                    height: 60
                    Row {
                        anchors.left: parent.left
                        anchors.right: parent.right
                        Item {
                            width: 4
                            height: parentContent.height
                        }
                        Text {
                            text: modelData.task_title
                            color: "#fff"
                            font.pixelSize: 16
                            width: requestsList.width / 5
                            elide: Text.ElideRight
                        }
                        Item {
                            width: 4
                            height: parentContent.height
                        }

                        Text {
                            text: modelData.task_body
                            color: "#fff"
                            font.pixelSize: 16
                            width: requestsList.width / 5
                            elide: Text.ElideRight
                        }
                        Item {
                            width: 4
                            height: parentContent.height
                        }

                        Text {
                            text: modelData.task_payment_methods[0]
                            color: "#fff"
                            font.pixelSize: 16
                            width: requestsList.width / 5
                        }
                        Item {
                            width: 4
                            height: parentContent.height
                        }
                        Text {
                            text: modelData.task_escrow_required
                            color: "#fff"
                            font.pixelSize: 16
                            width: requestsList.width / 5
                        }
                        Item {
                            width: 4
                            height: parentContent.height
                        }

                        Text {
                            text: modelData.task_currency
                            color: "#fff"
                            font.pixelSize: 16
                            horizontalAlignment: Text.AlignHCenter
                            width: requestsList.width / 5
                        }

                    }
                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onDoubleClicked: {
                            parentContent.ListView.view.currentIndex = index
                            parentContent.forceActiveFocus()
                            window.selectedTask = parentContent.ListView.view.model[index]
                            print("JSON STRING: " +JSON.stringify(window.tasks.offers))
                            var component = Qt.createComponent("TaskInformation.qml")
                            var task_window = component.createObject(window)
                            task_window.show()

                        }
                    }
                }
            }
            Component {
                id: headerComponent
                Rectangle {
                    id: test1
                    height: 60
                    width: requestsList.width
                    color: "transparent"
                    z: 999
                    Row {
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.topMargin: 20
                        Rectangle {
                            width: 2
                            height: test1.height - 25
                            color: "#fff"
                        }
                        Text{
                            width: requestsList.width / 5
                            text: "Title"
                            color: "#fff"
                            font.pixelSize: 18
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        Item {
                            width: 2
                            height: test1.height  - 25
                        }
                        Rectangle {
                            width: 2
                            height: test1.height  - 25
                            color: "#fff"
                        }
                        Text{
                            width: requestsList.width / 5
                            text: "Description"
                            color: "#fff"
                            font.pixelSize: 18
                            horizontalAlignment: Text.AlignHCenter
                        }
                        Item {
                            width: 2
                            height: test1.height
                        }
                        Rectangle {
                            width: 2
                            height: test1.height  - 25
                            color: "#fff"
                        }
                        Text{
                            width: requestsList.width / 5
                            text: "Payment Methods"
                            color: "#fff"
                            font.pixelSize: 18
                            horizontalAlignment: Text.AlignHCenter
                        }
                        Item {
                            width: 2
                            height: test1.height  - 25
                        }
                        Rectangle {
                            width: 2
                            height: test1.height  - 25
                            color: "#fff"
                        }
                        Text{
                            width: requestsList.width / 5
                            text: "Escrow Required"
                            color: "#fff"
                            font.pixelSize: 18
                            horizontalAlignment: Text.AlignHCenter
                        }
                        Rectangle {
                            width: 2
                            height: test1.height  - 25
                            color: "#fff"
                        }
                        Text{
                            width: requestsList.width / 5
                            text: "Currency"
                            color: "#fff"
                            font.pixelSize: 18
                            horizontalAlignment: Text.AlignHCenter
                        }
                        Rectangle {
                            width: 2
                            height: test1.height  - 25
                            color: "#fff"
                        }
                    }
                }
            }
            Component {
                id: highlight
                Rectangle {
                    width: requestsList.width; height: 60 -25
                    color: "lightsteelblue"; radius: 5
                    y: requestsList.currentItem.y
                    Behavior on y {
                        SpringAnimation {
                            spring: 3
                            damping: 0.2
                        }
                    }
                }
            }
            ListView {
                anchors.leftMargin: 30
                anchors.rightMargin: 30
                id: requestsList
                model: window.tasks.requests
                anchors.right: parent.right
                anchors.left: parent.left
                anchors.top: requestsTitle.bottom
                anchors.bottom: parent.bottom
                delegate: taskComponent
                header: headerComponent
                clip: true
                headerPositioning: ListView.OverlayHeader
                highlight: highlight
                highlightFollowsCurrentItem: false
                focus: true
            }
        }
        Rectangle {
            id: offers
            height: window.height * 0.40
            width: parent.width
            anchors.top: requests.bottom
            color: "transparent"
            Rectangle {
                color: "transparent"
                id: offersTitle
                width: parent.width
                height: 45
                Item {
                    anchors.leftMargin: 30
                    anchors.rightMargin: 30
                    anchors.left: offersTitle.left
                    anchors.right: offersTitle.right
                    width: parent.width - 20
                    height: parent.height
                    Text {
                        id: offersText
                        anchors.left: parent.left
                        text: qsTr("Offers")
                        font.pixelSize: 22
                        color: "#fff"
                    }
                    Row {
                        anchors.right: parent.right
                        height: parent.height
                        spacing: 20
                        Image {
                            id: iconAdd2
                            source: "images/icon-add.svg"
                        }
                        Image {
                            id: iconFilter2
                            source: "images/icon-filter.svg"
                        }
                    }
                }
                Rectangle {
                    anchors.bottom: offersTitle.bottom
                    height: 1
                    width: parent.width
                }
            }
            Component {
                id: highlightOffers
                Rectangle {
                    width: offersList.width; height: 60 -25
                    color: "lightsteelblue"; radius: 5
                    y: offersList.currentItem.y
                    Behavior on y {
                        SpringAnimation {
                            spring: 3
                            damping: 0.2
                        }
                    }
                }
            }
            ListView {
                anchors.leftMargin: 30
                anchors.rightMargin: 30
                id: offersList
                model: window.tasks.offers
                anchors.right: parent.right
                anchors.left: parent.left
                anchors.top: offersTitle.bottom
                anchors.bottom: parent.bottom
                delegate: taskComponent
                header: headerComponent
                clip: true
                headerPositioning: ListView.OverlayHeader
                highlight: highlightOffers
                highlightFollowsCurrentItem: false
                focus: true
            }
        }
        Image {
             id: img
             visible: false
             source: "background.png"
             height: window.height * 0.15
             fillMode: Image.PreserveAspectFit
        }

         Row {
             anchors.bottom: parent.bottom
             Repeater {
                 model: Math.ceil(window.width / img.width)
                 ShaderEffectSource {
                     sourceItem: img
                     height: img.height
                     width: img.width
                 }
             }
         }
         Connections {
             target: TaskThread
             onNewTask:{
                window.tasks = result
                window.requests = result.requests
                window.offers = result.offers
             }
         }
         MessageDialog {
             id: warningDialog
             text: "You can't create a task if you don't have a Taskhive User.\n Do you want to go through the Profile Wizard?"
             standardButtons: StandardButton.Yes | StandardButton.No
             title: "Missing User Profile"
             icon: StandardIcon.Warning
             onYes: {
                 var component = Qt.createComponent("Wizard/Wizard.qml")
                 var wizard_window = component.createObject(window)
                 wizard_window.show()
             }
             onNo: {
                 warningDialog.close()
             }
         }
         Component.onCompleted: {
             var profile = Profile.verifyProfile()
             window.userData = profile
             print(window.userData)
             TaskThread.start()
         }
    }

