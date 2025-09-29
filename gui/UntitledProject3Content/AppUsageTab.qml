import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    width: 1000
    height: 700

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20

        Label {
            text: "📊 Uygulama Kullanım Geçmişi"
            font.pixelSize: 20
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            ListView {
                id: usageList
                model: appUsageModel
                spacing: 12
                clip: true

                delegate: Rectangle {
                    width: usageList.width
                    height: 100
                    radius: 12
                    color: "#ffffff"
                    border.color: "#dddddd"
                    border.width: 1

                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 16
                        spacing: 16

                        // 1️⃣ Kategori ikonu
                        Image {
                            width: 28
                            height: 28
                            fillMode: Image.PreserveAspectFit
                            Layout.alignment: Qt.AlignVCenter
                            source: context === "web" ? "icons/web.png"
                                  : context === "video" ? "icons/video.png"
                                  : context === "game" ? "icons/game.png"
                                  : context === "chat" ? "icons/chat.png"
                                  : "icons/other.png"
                        }

                        // 2️⃣ Metin bloğu (sabit genişlik verildi)
                        ColumnLayout {
                            spacing: 4
                            Layout.preferredWidth: 700

                            Text {
                                text: "📱 " + app_name + " (" + start_time.split(" ")[0] + ")"
                                font.pixelSize: 15
                                font.bold: true
                                color: "#222"
                                elide: Text.ElideRight
                            }

                            Text {
                                text: "⏱️ Süre: " + Math.floor(duration_seconds / 60) + " dk " + (duration_seconds % 60) + " sn"
                                font.pixelSize: 13
                                color: "#555"
                                elide: Text.ElideRight
                            }

                            Text {
                                text: "🕒 " + start_time.split(" ")[1] + " - " + end_time.split(" ")[1]
                                font.pixelSize: 13
                                color: "#666"
                                elide: Text.ElideRight
                            }
                        }

                        // 3️⃣ Kategori ismi
                        Text {
                            text: context.toUpperCase()
                            font.pixelSize: 12
                            color: "#888"
                            Layout.alignment: Qt.AlignVCenter
                            Layout.preferredWidth: 60
                            horizontalAlignment: Text.AlignRight
                        }
                    }
                }
            }
        }
    }
}
