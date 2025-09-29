import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: root
    width: 1440
    height: 1024

    signal registerClicked()
    signal signInClicked()
    signal forgotClicked()

    Rectangle {
        anchors.fill: parent
        color: "white"

        Image {
            source: "images/Frame 6.png"
            anchors.fill: parent
            fillMode: Image.PreserveAspectCrop
        }

        Column {
            x: 129
            anchors.top: parent.top
            anchors.topMargin: 507
            width: 600
            spacing: 30

            TextField {
                id: emailField
                width: 460
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
                id: passwordField
                width: 460
                height: 48
                placeholderText: "Password"
                echoMode: TextInput.Password
                font.pixelSize: 15
                rightPadding: 40
                background: Rectangle {
                    color: "#d7d6d6"
                    border.color: "#8f8d8d"
                    radius: 12
                }

                Item {
                    width: 24
                    height: 24
                    anchors.verticalCenter: passwordField.verticalCenter
                    anchors.right: passwordField.right
                    anchors.rightMargin: 12

                    Image {
                        id: eyeIcon
                        source: passwordField.echoMode === TextInput.Password ? "images/eye.png" : "images/eye-off.png"
                        width: 24
                        height: 24
                        anchors.centerIn: parent
                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                passwordField.echoMode = passwordField.echoMode === TextInput.Password ? TextInput.Normal : TextInput.Password
                            }
                        }
                    }
                }
            }

            CheckBox {
                id: rememberMeRow
                text: "Remember me"
                font.pixelSize: 14
            }

            Row {
                spacing: 12
                x: 80
                y: 200

                Rectangle {
                    id: signInButton
                    width: 140
                    height: 44
                    radius: 22
                    color: "#44B678"
                    Text {
                        text: "Sign in"
                        anchors.centerIn: parent
                        font.pixelSize: 15
                        color: "white"
                        font.bold: true
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            LoginHandler.save_remember_me(emailField.text, rememberMeRow.checked)
                            LoginHandler.login(emailField.text, passwordField.text)
                        }
                    }
                }

                Rectangle {
                    id: registerButton
                    width: 140
                    height: 44
                    radius: 22
                    color: "#E3F9FC"
                    border.color: "#6AC2D1"
                    Text {
                        text: "Register"
                        anchors.centerIn: parent
                        font.pixelSize: 15
                        color: "#009FB7"
                        font.bold: true
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            console.log("➡️ Register butonuna tıklandı")
                            root.registerClicked()
                        }
                    }
                }
            }

            Rectangle {
                width: 360
                height: 24
                color: "transparent"
                x: 50
                Text {
                    anchors.centerIn: parent
                    text: "Forgot password?"
                    font.pixelSize: 14
                    color: "#007af4"
                    font.underline: true
                }
                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.forgotClicked()
                }
            }
        }
    }

    Connections {
        target: LoginHandler

        onLoginSuccess: {
            console.log("✅ Giriş başarılı")
            root.signInClicked()
        }

        onLoginFailed: (msg) => {
            console.log("❌ Giriş başarısız:", msg)
        }

        onRegisterSuccess: {
            console.log("✅ Kayıt başarılı")
        }

        onRegisterFailed: (msg) => {
            console.log("❌ Kayıt başarısız:", msg)
        }
    }

    Component.onCompleted: {
        emailField.text = LoginHandler.load_remember_me()
        rememberMeRow.checked = emailField.text !== ""
    }
}
