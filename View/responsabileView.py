from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QComboBox, QLineEdit, QPushButton, QHBoxLayout, \
    QMessageBox, QSizePolicy, QMenu, QSpacerItem
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from Controllers.operation_service import calcolaVenditeTotali, ordinamentoOperazioni, giacenzaMediaMensile, indiceRotazione
from entities.operazione import letturaDatabaseOperazioni, letturaDatabaseArticoli
import Controllers.operation_service as operation_service

STYLESHEET = """
    /* Main window and general styling */
    QWidget {
        background-color: #f5f7fa;
        font-family: Arial, sans-serif;
        color: #000000;
    }

    QLabel {
        color: #2d3748;
        background: transparent;
    }

    /* Filter bar */
    QFrame#filterFrame {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #e0e6ed;
        padding: 8px;
        margin-bottom: 10px;
        max-height: 60px;
    }

    /* Input fields */
    QLineEdit {
        padding: 6px;
        border: 2px solid #cccccc;
        border-radius: 6px;
        font-size: 13px;
        color: black;
        min-width: 80px;
    }
    QLineEdit:focus {
        border: 2px solid #3A81F1;
    }

    /* ComboBox styling */
    QComboBox {
        padding: 6px;
        border: 2px solid #cccccc;
        border-radius: 6px;
        font-size: 13px;
        color: black;
        min-width: 80px;
    }
    QComboBox:focus {
        border: 2px solid #3A81F1;
    }

    QComboBox QAbstractItemView {
        border: 2px solid #cccccc;
        border-radius: 8px;
        padding: 4px;
        background: white;
        selection-background-color: #0F4C81;
        selection-color: white;
    }

    /* Button styling */
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

    /* Menu styling */
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
"""


class BarChartCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(10, 5), tight_layout=True)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

        if parent:
            self.setParent(parent)

        self.setStyleSheet("""
            background-color: white;
            border-radius: 12px;
            border: 1px solid #e0e6ed;
        """)

        self.plot_data()

    def plot_data(self, vendite=None, giacenze=None):
        mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]

        if vendite is None or giacenze is None:
            lista_operazioni = letturaDatabaseOperazioni("Model/databaseOperazioni.txt")
            vendite = calcolaVenditeTotali(lista_operazioni)
            giacenze = [giacenzaMediaMensile(ordinamentoOperazioni(lista_operazioni, i + 1), i + 1) for i in range(12)]

        max_vendite = max(vendite) if vendite else 1
        rotazione = indiceRotazione(vendite, giacenze)
        rotazione_multiplo = [val * (max_vendite / 10) for val in rotazione]

        x = np.arange(len(mesi))
        width = 0.35

        self.axes.clear()
        self.axes.bar(x - width / 2, vendite, width, label='Vendite Totali', color='#455C75')
        self.axes.bar(x + width / 2, giacenze, width, label='Giacenza Media', color='#E0BC47')
        self.axes.plot(x, rotazione_multiplo, color='black', marker='o', label='Indice Rotazione', linewidth=2)

        for i, val in enumerate(rotazione):
            self.axes.annotate(
                f'{val:.2f}',
                (x[i], rotazione_multiplo[i]),
                textcoords="offset points",
                xytext=(0, 10),
                ha='center',
                fontsize=8,
                color='black'
            )

        self.axes.set_xticks(x)
        self.axes.set_xticklabels(mesi, fontsize=10)
        self.axes.set_ylabel('Quantità', fontsize=11)
        self.axes.set_title('Andamento Mensile Vendite e Giacenza', fontsize=12, weight='bold')
        self.axes.legend()
        self.axes.grid(axis='y', linestyle='--', alpha=0.3)
        self.fig.tight_layout()
        self.draw()

    def update_data(self, lista_operazioni):
        vendite = calcolaVenditeTotali(lista_operazioni)
        giacenze = [giacenzaMediaMensile(ordinamentoOperazioni(lista_operazioni, i + 1), i + 1) for i in range(12)]
        self.plot_data(vendite, giacenze)


