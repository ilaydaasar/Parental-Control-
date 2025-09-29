import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtCharts 2.15

Rectangle {
    width: 1440
    height: 1024
    color: "#f7f9fc"

    property int totalRisks: 0
    property string screenTime: ""
    property string mostUsedApp: ""
    property int activeUsers: 0
    property var pieData: [0, 0, 0]
    property var riskTimeData: []
    property var riskImages: []

    Component.onCompleted: {
        if (dashboardData) {
            totalRisks = dashboardData.totalRisks
            screenTime = dashboardData.screenTime
            mostUsedApp = dashboardData.mostUsedApp
            activeUsers = dashboardData.activeUsers
            pieData = dashboardData.pieData
            riskTimeData = dashboardData.riskTimeData
            riskImages = dashboardData.riskImages
        } else {
            console.warn("⚠️ dashboardData bağlanamadı.")
        }
    }

    Timer {
        id: imageRefreshTimer
        interval: 40000
        running: true
        repeat: true
        onTriggered: {
            riskImages = dashboardData.refreshRiskImages()
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 32
        spacing: 24

        // KPI Bilgileri
        GridLayout {
            columns: 4
            rowSpacing: 16
            columnSpacing: 24
            Layout.fillWidth: true
            Layout.preferredHeight: 120

            Repeater {
                model: [
                    { icon: "❗", title: "Toplam Risk Sayısı", value: totalRisks, color: "#ffcccc" },
                    { icon: "🕒", title: "Günlük Ekran Süresi", value: screenTime, color: "#cce0ff" },
                    { icon: "▶️", title: "En Riskli Uygulama", value: mostUsedApp, color: "#ffe0b3" },
                    { icon: "👤", title: "Aktif Kullanıcı", value: activeUsers, color: "#cceccc" }
                ]
                delegate: Rectangle {
                    width: 300
                    height: 100
                    radius: 16
                    color: "#ffffff"
                    border.color: "#e0e0e0"
                    Layout.alignment: Qt.AlignTop

                    Row {
                        anchors.centerIn: parent
                        spacing: 12
                        Rectangle {
                            width: 40; height: 40; radius: 20
                            color: modelData.color
                            Text { anchors.centerIn: parent; text: modelData.icon; font.pixelSize: 20 }
                        }
                        Column {
                            spacing: 4
                            Text { text: modelData.title; font.pixelSize: 14; color: "#666" }
                            Text { text: modelData.value; font.pixelSize: 20; font.bold: true; color: "#111" }
                        }
                    }
                }
            }
        }

        // Grafikler
        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 300
            spacing: 16

            // Pie Chart
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 300
                radius: 16
                color: "#ffffff"
                border.color: "#ddd"
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 8
                    Text { text: "📊 Risk Dağılımı"; font.pixelSize: 16; font.bold: true }
                    ChartView {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        legend.visible: true
                        antialiasing: true
                        PieSeries {
                            PieSlice { label: "Şiddet"; value: pieData.length > 0 ? pieData[0] : 0; color: "#ffb74d" }
                            PieSlice { label: "Silah"; value: pieData.length > 1 ? pieData[1] : 0; color: "#4fc3f7" }
                            PieSlice { label: "Küfür"; value: pieData.length > 2 ? pieData[2] : 0; color: "#81c784" }
                        }
                    }
                }
            }

            // Line Chart
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 300
                radius: 16
                color: "#ffffff"
                border.color: "#ddd"
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 8
                    Text { text: "📈 Günlük Risk Zaman Grafiği"; font.pixelSize: 16; font.bold: true }
                    ChartView {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        antialiasing: true
                        legend.visible: false
                        ValueAxis { id: axisX; min: 0; max: 23; titleText: "Saat" }
                        ValueAxis { id: axisY; min: 0; max: 10; titleText: "Risk Sayısı" }
                        LineSeries {
                            id: riskLine
                            axisX: axisX
                            axisY: axisY
                            Component.onCompleted: {
                                var maxValue = 1
                                for (var i = 0; i < riskTimeData.length; ++i) {
                                    var hour = riskTimeData[i].hour
                                    var value = riskTimeData[i].value
                                    append(hour, value)
                                    if (value > maxValue)
                                        maxValue = value
                                }
                                axisY.max = maxValue + 1
                            }
                        }
                    }
                }
            }
        }

        // Riskli Görseller
        ColumnLayout {
            spacing: 6
            anchors.horizontalCenter: parent.horizontalCenter
            Text {
                text: "📸 Riskli Görüntüler"
                font.pixelSize: 16
                font.bold: true
            }

            Flickable {
                Layout.preferredHeight: 160
                Layout.preferredWidth: 1200
                clip: true

                Row {
                    id: rowImages
                    spacing: 16
                    anchors.horizontalCenter: parent.horizontalCenter

                    Repeater {
                        model: riskImages
                        delegate: Rectangle {
                            width: 200
                            height: 140
                            radius: 12
                            color: "#eee"
                            Image {
                                source: modelData
                                anchors.fill: parent
                                fillMode: Image.PreserveAspectCrop
                            }
                        }
                    }
                }
            }
        }
    }
}
