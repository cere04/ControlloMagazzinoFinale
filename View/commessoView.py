from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QGroupBox, QFormLayout, QSpinBox, QComboBox, QMenu,
    QSpacerItem, QSizePolicy, QFrame
)
from PyQt6.QtGui import QAction
from entities.operazione import Operazione, letturaDatabaseArticoli


class FinestraC(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle("Finestra dei Commessi")
        self.setGeometry(200, 200, 700, 300)

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
                font-size: 20px;
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

        nuovaVenditaBox = QGroupBox("Nuova Vendita")
        nuovaVenditaLayout = QFormLayout()
        nuovaVenditaLayout.setSpacing(15)

        self.sku_av = QLineEdit()
        self.sku_av.setPlaceholderText("Inserisci SKU")

        self.numero_av = QSpinBox()
        self.numero_av.setMinimum(1)
        self.numero_av.setMaximum(10000)

        self.paese_av = QComboBox()
        self.paese_av.addItem("Italia")
        self.paese_av.addItem("Germania")
        self.paese_av.addItem("Francia")
        self.paese_av.addItem("Spagna")
        self.paese_av.setCurrentIndex(-1)

        nuovaVenditaLayout.addRow("SKU:", self.sku_av)
        nuovaVenditaLayout.addRow("Quantità:", self.numero_av)
        nuovaVenditaLayout.addRow("Paese:", self.paese_av)

        btn_aggiungi = QPushButton("Aggiungi Vendita")
        btn_aggiungi.clicked.connect(self.aggiunta)
        nuovaVenditaLayout.addWidget(btn_aggiungi)

        nuovaVenditaBox.setLayout(nuovaVenditaLayout)
        content_layout.addWidget(nuovaVenditaBox)

        # ---------- form modifica vendita ----------
        modificaVenditaBox = QGroupBox("Modifica Vendita")
        modificaVenditaLayout = QFormLayout()
        modificaVenditaLayout.setSpacing(15)

        self.id_Vendita = QLineEdit()
        self.id_Vendita.setPlaceholderText("ID Vendita")

        self.sku_mv = QLineEdit()
        self.sku_mv.setPlaceholderText("SKU")

        self.numero_mv = QSpinBox()
        self.numero_mv.setMinimum(1)
        self.numero_mv.setMaximum(10000)

        self.paese_mv = QComboBox()
        self.paese_mv.addItem("Italia")
        self.paese_mv.addItem("Germania")
        self.paese_mv.addItem("Francia")
        self.paese_mv.addItem("Spagna")
        self.paese_mv.setCurrentIndex(-1)

        modificaVenditaLayout.addRow("ID Vendita:", self.id_Vendita)
        modificaVenditaLayout.addRow("SKU:", self.sku_mv)
        modificaVenditaLayout.addRow("Quantità:", self.numero_mv)
        modificaVenditaLayout.addRow("Paese:", self.paese_mv)

        btn_modifica = QPushButton("Modifica Vendita")
        btn_modifica.clicked.connect(self.modifica_v_)
        modificaVenditaLayout.addWidget(btn_modifica)

        modificaVenditaBox.setLayout(modificaVenditaLayout)
        content_layout.addWidget(modificaVenditaBox)

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
                font-size: 13px;
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
                font-size: 14px;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #cccccc;
                border-radius: 8px;
                font-size: 13px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #3A81F1;
            }

            /* ComboBox styling */
            QComboBox {
                padding: 8px;
                border: 2px solid #cccccc;
                border-radius: 8px;
                font-size: 13px;
                color: black;
                background-color: white;
            }

            QComboBox:focus {
                border: 2px solid #3A81F1;
            }

            QComboBox QAbstractItemView {
                border: 2px solid #cccccc;
                border-radius: 8px;
                padding: 6px;
                background: white;
                selection-background-color: #0F4C81;
                selection-color: white;
                font-size: 13px;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 15px;
                background: none;
                margin-right: 4px;
            }

            /* SpinBox styling */
            QSpinBox {
                padding: 8px;
                border: 2px solid #cccccc;
                border-radius: 8px;
                font-size: 13px;
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
                padding: 8px 12px;
                background-color: #0F4C81;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
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
        """ metodo lettura dati in input per l'aggiunta di una vendita"""

        SKU_AV = self.sku_av.text().strip()
        N_AV = self.numero_av.value()
        P_AV = self.paese_av.currentText().strip()

        if not SKU_AV:
            QMessageBox.critical(
                self,
                'Errore',
                'Il campo SKU deve essere compilato'
            )
            return

        if P_AV == "":
            QMessageBox.critical(
                self,
                'Errore',
                'Seleziona un paese'
            )
            return

        lista_articoli = letturaDatabaseArticoli("Model/databaseArticoli.txt")
        sku_exists = any(art['sku'] == SKU_AV for art in lista_articoli)

        if not sku_exists:
            QMessageBox.critical(
                self,
                'Errore',
                f'Lo SKU "{SKU_AV}" non esiste nel database'
            )
            self.sku_av.clear()
            return

        try:
            O = Operazione()
            O.aggiungiVendita(SKU_AV, N_AV, P_AV)

            QMessageBox.information(
                self,
                'Successo',
                f'Vendita aggiunta con successo!\n'
                f'SKU: {SKU_AV}\n'
                f'Quantità: {N_AV}\n'
                f'Paese: {P_AV}'
            )

            self.sku_av.clear()
            self.numero_av.setValue(1)
            self.paese_av.setCurrentIndex(-1)

        except Exception as e:
            QMessageBox.critical(
                self,
                'Errore',
                f'Si è verificato un errore durante l\'aggiunta:\n{str(e)}'
            )

    def modifica_v_(self):
        """ metodo lettura dati in input per la modifica di una vendita"""

        ID_OP = self.id_Vendita.text().strip()
        SKU_MV = self.sku_mv.text().strip()
        QTA_MV = self.numero_mv.value()
        PAESE_MV = self.paese_mv.currentText().strip()

        if not ID_OP:
            QMessageBox.critical(
                self,
                'Errore',
                'Il campo ID Vendita deve essere compilato'
            )
            return

        if not SKU_MV:
            QMessageBox.critical(
                self,
                'Errore',
                'Il campo SKU deve essere compilato'
            )
            return

        if PAESE_MV == "":
            QMessageBox.critical(
                self,
                'Errore',
                'Seleziona un paese'
            )
            return

        try:
            id_vendita = int(ID_OP)
            if id_vendita <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.critical(
                self,
                'Errore',
                'ID Vendita deve essere un numero intero positivo'
            )
            self.id_Vendita.clear()
            return

        lista_articoli = letturaDatabaseArticoli("Model/databaseArticoli.txt")
        sku_exists = any(art['sku'] == SKU_MV for art in lista_articoli)

        if not sku_exists:
            QMessageBox.critical(
                self,
                'Errore',
                f'Lo SKU "{SKU_MV}" non esiste nel database'
            )
            self.sku_mv.clear()
            return

        try:
            OpP = Operazione()
            risultato = OpP.modificaVendita(id_vendita, SKU_MV, QTA_MV, PAESE_MV)

            if risultato is True:
                QMessageBox.critical(
                    self,
                    'Errore',
                    "L'operazione selezionata non è una vendita"
                )
            elif risultato == 'non trovato':
                QMessageBox.critical(
                    self,
                    'Errore',
                    "Nessuna vendita trovata con l'ID specificato"
                )
            else:
                QMessageBox.information(
                    self,
                    'Successo',
                    f'Vendita modificata con successo!\n'
                    f'ID: {id_vendita}\n'
                    f'SKU: {SKU_MV}\n'
                    f'Quantità: {QTA_MV}\n'
                    f'Paese: {PAESE_MV}'
                )
                self.id_Vendita.clear()
                self.sku_mv.clear()
                self.numero_mv.setValue(1)
                self.paese_mv.setCurrentIndex(-1)

        except Exception as e:
            QMessageBox.critical(
                self,
                'Errore',
                f'Si è verificato un errore durante la modifica:\n{str(e)}'
            )