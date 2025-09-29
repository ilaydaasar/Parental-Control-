import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtGraphicalEffects 1.15

Item {
    width: 800
    height: 600

    property string statusMessage: ""
    property bool monitoringActive: settingsHandler.isMonitoring()
    property bool autoStartEnabled: settingsHandler.isAutoStartEnabled()

    Rectangle {
        width: 600
        height: 580
        radius: 20
        color: "white"
        anchors.centerIn: parent

        layer.enabled: true
        layer.effect: DropShadow {
            color: "#999999"
            radius: 10
            samples: 20
            horizontalOffset: 2
            verticalOffset: 2
        }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 32
            spacing: 18

            Label {
                text: "⚙️ Süre Limitleri ve İzleme Kontrolü"
                font.pixelSize: 20
                font.bold: true
                Layout.alignment: Qt.AlignHCenter
            }

            Repeater {
                model: ["web", "video", "chat", "game"]
                delegate: RowLayout {
                    spacing: 10
                    Layout.alignment: Qt.AlignHCenter

                    Label {
                        text: modelData.toUpperCase()
                        font.pixelSize: 14
                        Layout.preferredWidth: 70
                    }

                    SpinBox {
                        value: settingsHandler.getLimit(modelData, "duration")
                        from: 0; to: 600
                        Layout.preferredWidth: 80
                        onValueChanged: settingsHandler.setLimit(modelData, "duration", value)
                    }

                    ComboBox {
                        model: ["none", "notify", "email"]
                        Layout.preferredWidth: 120
                        Component.onCompleted: currentIndex = model.indexOf(settingsHandler.getLimit(modelData, "action"))
                        onCurrentTextChanged: settingsHandler.setLimit(modelData, "action", currentText)
                    }
                }
            }

            CheckBox {
                text: "🖥️ Sistem açıldığında otomatik başlat"
                checked: autoStartEnabled
                onCheckedChanged: settingsHandler.setAutoStartEnabled(checked)
                Layout.alignment: Qt.AlignHCenter
            }

            RowLayout {
                spacing: 16
                Layout.alignment: Qt.AlignHCenter

                Button {
                    text: "💾 Ayarları Kaydet"
                    onClicked: {
                        settingsHandler.saveAll()
                        statusMessage = "✅ Ayarlar kaydedildi"
                    }
                }

                Button {
                    text: monitoringActive ? "🛑 İzlemeyi Durdur" : "▶️ İzlemeyi Başlat"
                    onClicked: {
                        if (monitoringActive) {
                            settingsHandler.stopMonitoring()
                        } else {
                            settingsHandler.startMonitoring()
                        }
                    }
                }
            }

            Button {
                text: "🔒 Şifre Değiştir"
                Layout.alignment: Qt.AlignHCenter
                onClicked: passwordDialog.open()
            }

            Label {
                text: statusMessage
                font.pixelSize: 13
                color: "#444"
                wrapMode: Text.Wrap
                Layout.alignment: Qt.AlignHCenter
            }
        }

        // 🔒 Şifre Değiştir Popup
        Popup {
            id: passwordDialog
            modal: true
            focus: true
            width: 420
            height: 330
            anchors.centerIn: parent
            background: Rectangle {
                color: "white"
                radius: 12
            }

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 24
                spacing: 16
                Layout.alignment: Qt.AlignHCenter

                Label {
                    text: "🔐 Şifre Değiştir"
                    font.pixelSize: 18
                    font.bold: true
                    Layout.alignment: Qt.AlignHCenter
                }

                TextField {
                    id: oldPasswordField
                    placeholderText: "Eski Şifre"
                    echoMode: TextInput.Password
                    Layout.preferredWidth: 260
                    Layout.alignment: Qt.AlignHCenter
                }

                TextField {
                    id: newPasswordField
                    placeholderText: "Yeni Şifre"
                    echoMode: TextInput.Password
                    Layout.preferredWidth: 260
                    Layout.alignment: Qt.AlignHCenter
                }

                TextField {
                    id: confirmPasswordField
                    placeholderText: "Yeni Şifre (Tekrar)"
                    echoMode: TextInput.Password
                    Layout.preferredWidth: 260
                    Layout.alignment: Qt.AlignHCenter
                }

                RowLayout {
                    spacing: 16
                    Layout.alignment: Qt.AlignHCenter

                    Button {
                        text: "İptal"
                        Layout.preferredWidth: 120
                        onClicked: passwordDialog.close()
                    }

                    Button {
                        text: "Güncelle"
                        Layout.preferredWidth: 120
                        onClicked: {
                            if (newPasswordField.text !== confirmPasswordField.text) {
                                statusMessage = "❌ Yeni şifreler eşleşmiyor."
                                return
                            }
                            settingsHandler.change_password(
                                LoginHandler.currentUserEmail,
                                oldPasswordField.text,
                                newPasswordField.text
                            )
                            passwordDialog.close()
                        }
                    }
                }
            }
        }

        Connections {
            target: settingsHandler
            function onMonitoringChanged(active) {
                monitoringActive = active
                statusMessage = active ? "▶️ İzleme başlatıldı" : "🛑 İzleme durduruldu"
            }

            function onStatusMessageChanged(msg) {
                statusMessage = msg
            }
        }
    }
}
