import QtQuick 2.6
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import QtQuick.Controls.Styles 1.4

Window {
    id: createWindow
    height: 800
    width: 1200
    color: "#0c0c0c"
    property variant selectedMethods: ListModel {}
    property ListModel keywordList: ListModel {}


    function createPosting(){
        var keywords = []
        for(var i=0; i<createWindow.keywordList.rowCount(); i++){
            keywords.push(createWindow.keywordList.get(i).word);
        }

        var JSON_DATA = {
            "task_keywords": keywords,
            "task_references": ["URL1", "URL2"],
            "task_body": task_body.text,
            "task_title": task_title.text,
            "task_currency": task_currency.currentText,
            "task_type": task_type.currentText,
            "task_cost": task_cost.text,
            "task_deadline": task_deadline.text,
            "task_escrow_required": 1,
            "task_payment_rate_type": "task",
            "task_categories": ['01','02'],
            'task_payment_methods': ['BTC', 'DGE'],
            'task_escrow_recommendation': 'BITCOIN-PUBKEY',
            'task_license': 'CC BY 4.0',
            'task_entropy': 'CURRENTLY-NOT-IN-USE'
        }
        TaskThread.pause()
        Task.createTask(JSON_DATA)
        TaskThread.resume()
    }


    Row {
        id: windowTitleCreate
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 20
        anchors.topMargin: 20
        Text {
            text: "Create a "
            color: "#fff"
            font.pixelSize: 25
        }
        ComboBox {
            id: task_type
            model: ["Request", "Offer"]
        }
    }
    Column {
        id: contentInfo
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
            id: task_title
            height: 40
            width: parent.width
        }
        Text {
            text: "Task Description"
            font.pixelSize: 22
            color: "#fff"
        }
        TextBox {
            id: task_body
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
                id: paymentMethodCombo
                model: ["BTC", "DOGE"]
                width: 100
                height: 40
                onAccepted: {
                    if(createWindow.selectedMethods){
                        if(createWindow.selectedMethods.indexOf({"method":paymentMethodCombo.currentText}) >= 0){
                            createWindow.selectedMethods.append({"method":paymentMethodCombo.currentText});
                        }
                    }
                    else {
                        createWindow.selectedMethods.append({"method":paymentMethodCombo.currentText});
                    }
                }
            }
            Column {
                spacing: 5
                Text {
                    text: "Selected Methods"
                    anchors.horizontalCenter: parent.horizontalCenter
                    color: "#fff"
                    font.pixelSize: 18
                }
                ListView {
                    model: createWindow.selectedMethods
                    delegate: Text {
                        text: modelData.method
                        color: "#fff"
                        font.pixelSize: 16
                    }
                }
            }
            Text {
                text: "Task Currency:"
                anchors.verticalCenter: parent.verticalCenter
                color: "#fff"
                font.pixelSize: 22
                verticalAlignment: Text.AlignVCenter
            }
            Combo {
                id: task_currency
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
                id: task_cost
                height: 40
                width: 100
            }
        }
        Text {
            text: "Deadline"
            color: "#fff"
            font.pixelSize: 22
        }
        Datepicker {
            id: task_deadline
            height: 40
            width: 150
            z: 999
        }
        Row{
            spacing: 5
            Text {
                text: "Insert Keywords"
                color: "#fff"
                font.pixelSize: 22
                anchors.verticalCenter: parent.verticalCenter
            }
            LineEdit {
                id: keyword
                height: 40
                width: 150
                onAccepted: {
                    createWindow.keywordList.append({"word":keyword.text})
                    print("Appended!")
                }
            }
        }
        GridView {
            id: keywords
            model: createWindow.keywordList
            height: 100
            anchors.left: parent.left
            anchors.right: parent.right
            cellHeight: 45
            cellWidth: 105
            delegate: keywordItem
        }
        Component {
            id: keywordItem
            Rectangle {
                radius: 2
                height: 40
                width: 100
                Text {
                    text: "X"
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.rightMargin: 2
                    anchors.topMargin: 2
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            createWindow.keywordList.remove(keywords.currentIndex-1)
                        }
                    }
                }
                Text {
                    text: modelData
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    font.pixelSize: 18
                }

            }
        }

    }
    Row {
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 15
        anchors.right: parent.right
        anchors.rightMargin: 20
        spacing: 15
        Button {
            id: submitB
            text: "Submit"
            onClicked:  {
                createWindow.createPosting()
                createWindow.close()

            }
            style: ButtonStyle {
                label: Label {
                    text: submitB.text
                    font.pixelSize: 18
                    color: "#3F3F3F"
                }
            }
        }
        Button {
            id: cancelB
            text: "Cancel"
            onClicked: {
                createWindow.close()
            }
            style: ButtonStyle {
                label: Label {
                    text: cancelB.text
                    font.pixelSize: 18
                    color: "#3F3F3F"
                }
            }
        }
    }
}
