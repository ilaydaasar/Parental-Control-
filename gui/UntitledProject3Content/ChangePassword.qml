Item {
    width: 400; height: 300
    signal changePasswordClicked(string email, string oldPassword, string newPassword)

    Column {
        spacing: 10
        TextField { id: oldPass; placeholderText: "Eski Şifre" }
        TextField { id: newPass; placeholderText: "Yeni Şifre" }
        TextField { id: newPassAgain; placeholderText: "Yeni Şifre Tekrar" }

        Button {
            text: "Şifreyi Değiştir"
            onClicked: {
                if (newPass.text !== newPassAgain.text) {
                    console.log("Yeni şifreler eşleşmiyor.")
                    return
                }
                changePasswordClicked(currentEmail, oldPass.text, newPass.text)
            }
        }
    }

    Connections {
        target: LoginHandler
        function onResetSuccess() {
            console.log("✅ Şifre değiştirildi.")
        }

        function onResetFailed(msg) {
            console.log("❌ Hata:", msg)
        }
    }
}
