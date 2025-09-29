import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15


Window {
    visible: true
    width: 1440
    height: 1024
    title: qsTr("KidShield Login")

    Loader {
        id: uiLoader
        source: "loginpage.qml"
        anchors.fill: parent

        onLoaded: {
            if (uiLoader.item.registerClicked)
                uiLoader.item.registerClicked.connect(() => uiLoader.source = "Register.qml");

            if (uiLoader.item.signInClicked)
                uiLoader.item.signInClicked.connect(() => {
                    console.log("➡️ Dashboarda geçiliyor")
                    uiLoader.source = "Mainw.qml"
                });

            if (uiLoader.item.forgotClicked)
                uiLoader.item.forgotClicked.connect(() => uiLoader.source = "Forpass.qml");

            if (uiLoader.item.backClicked)
                uiLoader.item.backClicked.connect(() => uiLoader.source = "loginpage.qml");

            if (uiLoader.item.submitClicked)
                uiLoader.item.submitClicked.connect((name, email, password) => {
                    LoginHandler.register(name, email, password);
                });

            if (uiLoader.item.backToLogin)
                uiLoader.item.backToLogin.connect(() => uiLoader.source = "loginpage.qml");

            if (uiLoader.item.logoutRequested)
                uiLoader.item.logoutRequested.connect(() => uiLoader.source = "loginpage.qml");

            // 🔔 Şifre sıfırlama tıklama bağlantısı
            
             if (uiLoader.item.resetClicked) {
                uiLoader.item.resetClicked.connect((email) => {
                    console.log("📨 resetClicked tetiklendi: " + email)
                    LoginHandler.send_reset_email(email)
                })
            }
            if (uiLoader.item.changePasswordClicked) {
                uiLoader.item.changePasswordClicked.connect((email, oldPass, newPass) => {
                console.log("🛠 Şifre değiştiriliyor: ", email)
                LoginHandler.change_password(email, oldPass, newPass)
    });
}

           
        }
    }

    Notification {
        id: alertBox
    }

    Connections {
        target: LoginHandler

        function onLoginSuccess() {
            console.log("✅ Giriş başarılı!")
            alertBox.show("Giriş başarılı! Yönlendiriliyorsunuz...", "#4CAF50")
            Qt.callLater(() => {
                uiLoader.source = "Mainw.qml"
            })
        }

        function onLoginFailed(msg) {
            console.log("❌ Giriş başarısız:", msg)
            alertBox.show(msg, "#F44336")
        }

        function onRegisterSuccess() {
            console.log("✅ Kayıt başarılı!")
            alertBox.show("Hesabınız başarıyla oluşturuldu.", "#4CAF50")
            uiLoader.source = "loginpage.qml"
        }

        function onRegisterFailed(msg) {
            console.log("❌ Kayıt başarısız:", msg)
            alertBox.show(msg, "#F44336")
        }

        function onResetSuccess() {
            console.log("📧 Reset mail gönderildi.")
            alertBox.show("Yeni şifreniz e-posta adresinize gönderildi.", "#4CAF50")
        }

        function onResetFailed(msg) {
            console.log("🚫 Reset hatası:", msg)
            alertBox.show(msg, "#F44336")

        function onResetSuccess() {
            console.log("✅ Şifre değiştirildi.")
            alertBox.show("Şifreniz başarıyla güncellendi.", "#4CAF50")
        }

        function onResetFailed(msg) {
            console.log("❌ Hata:", msg)
            alertBox.show(msg, "#F44336")
        }
    
        }
    }
}
