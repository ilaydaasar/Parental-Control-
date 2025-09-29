import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    width: 1000
    height: 600

    ColumnLayout {
        anchors.fill: parent
        spacing: 12
        anchors.margins: 12

        // 🔍 Arama ve Filtre
        RowLayout {
            Layout.fillWidth: true
            spacing: 12

            TextField {
                id: searchField
                placeholderText: "İçerikte ara..."
                font.pixelSize: 14
                Layout.fillWidth: true
                onTextChanged: riskLogModel.setFilter(text)

                background: Rectangle {
                    radius: 6
                    color: "#ffffff"
                    border.color: "#cccccc"
                    border.width: 1
                }
            }

            ComboBox {
                id: typeFilter
                model: ["Tümü", "Silah", "Şiddet", "Küfür"]
                font.pixelSize: 14
                Layout.preferredWidth: 150
                onCurrentTextChanged: riskLogModel.setTypeFilter(currentText)
            }
        }

        // 🧾 Kayıt Listesi
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            ScrollBar.vertical.policy: ScrollBar.AlwaysOn

            ListView {
                id: listView
                model: riskLogModel
                spacing: 10
                clip: true
                width: parent.width

                delegate: Rectangle {
                    width: listView.width
                    height: 130
                    radius: 10
                    color: "#ffffff"
                    border.color: "#dddddd"
                    border.width: 1

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 12
                        spacing: 5

                        Text {
                            text: "🕒 " + timestamp
                            font.pixelSize: 14
                            color: "#222"
                        }

                        Text {
                            text: "⚠️ Risk Türü: " + risk_type
                            font.pixelSize: 14
                            color: risk_type === "Silah" ? "darkred"
                                  : risk_type === "Şiddet" ? "orange"
                                  : risk_type === "Küfür" ? "#aa00aa"
                                  : "#555"
                        }

                        Text {
                            text: "📱 Uygulama: " + app_name
                            font.pixelSize: 14
                            color: "#333"
                        }

                        MouseArea {
                            width: parent.width
                            height: 20
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                popupImage.source = image_path
                                popupImage.visible = true
                            }

                            Text {
                                text: "📁 Görsel: " + image_path
                                font.pixelSize: 12
                                color: "#0066cc"
                                elide: Text.ElideRight
                            }
                        }
                    }
                }
            }
        }

        // 🖼️ Pop-up Resim
        Image {
            id: popupImage
            visible: false
            anchors.centerIn: parent
            source: image_path
            width: 640
            height: 360
            fillMode: Image.PreserveAspectFit
            z: 10

            Rectangle {
                anchors.fill: parent
                color: "black"
                opacity: 0.5
            }

            MouseArea {
                anchors.fill: parent
                onClicked: popupImage.visible = false
            }

            Rectangle {
                width: 640
                height: 360
                color: "white"
                radius: 10
                border.color: "#888"
                border.width: 1
                anchors.centerIn: parent

                Image {
                    anchors.fill: parent
                    source: popupImage.source
                    fillMode: Image.PreserveAspectFit
                }
            }
        }
    }
}
