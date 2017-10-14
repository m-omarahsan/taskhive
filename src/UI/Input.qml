import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.2
import QtQuick 2.7

TextField {
    horizontalAlignment: TextInput.AlignLeft
    style: TextFieldStyle {
        textColor: "#3F3F3F"
        placeholderTextColor: "#BABABA"
        background: Rectangle {
                    border.width: 0
                    color: "transparent"
                }
    }
}