class FinestraRC(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.setStyleSheet(STYLESHEET)
        self.setWindowTitle("Responsabile Commerciale")
        self.resize(1200, 800)

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
        self.menu_button.setFixedSize(40, 35)  # Dimensioni leggermente ridotte
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

        # ---------- barra filtri ----------
        filter_frame = QFrame()
        filter_frame.setObjectName("filterFrame")
        filter_frame.setMaximumHeight(60)
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(10, 5, 10, 5)
        filter_layout.setSpacing(10)

        label_genere = QLabel("Genere:")
        filter_layout.addWidget(label_genere)

        self.comboBox_genere = QComboBox()
        self.comboBox_genere.addItem(" ")
        self.comboBox_genere.addItem("uomo")
        self.comboBox_genere.addItem("donna")
        filter_layout.addWidget(self.comboBox_genere)

        label_tipologia = QLabel("Tipologia:")
        filter_layout.addWidget(label_tipologia)

        self.comboBox_tipologia = QComboBox()
        self.comboBox_tipologia.addItem(" ")
        self.comboBox_tipologia.addItem("calzatura")
        self.comboBox_tipologia.addItem("borsa")
        self.comboBox_tipologia.addItem("abbigliamento")
        filter_layout.addWidget(self.comboBox_tipologia)

        label_sku = QLabel("SKU:")
        filter_layout.addWidget(label_sku)

        self.lineEdit_sku = QLineEdit()
        self.lineEdit_sku.setMinimumWidth(80)
        filter_layout.addWidget(self.lineEdit_sku)

        label_paese = QLabel("Paese:")
        filter_layout.addWidget(label_paese)

        self.comboBox_paese = QComboBox()
        self.comboBox_paese.addItem(" ")
        self.comboBox_paese.addItem("Italia")
        self.comboBox_paese.addItem("Germania")
        self.comboBox_paese.addItem("Francia")
        self.comboBox_paese.addItem("Spagna")
        filter_layout.addWidget(self.comboBox_paese)

        btn_apply = QPushButton("Applica Filtri")
        btn_apply.clicked.connect(self.applicaFiltri)
        filter_layout.addWidget(btn_apply)

        btn_reset = QPushButton("Reset")
        btn_reset.clicked.connect(self.reset_filtri)
        filter_layout.addWidget(btn_reset)

        main_layout.addWidget(filter_frame)

        self.chart = BarChartCanvas()
        self.chart.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(self.chart, 1)  # Fattore di espansione = 1

        self.show()

    def reset_filtri(self):
        """metodo per il reset dei valori del grafico"""

        self.comboBox_genere.setCurrentIndex(0)
        self.comboBox_tipologia.setCurrentIndex(0)
        self.comboBox_paese.setCurrentIndex(0)

        self.lineEdit_sku.clear()

        self.chart.plot_data()

    def show_user_menu(self):
        menu = QMenu()

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

        menu.setStyleSheet(STYLESHEET)

        menu.exec(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))

    def logout(self):
        """metodo per il logout"""

        self.logout_requested.emit()
        self.close()

    def applicaFiltri(self):
        """ metodo lettura dati in input dei filtri desiderati"""

        try:
            lista_operazioni = letturaDatabaseOperazioni("Model/databaseOperazioni.txt")
            lista_articoli = letturaDatabaseArticoli("Model/databaseArticoli.txt")

            operazioniFiltrate = operation_service.filtraOperazioni(
                lista_operazioni,
                lista_articoli,
                [self.lineEdit_sku.text()],
                [self.comboBox_genere.currentText()],
                [self.comboBox_tipologia.currentText()],
                [self.comboBox_paese.currentText()]
            )

            if not operazioniFiltrate:
                QMessageBox.information(
                    self,
                    'Nessun risultato',
                    'Nessuna operazione trovata con i filtri selezionati'
                )
            else:
                self.chart.update_data(operazioniFiltrate)

        except Exception as e:
            QMessageBox.critical(
                self,
                'Errore',
                f'Errore durante l\'applicazione dei filtri: {str(e)}'
            )