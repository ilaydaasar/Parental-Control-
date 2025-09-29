import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: root
    width: 1440
    height: 1024

    signal backToLogin()
    signal resetClicked(string email)

    Rectangle {
        anchors.fill: parent
        color: "white"

        Column {
            anchors.centerIn: parent
            spacing: 20

            Text {
                text: "Şifre Sıfırlama"
                font.pixelSize: 26
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                text: "Kayıtlı e-posta adresinizi girin, yeni şifre gönderilecek."
                font.pixelSize: 14
                color: "#666666"
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                anchors.horizontalCenter: parent.horizontalCenter
                width: 400
            }

            TextField {
                id: emailField
                width: 400
                height: 48
                placeholderText: "Email"
                font.pixelSize: 15
                background: Rectangle {
                    color: "#f0f0f0"
                    border.color: "#999999"
                    radius: 10
                }
            }

            Row {
                spacing: 20
                anchors.horizontalCenter: parent.horizontalCenter

                Rectangle {
                    width: 140
                    height: 44
                    radius: 22
                    color: "#E3F9FC"
                    border.color: "#6AC2D1"
                    Text {
                        text: "Geri"
                        anchors.centerIn: parent
                        font.pixelSize: 15
                        color: "#009FB7"
                        font.bold: true
                    }
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: root.backToLogin()
                    }
                }

                Rectangle {
                    width: 160
                    height: 44
                    radius: 22
                    color: "#44B678"
                    Text {
                        text: "Şifreyi Gönder"
                        anchors.centerIn: parent
                        font.pixelSize: 15
                        color: "white"
                        font.bold: true
                    }
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            console.log("🧪 Butona tıklandı", emailField.text)
                            root.resetClicked(emailField.text)
                        }
                    }
                }
            }
        }
    }

    // Backend bağlantısı
    Connections {
        target: LoginHandler

        function onResetSuccess() {
            Qt.createQmlObject('import QtQuick 2.15; import QtQuick.Controls 2.15; MessageDialog { text: "Yeni şifreniz e-posta adresinize gönderildi."; visible: true; icon: StandardIcon.Information }', root)
        }

        function onResetFailed(msg) {
            Qt.createQmlObject(`import QtQuick 2.15; import QtQuick.Controls 2.15; MessageDialog { text: "${msg}"; visible: true; icon: StandardIcon.Critical }`, root)
        }
    }
}
