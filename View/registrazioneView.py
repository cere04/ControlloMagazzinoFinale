from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLineEdit,
    QLabel, QComboBox, QMessageBox
)
from Controllers.auth_service import AuthService

STYLESHEET = """
    QWidget {
        background-color: #ffffff;
        font-family: Arial, sans-serif;
        color: #000000;
    }

    QMainWindow {
        background-color: #f5f7fa;
    }

    QLabel {
        color: #2d3748;
    }

    QLabel[objectName^="label_"] {
        font-weight: 600;
    }

    QLabel[objectName="label_10"] {
        font-size: 16px;
        font-weight: 700;
        color: #4a5568;
        padding-bottom: 8px;
    }

    QLineEdit {
        padding: 8px;
        border: 2px solid #cccccc;
        border-radius: 8px;
        font-size: 14px;
        color: black;
    }

    QLineEdit:focus {
        border: 2px solid #3A81F1;
    }

    QComboBox {
        padding: 8px;
        border: 2px solid #cccccc;
        border-radius: 8px;
        font-size: 14px;
        color: black;
    }

    QComboBox:focus {
        border: 2px solid #3A81F1;
    }

    QComboBox QAbstractItemView {
        border: 2px solid #cccccc;
        border-radius: 8px;
        padding: 8px;
        background: white;
        selection-background-color: #0F4C81;
        selection-color: white;
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: center right;
        width: 15px;
        background: none;
        margin-right: 4px;
    }

    QPushButton {
        padding: 10px;
        background-color: #0F4C81;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #1666AA;
    }

    QPushButton:pressed {
        background-color: #0C3C66;
    }
"""


class FinestraR(QWidget):
    def __init__(self, loginView):
        super().__init__()
        self.loginView = loginView
        self.finestra_1 = None
        self.setWindowTitle("Finestra di Registrazione")
        self.setGeometry(200, 200, 400, 300)

        self.setStyleSheet(STYLESHEET)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

        # ---------- form registrazione ----------
        self.titolo = QLabel('Registrazione')
        self.titolo.setObjectName("label_10")
        self.titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.titolo)

        self.layout.addWidget(QLabel('NOME'))
        self.Label1 = QLineEdit()
        self.Label1.setPlaceholderText("Inserisci nome")
        self.Label1.setObjectName("lineEdit_nome")
        self.layout.addWidget(self.Label1)

        self.layout.addWidget(QLabel('COGNOME'))
        self.Label2 = QLineEdit()
        self.Label2.setPlaceholderText("Inserisci cognome")
        self.Label2.setObjectName("lineEdit_cognome")
        self.layout.addWidget(self.Label2)

        self.layout.addWidget(QLabel('RUOLO'))
        self.label3 = QComboBox()
        self.label3.setObjectName("comboBox_ruolo")
        self.label3.addItems(["Magazziniere", "Commesso", "Responsabile Commerciale"])
        self.label3.setCurrentIndex(-1)  # Nessuna selezione iniziale
        self.layout.addWidget(self.label3)

        self.ButtonA = QPushButton('Registrati')
        self.ButtonA.setObjectName("button_registrati")
        self.layout.addWidget(self.ButtonA)
        self.ButtonA.clicked.connect(self.Registrazione)

    def Registrazione(self):
        """ metodo lettura dati in input per la registrazione"""

        nome = self.Label1.text().strip()
        cognome = self.Label2.text().strip()

        if not nome or not cognome:
            QMessageBox.critical(
                self,
                "Errore",
                "Campi mancanti\nCompilare tutto per il rilascio del nome utente"
            )
            return

        b = AuthService()
        username = b.aggiungiUtenti(nome, cognome, self.label3.currentText())

        if username is None:
            QMessageBox.critical(
                self,
                "Errore",
                "Si è verificato un errore durante la registrazione"
            )
        else:
            QMessageBox.information(
                self,
                "Nome Utente",
                f"Registrazione avvenuta con successo\nIl tuo nome utente è: {username}"
            )
            self.hide()
            self.loginView.show()