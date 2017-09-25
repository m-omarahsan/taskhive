import QtQuick 2.0
import QtGraphicalEffects 1.0
Item {
    id: item1
    property variant wizardStackURL: null
    property variant profileStackURL: null
    property int sizeH: 80
    property int sizeW: 80
    height: sizeH
    width: sizeW
    Image {
        id: confirmButton
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        sourceSize.height: 60
        sourceSize.width: 60
        source: Qt.resolvedUrl('../images/01.svg')
        anchors.centerIn: parent
        MouseArea {
            anchors.fill: parent
            onClicked: {
                wizardStack.push(Qt.resolvedUrl(wizardStackURL))
                profileStack.push(Qt.resolvedUrl(profileStackURL))
            }
       onPressed: {
           overlay.visible = true
       }
       onReleased: {
           overlay.visible = false
       }
        }

    }
    ColorOverlay {
        id: overlay
        anchors.fill: confirmButton
        source: confirmButton
        color: "blue"
        visible: false
        opacity: 0.2

    }
}
