import QtQuick 2.7
import QtQuick.Controls 1.4

 ScrollView {
        property alias text: control.text
     function clearText(){
         control.text = ''
     }
        TextArea {
            id: control
            wrapMode: TextEdit.WordWrap
            font.pixelSize: 18
        }
    }

