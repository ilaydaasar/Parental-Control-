import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    width: 1000
    height: 600
    property string selectedFileContent: ""

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 10

        Text {
            text: "📄 Keylogger Dosyaları"
            font.pixelSize: 22
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        TextField {
            placeholderText: "İçerikte ara..."
            Layout.fillWidth: true
            onTextChanged: keylogData.setFilter(text)
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 20

            // ✅ SOL: Dosya listesi scroll’lu
            ScrollView {
                width: 250
                Layout.fillHeight: true

                ListView {
                    id: fileList
                    model: keylogData
                    width: parent.width
                    implicitHeight: contentHeight
                    clip: true
                    spacing: 4

                    delegate: Rectangle {
                        width: ListView.view.width
                        height: 40
                        color: ListView.isCurrentItem ? "#d6ecff" : "transparent"
                        border.color: "#ccc"
                        radius: 4

                        Text {
                            anchors.centerIn: parent
                            text: model.text.replace(".txt", "")
                            font.pixelSize: 14
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                fileList.currentIndex = index
                                selectedFileContent = keylogData.readFileContent(model.text)
                            }
                        }
                    }
                }
            }

            // ✅ SAĞ: Seçilen dosya içeriği
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true

                TextArea {
                    text: selectedFileContent
                    wrapMode: TextArea.Wrap
                    readOnly: true
                    font.pixelSize: 14
                    placeholderText: "Bir dosya seçiniz..."
                    padding: 10
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignTop
                }
            }
        }
    }
}
