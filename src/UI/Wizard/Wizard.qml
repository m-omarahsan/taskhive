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
    property variant portfolioList: ListModel {}
    property variant profiles: ListModel {}
    property variant categories: ListModel {}
    property variant selectedSkills: ListModel {}
    property variant skills: []
    property string handle: "Guest"
    property string privacy


    function getCategories(){
        return categories
    }
    StackView {
        id: mainStack
        anchors.fill: parent
        initialItem: Qt.resolvedUrl('creationProfile.qml')
    }
}
