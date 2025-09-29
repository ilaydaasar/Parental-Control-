import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: mainRoot
    signal logoutRequested()

    width: 1440
    height: 1024

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // 🔲 TabBar + Logout aynı yatay satırda
        RowLayout {
            Layout.fillWidth: true
            spacing: 0
            height: 40

            TabBar {
                id: tabBar
                Layout.fillWidth: true
                height: 40

                TabButton { text: "Dashboard" }
                TabButton { text: "Keylogs" }
                TabButton { text: "Risk Logs" }
                TabButton { text: "App Usage" }
                TabButton { text: "Settings" }
            }

            MouseArea {
                width: 48
                height: 40
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: mainRoot.logoutRequested()

                Image {
                    source: "images/logout.png" // ikon beyaz olmalı
                    anchors.centerIn: parent
                    width: 24
                    height: 40
                    fillMode: Image.PreserveAspectFit
                }
            }
        }

        // 🔲 Sayfa içerikleri
        StackLayout {
            id: stack
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: tabBar.currentIndex

            DashboardTab {}
            KeylogTab {}
            RiskLogTab {}
            AppUsageTab {}
            SettingsTab {}
        }
    }
}
