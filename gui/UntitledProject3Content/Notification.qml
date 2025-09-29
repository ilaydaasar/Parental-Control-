import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: notification
    width: parent ? parent.width : 400
    height: 50
    anchors.top: parent ? parent.top : undefined
    anchors.horizontalCenter: parent ? parent.horizontalCenter : undefined
    color: backgroundColor
    radius: 8
    visible: false
    opacity: 0.95
    z: 999

    property string message: ""
    property color backgroundColor: "#4CAF50" // varsayılan yeşil

    Text {
        text: notification.message
        anchors.centerIn: parent
        font.pixelSize: 16
        color: "white"
    }

    Timer {
        id: hideTimer
        interval: 3000
        running: false
        repeat: false
        onTriggered: notification.visible = false
    }

    function show(msg, color) {
        notification.message = msg
        notification.backgroundColor = color
        notification.visible = true
        hideTimer.restart()
    }
}
