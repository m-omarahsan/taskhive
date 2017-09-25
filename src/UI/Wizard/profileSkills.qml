import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQml 2.2

Item {
    Text {
        id: skillsTitle
        anchors.left: parent.left
        anchors.leftMargin: 30
        text: qsTr("Skills")
        font.pointSize: 24
        color: "#fff"
    }
    Rectangle {
        height: 1
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: skillsTitle.bottom
        anchors.topMargin: 5
    }
    ScrollView {
        id: content
        anchors.top: skillsTitle.bottom
        anchors.topMargin: 45
        anchors.right: parent.right
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        Column {
            id: column
            width: content.width
        }
    }

    Component {
        id: categoryComponent
        RowLayout {
            spacing: 0
            height: 50
        }
    }

    Component {
        id: subLevelComponent
        Column {
            width: 150
        }
    }
    Component {
        id: subCategoryComponent
        Rectangle {
            property alias text: text2.text
            color: "#BD9CBE"
            width: 200
            height: 50
            Text {
                id: text2
                color: "#FEFEFE"
                font.pointSize: 18
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }

    function traverseJSON(data){

        for (var i in data) {
            var category = data[i];
            var categoryItem = categoryComponent.createObject(column);
            var categoryItem2 = subCategoryComponent.createObject(categoryItem, {text: category.name});
            // print(category.sub_categories, category.sub_categories);
            if (category.sub_categories) {
                var subLevelItem = subLevelComponent.createObject(categoryItem);
                for (var j in category.sub_categories) {
                    var subCategory = category.sub_categories[j];
                    var categoryRow = categoryComponent.createObject(subLevelItem);
                    subCategoryComponent.createObject(categoryRow, {text: subCategory.name});
                    print("Created sub_category: " + subCategory.name);
                    if(subCategory.sub_categories){
                        var categoryRow2 = categoryComponent.createObject(categoryRow);
                        var subLevelItem2 = subLevelComponent.createObject(categoryRow2);
                        for(var k in subCategory.sub_categories) {
                            var subCategory2 = subCategory.sub_categories[k];
                            subCategoryComponent.createObject(subLevelItem2, {text: subCategory2.name});
                            print("Created sub_category: " + subCategory2.name);
                        }
                    }
                }
            }
        }
    }
    Component.onCompleted: {
        var data = TaskhiveCategories.getCategories()['categories'];
        traverseJSON(data);

    }
}
