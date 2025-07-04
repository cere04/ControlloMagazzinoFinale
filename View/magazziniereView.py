from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QGroupBox, QFormLayout, QSpinBox, QMenu, QSpacerItem,
    QSizePolicy, QFrame
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal
from entities.operazione import Operazione, letturaDatabaseArticoli


class FinestraM(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle("Finestra dei Magazzinieri")
        self.setGeometry(200, 200, 700, 300)

        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 15, 20, 20)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        # ---------- top bar ----------
        top_bar = QFrame()
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)

        # ---------- bottone menu ----------
        self.menu_button = QPushButton("☰")
        self.menu_button.setFixedSize(40, 35)
        self.menu_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                color: #0F4C81;
                font-size: 20px;  /* Dimensione font ridotta */
                font-weight: bold;
                qproperty-icon: none;  
            }
            QPushButton:hover {
                color: #1666AA;
                background-color: #e0e6ed;
                border-radius: 4px;
            }
        """)
        self.menu_button.clicked.connect(self.show_user_menu)
        top_bar_layout.addWidget(self.menu_button)

        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        top_bar_layout.addSpacerItem(spacer)

        main_layout.addWidget(top_bar)

        # ---------- contenuto principale ----------
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # ---------- form inserimento giacenza ----------
        nuovaGiacenzaBox = QGroupBox("Nuova Giacenza")
        nuovaGiacenzaLayout = QFormLayout()
        nuovaGiacenzaLayout.setSpacing(15)

        self.sku_ag = QLineEdit()
        self.sku_ag.setPlaceholderText("Inserisci SKU")

        self.numero_ag = QSpinBox()
        self.numero_ag.setMinimum(1)
        self.numero_ag.setMaximum(10000)

        nuovaGiacenzaLayout.addRow("SKU:", self.sku_ag)
        nuovaGiacenzaLayout.addRow("Quantità:", self.numero_ag)

        btn_aggiungi = QPushButton("Aggiungi Giacenza")
        btn_aggiungi.clicked.connect(self.aggiunta)
        nuovaGiacenzaLayout.addWidget(btn_aggiungi)

        nuovaGiacenzaBox.setLayout(nuovaGiacenzaLayout)
        content_layout.addWidget(nuovaGiacenzaBox)

        # ---------- form modifica giacenza ----------
        modificaBox = QGroupBox("Modifica Giacenza")
        modificaLayout = QFormLayout()
        modificaLayout.setSpacing(15)

        self.id_Giacenza = QLineEdit()
        self.id_Giacenza.setPlaceholderText("ID Operazione")

        self.sku_mg = QLineEdit()
        self.sku_mg.setPlaceholderText("SKU")

        self.numero_mg = QSpinBox()
        self.numero_mg.setMinimum(1)
        self.numero_mg.setMaximum(10000)

        modificaLayout.addRow("ID Operazione:", self.id_Giacenza)
        modificaLayout.addRow("SKU:", self.sku_mg)
        modificaLayout.addRow("Quantità:", self.numero_mg)

        btn_modifica = QPushButton("Modifica Giacenza")
        btn_modifica.clicked.connect(self.modifica_)
        modificaLayout.addWidget(btn_modifica)

        modificaBox.setLayout(modificaLayout)
        content_layout.addWidget(modificaBox)

        main_layout.addLayout(content_layout)

        self.apply_style()

        self.show()

    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
                font-family: Arial, sans-serif;
                color: #2d3748;
            }

            QLabel {
                font-weight: 500;
                background-color: transparent;
                font-size: 13px;  /* Dimensione font ridotta */
            } 

            QGroupBox {
                border: 2px solid #0F4C81;
                border-radius: 8px;
                margin: 10px;
                padding: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #0F4C81;
                font-weight: bold;
                font-size: 14px;  /* Dimensione font ridotta */
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #cccccc;
                border-radius: 8px;
                font-size: 13px;  /* Dimensione font ridotta */
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #3A81F1;
            }

            QSpinBox {
                padding: 8px;
                border: 2px solid #cccccc;
                border-radius: 8px;
                font-size: 13px;  /* Dimensione font ridotta */
                color: black;
                padding-right: 25px;
                background-color: white;
            }

            QSpinBox:focus {
                border: 2px solid #3A81F1;
            }

            QSpinBox::up-button, QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: center right;
                width: 16px;
                background-color: none;
            }

            QSpinBox::up-button {
                subcontrol-position: top right;
                margin-top: 2px;
                margin-right: 3px;
            }

            QSpinBox::down-button {
                subcontrol-position: bottom right;
                margin-bottom: 2px;
                margin-right: 3px;
            }

            QPushButton {
                padding: 8px 12px;  /* Padding ridotto */
                background-color: #0F4C81;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;  /* Dimensione font ridotta */
            }
            QPushButton:hover {
                background-color: #1666AA;
            }
            QPushButton:pressed {
                background-color: #0C3C66;
            }

            /* Stile ottimizzato per il menu */
            QMenu {
                background-color: white;
                border: 1px solid #e0e6ed;
                border-radius: 6px;
                padding: 6px;
                min-width: 220px;  
                font-size: 13px;   
            }
            QMenu::item {
                padding: 6px 20px 6px 12px;  
                min-height: 28px;  
            }
            QMenu::item:disabled {
                color: #2d3748;
                background: transparent;
                font-weight: bold;
                font-size: 13px;  
            }
            QMenu::item:selected {
                background-color: #0F4C81;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                background: #e0e6ed;
                margin: 4px 0;
            }
        """)

    def show_user_menu(self):
        """metodo per la visualizzazione dei dati utente nel menu a tendina"""

        menu = QMenu(self)

        nome_completo = QAction(f"Nome: {self.user_data['nome']} {self.user_data['cognome']}", self)
        nome_completo.setEnabled(False)
        menu.addAction(nome_completo)

        ruolo = QAction(f"Ruolo: {self.user_data['ruolo']}", self)
        ruolo.setEnabled(False)
        menu.addAction(ruolo)

        user_id = QAction(f"ID: {self.user_data['codice']}", self)
        user_id.setEnabled(False)
        menu.addAction(user_id)

        menu.addSeparator()

        # ---------- logout button ----------
        logout_action = QAction("Logout", self)
        logout_action.triggered.connect(self.logout)
        menu.addAction(logout_action)

        menu.setStyleSheet(self.styleSheet())

        menu.exec(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))


    def logout(self):
        """metodo per il logout"""

        self.logout_requested.emit()
        self.close()

    def aggiunta(self):
        """ metodo lettura dati in input per l'aggiunta di una giacenza"""

        SKU_AG = self.sku_ag.text().strip()
        N_AG = self.numero_ag.value()

        if not SKU_AG:
            QMessageBox.critical(
                self,
                'Errore',
                'Il campo SKU deve essere compilato'
            )
            return

        lista_articoli = letturaDatabaseArticoli("Model/databaseArticoli.txt")
        sku_exists = any(art['sku'] == SKU_AG for art in lista_articoli)

        if not sku_exists:
            QMessageBox.critical(
                self,
                'Errore',
                f'Lo SKU "{SKU_AG}" non esiste nel database'
            )
            self.sku_ag.clear()
            return

        try:
            O = Operazione()
            O.aggiungiGiacenza(SKU_AG, N_AG)

            QMessageBox.information(
                self,
                'Successo',
                f'Giacenza aggiunta con successo!\n'
                f'SKU: {SKU_AG}\n'
                f'Quantità: {N_AG}'
            )

            self.sku_ag.clear()
            self.numero_ag.setValue(1)

        except Exception as e:
            QMessageBox.critical(
                self,
                'Errore',
                f'Si è verificato un errore durante l\'aggiunta:\n{str(e)}'
            )

    def modifica_(self):
        """ metodo lettura dati in input per la modifica di una giacenza"""

        ID_OP = self.id_Giacenza.text().strip()
        SKU_MG = self.sku_mg.text().strip()
        QTA_MG = self.numero_mg.value()

        if not ID_OP:
            QMessageBox.critical(
                self,
                'Errore',
                'Il campo ID Operazione deve essere compilato'
            )
            return

        if not SKU_MG:
            QMessageBox.critical(
                self,
                'Errore',
                'Il campo SKU deve essere compilato'
            )
            return

        try:
            id_op = int(ID_OP)
            if id_op <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.critical(
                self,
                'Errore',
                'ID Operazione deve essere un numero intero positivo'
            )
            self.id_Giacenza.clear()
            return

        lista_articoli = letturaDatabaseArticoli("Model/databaseArticoli.txt")
        sku_exists = any(art['sku'] == SKU_MG for art in lista_articoli)

        if not sku_exists:
            QMessageBox.critical(
                self,
                'Errore',
                f'Lo SKU "{SKU_MG}" non esiste nel database'
            )
            self.sku_mg.clear()
            return

        try:
            Opp = Operazione()
            result = Opp.modificaGiacenza(id_op, SKU_MG, QTA_MG, None)

            if result is True:
                QMessageBox.critical(
                    self,
                    'Errore',
                    "L'operazione selezionata non è una giacenza"
                )
            elif result == 'Errore':
                QMessageBox.critical(
                    self,
                    'Errore',
                    "Nessuna operazione trovata con l'ID specificato"
                )
            else:
                QMessageBox.information(
                    self,
                    'Successo',
                    f'Giacenza modificata con successo!\n'
                    f'ID: {id_op}\n'
                    f'SKU: {SKU_MG}\n'
                    f'Nuova quantità: {QTA_MG}'
                )

                self.id_Giacenza.clear()
                self.sku_mg.clear()
                self.numero_mg.setValue(1)

        except Exception as e:
            QMessageBox.critical(
                self,
                'Errore',
                f'Si è verificato un errore durante la modifica:\n{str(e)}'
            )