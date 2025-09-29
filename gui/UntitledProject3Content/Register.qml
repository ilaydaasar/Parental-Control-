import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: root
    width: 1440
    height: 1024

    signal backClicked()
    signal submitClicked(string name, string email, string password)

    property alias emailField: emailInput
    property alias passwordField: passwordInput
    property alias nameField: nameInput

    Rectangle {
        anchors.fill: parent
        color: "white"
        Image {
            source: "images/Frame 7 (2).png"
            anchors.fill: parent
            fillMode: Image.PreserveAspectCrop
        }

        Column {
            x:30
            anchors.centerIn: parent
            spacing: 20

            Text {
                text: "Yeni Hesap Oluştur"
                font.pixelSize: 26
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                anchors.horizontalCenter: parent.horizontalCenter
            }

            TextField {
                id: nameInput
                width: 400
                height: 48
                placeholderText: "Ad Soyad"
                font.pixelSize: 15
                background: Rectangle {
                    color: "#d7d6d6"
                    border.color: "#8f8d8d"
                    radius: 12
                }
            }

            TextField {
                id: emailInput
                width: 400
                height: 48
                placeholderText: "Email"
                font.pixelSize: 15
                background: Rectangle {
                    color: "#d7d6d6"
                    border.color: "#8f8d8d"
                    radius: 12
                }
            }

            TextField {
                id: passwordInput
                width: 400
                height: 48
                placeholderText: "Şifre"
                echoMode: TextInput.Password
                font.pixelSize: 15
                background: Rectangle {
                    color: "#d7d6d6"
                    border.color: "#8f8d8d"
                    radius: 12
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
                        onClicked: backClicked()
                        cursorShape: Qt.PointingHandCursor
                    }
                }

                Rectangle {
                    width: 140
                    height: 44
                    radius: 22
                    color: "#44B678"

                    Text {
                        text: "Kaydol"
                        anchors.centerIn: parent
                        font.pixelSize: 15
                        color: "white"
                        font.bold: true
                    }

                    MouseArea {
                       anchors.fill: parent
                       onClicked: {
                           root.submitClicked(nameInput.text, emailInput.text, passwordInput.text)
                       }
                    }
                }
            }
        }
    }


    Connections {
        target: LoginHandler

        function onRegisterSuccess() {
            console.log("✅ Kayıt başarılı!")
            backClicked()
        }

        function onRegisterFailed(msg) {
            console.log("❌ Kayıt başarısız:", msg)
        }
    }
}
