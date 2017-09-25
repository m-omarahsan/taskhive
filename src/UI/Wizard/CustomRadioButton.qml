import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
RadioButton {
    property variant radioLabel: null
    style: RadioButtonStyle {
        label: Text {
            font.pointSize: 22
            text: radioLabel
            color: "#fff"
        }
        indicator: Image {
            source: control.checked ? "../images/07.svg" : "../images/10.svg"
            sourceSize.width: 30
            sourceSize.height: 30
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    if(control.checked === true)
                        control.checked = false
                    control.checked = true
                }
            }
        }
    }
}
