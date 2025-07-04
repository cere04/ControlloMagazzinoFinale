import numpy as np
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMessageBox, QComboBox, QMenu
from PyQt6.QtCore import pyqtSignal, QObject

from Controllers import operation_service
from entities.articolo import Articolo
from entities.operazione import Operazione, letturaDatabaseArticoli
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Controllers.operation_service import calcolaVenditeTotali, ordinamentoOperazioni, giacenzaMediaMensile, \
    indiceRotazione
from entities.operazione import letturaDatabaseOperazioni

STYLESHEET = """
    /* Main window and general styling */
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

    /* Section header labels */
    QLabel[objectName="label_9"],
    QLabel[objectName="label_8"],
    QLabel[objectName="label_10"],
    QLabel[objectName="label"],
    QLabel[objectName="label_17"],
    QLabel[objectName="label_21"],
    QLabel[objectName="label_28"] {
        font-size: 16px;
        font-weight: 700;
        color: #4a5568;
        padding-bottom: 8px;
    }

    /* Input fields */
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

    /* ComboBox styling */
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

    /* SpinBox styling */
    QSpinBox {
        padding: 8px;
        border: 2px solid #cccccc;
        border-radius: 8px;
        font-size: 14px;
        color: black;
        padding-right: 25px; /* Space for buttons */
    }

    QSpinBox:focus {
        border: 2px solid #3A81F1;
    }

    QSpinBox::up-button, QSpinBox::down-button {
        subcontrol-origin: border;
        subcontrol-position: center right;
        width: 16px;
        background-color: none;
         /* border: 0px solid transparent;*/
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

    /* Button styling */
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

    BarChartCanvas {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #e0e6ed;
        padding: 16px;
    }

    /* Filter bar */
    QFrame#frame_3 {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #e0e6ed;
        padding: 12px;
    }

    /* Horizontal line separator */
    QFrame[objectName="line"] {
        color: #e2e8f0;
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


class adminWindow(QObject):
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.user_data = None
        self.menu_button = None

    def setupUi(self, MainWindow, user_data):
        self.user_data = user_data
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1300, 800))

        MainWindow.setStyleSheet(STYLESHEET)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        # ---------- top bar ----------
        top_bar = QtWidgets.QFrame(parent=self.centralwidget)
        top_bar.setMaximumHeight(45)
        top_bar_layout = QtWidgets.QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(10, 5, 10, 5)
        top_bar_layout.setSpacing(0)

        # ---------- bottone menu ----------
        self.menu_button = QtWidgets.QPushButton(parent=top_bar)
        self.menu_button.setText("☰")
        self.menu_button.setFixedSize(40, 35)
        self.menu_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                color: #0F4C81;
                font-size: 20px;  
                font-weight: bold;
                padding: 0;
            }
            QPushButton:hover {
                color: #1666AA;
                background-color: #e0e6ed;
                border-radius: 4px;
            }
        """)
        self.menu_button.clicked.connect(self.show_user_menu)
        top_bar_layout.addWidget(self.menu_button)

        spacer_top = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        top_bar_layout.addItem(spacer_top)

        self.verticalLayout.addWidget(top_bar)

        # ---------- contenuto principale ----------
        self.main_content = QtWidgets.QWidget(parent=self.centralwidget)
        self.gridLayout = QtWidgets.QGridLayout(self.main_content)
        self.gridLayout.setContentsMargins(10, 0, 10, 10)
        self.gridLayout.setSpacing(10)
        self.verticalLayout.addWidget(self.main_content)

        # ---------- frame sinistro ----------
        self.frame = QtWidgets.QFrame(parent=self.main_content)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.formLayout_2 = QtWidgets.QFormLayout(self.frame)
        self.formLayout_2.setObjectName("formLayout_2")

        # ---------- form aggiunta vendita ----------
        self.label_9 = QtWidgets.QLabel(parent=self.frame)
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.label_9)
        self.label_5 = QtWidgets.QLabel(parent=self.frame)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.lineEdit_5 = QtWidgets.QLineEdit(parent=self.frame)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_5)
        self.label_6 = QtWidgets.QLabel(parent=self.frame)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_6)
        self.spinBox = QtWidgets.QSpinBox(parent=self.frame)
        self.spinBox.setObjectName("spinBox")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spinBox)
        self.label_7 = QtWidgets.QLabel(parent=self.frame)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_7)

        self.paese_av = QComboBox(parent=self.frame)
        self.paese_av.addItem("Italia")
        self.paese_av.addItem("Germania")
        self.paese_av.addItem("Francia")
        self.paese_av.addItem("Spagna")
        self.paese_av.setCurrentIndex(-1)
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.paese_av)

        self.pushButton = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.aggiuntaVendita)
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.formLayout_2.setItem(5, QtWidgets.QFormLayout.ItemRole.SpanningRole, spacerItem)

        # ---------- form aggiunta giacenza ----------
        self.label_8 = QtWidgets.QLabel(parent=self.frame)
        self.label_8.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.label_8)
        self.label_3 = QtWidgets.QLabel(parent=self.frame)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.frame)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_3)
        self.label_4 = QtWidgets.QLabel(parent=self.frame)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.spinBox_2 = QtWidgets.QSpinBox(parent=self.frame)
        self.spinBox_2.setObjectName("spinBox_2")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spinBox_2)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.aggiuntaGiacenza)
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.pushButton_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.formLayout_2.setItem(10, QtWidgets.QFormLayout.ItemRole.SpanningRole, spacerItem1)

        # ---------- form aggiunta articolo ----------
        self.label_10 = QtWidgets.QLabel(parent=self.frame)
        self.label_10.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.formLayout_2.setWidget(11, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.label_10)
        self.label_11 = QtWidgets.QLabel(parent=self.frame)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(12, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_11)
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.frame)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.formLayout_2.setWidget(12, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_4)
        self.label_12 = QtWidgets.QLabel(parent=self.frame)
        self.label_12.setObjectName("label_12")
        self.formLayout_2.setWidget(13, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_12)

        self.genere_art_add = QComboBox(parent=self.frame)
        self.genere_art_add.addItem("uomo")
        self.genere_art_add.addItem("donna")
        self.genere_art_add.setCurrentIndex(-1)
        self.formLayout_2.setWidget(13, QtWidgets.QFormLayout.ItemRole.FieldRole, self.genere_art_add)

        self.label_13 = QtWidgets.QLabel(parent=self.frame)
        self.label_13.setObjectName("label_13")
        self.formLayout_2.setWidget(14, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_13)

        self.tipologia_art_add = QComboBox(parent=self.frame)
        self.tipologia_art_add.addItem("calzatura")
        self.tipologia_art_add.addItem("borsa")
        self.tipologia_art_add.addItem("abbigliamento")
        self.tipologia_art_add.setCurrentIndex(-1)
        self.formLayout_2.setWidget(14, QtWidgets.QFormLayout.ItemRole.FieldRole, self.tipologia_art_add)

        self.pushButton_3 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.aggiuntaArticolo)
        self.formLayout_2.setWidget(15, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.pushButton_3)

        # ---------- form eliminazione articolo ----------
        spacerItem5 = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.formLayout_2.setItem(16, QtWidgets.QFormLayout.ItemRole.SpanningRole, spacerItem5)
        self.label_28 = QtWidgets.QLabel(parent=self.frame)
        self.label_28.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_28.setObjectName("label_28")
        self.formLayout_2.setWidget(17, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.label_28)
        self.label_29 = QtWidgets.QLabel(parent=self.frame)
        self.label_29.setObjectName("label_29")
        self.formLayout_2.setWidget(18, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_29)
        self.lineEdit_18 = QtWidgets.QLineEdit(parent=self.frame)
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.formLayout_2.setWidget(18, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_18)
        self.pushButton_7 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.eliminaArticolo)
        self.formLayout_2.setWidget(19, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.pushButton_7)

        self.gridLayout.addWidget(self.frame, 1, 2, 3, 1)

        # ---------- frame destro ----------
        self.frame_2 = QtWidgets.QFrame(parent=self.main_content)
        self.frame_2.setStyleSheet("QFrame#frame {\n"
                                   "    background-color: #ffffff;\\n\n"
                                   "    border-radius: 12px;\\n\n"
                                   "    border: 1px solid #e0e6ed;\\n\n"
                                   "    padding: 16px;\\n\n"
                                   "    box-shadow: 0 4px 12px rgba(0,0,0,0.05);\n"
                                   "}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.formLayout = QtWidgets.QFormLayout(self.frame_2)
        self.formLayout.setObjectName("formLayout")

        # ---------- form modifica vendita ----------
        self.label = QtWidgets.QLabel(parent=self.frame_2)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.label)
        self.label_15 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_15.setObjectName("label_15")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_15)
        self.lineEdit_9 = QtWidgets.QLineEdit(parent=self.frame_2)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_9)
        self.label_2 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(parent=self.frame_2)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit)
        self.label_14 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_14.setObjectName("label_14")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_14)
        self.spinBox_3 = QtWidgets.QSpinBox(parent=self.frame_2)
        self.spinBox_3.setObjectName("spinBox_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spinBox_3)
        self.label_16 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_16.setObjectName("label_16")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_16)

        self.paese_vendita_edit = QComboBox(parent=self.frame_2)
        self.paese_vendita_edit.addItem("Italia")
        self.paese_vendita_edit.addItem("Germania")
        self.paese_vendita_edit.addItem("Francia")
        self.paese_vendita_edit.addItem("Spagna")
        self.paese_vendita_edit.setCurrentIndex(-1)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.paese_vendita_edit)

        self.pushButton_4 = QtWidgets.QPushButton(parent=self.frame_2)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.modificaVendita)
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.pushButton_4)
        spacerItem2 = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.formLayout.setItem(6, QtWidgets.QFormLayout.ItemRole.SpanningRole, spacerItem2)

        # ---------- form modifica giacenza ----------
        self.label_17 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_17.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.label_17)
        self.label_18 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_18.setObjectName("label_18")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_18)
        self.lineEdit_11 = QtWidgets.QLineEdit(parent=self.frame_2)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_11)
        self.label_19 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_19.setObjectName("label_19")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_19)
        self.lineEdit_12 = QtWidgets.QLineEdit(parent=self.frame_2)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_12)
        self.label_20 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_20.setObjectName("label_20")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_20)
        self.spinBox_4 = QtWidgets.QSpinBox(parent=self.frame_2)
        self.spinBox_4.setObjectName("spinBox_4")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spinBox_4)
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.frame_2)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.modificaGiacenza)
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.pushButton_5)
        spacerItem3 = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.formLayout.setItem(12, QtWidgets.QFormLayout.ItemRole.SpanningRole, spacerItem3)

        # ---------- form modifica articolo ----------
        self.label_21 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_21.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.label_21)
        self.label_22 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_22.setObjectName("label_22")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_22)
        self.lineEdit_14 = QtWidgets.QLineEdit(parent=self.frame_2)
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_14)
        self.label_23 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_23.setObjectName("label_23")
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_23)

        self.genere_art_edit = QComboBox(parent=self.frame_2)
        self.genere_art_edit.addItem("uomo")
        self.genere_art_edit.addItem("donna")
        self.genere_art_edit.setCurrentIndex(-1)
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.ItemRole.FieldRole, self.genere_art_edit)

        self.label_24 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_24.setObjectName("label_24")
        self.formLayout.setWidget(16, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_24)

        self.tipologia_art_edit = QComboBox(parent=self.frame_2)
        self.tipologia_art_edit.addItem("calzatura")
        self.tipologia_art_edit.addItem("borsa")
        self.tipologia_art_edit.addItem("abbigliamento")
        self.tipologia_art_edit.setCurrentIndex(-1)
        self.formLayout.setWidget(16, QtWidgets.QFormLayout.ItemRole.FieldRole, self.tipologia_art_edit)

        self.pushButton_6 = QtWidgets.QPushButton(parent=self.frame_2)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.modificaArticolo)
        self.formLayout.setWidget(17, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.pushButton_6)
        spacerItem4 = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.formLayout.setItem(18, QtWidgets.QFormLayout.ItemRole.SpanningRole, spacerItem4)

        self.gridLayout.addWidget(self.frame_2, 1, 3, 3, 1)

        # ---------- frame visualizzazione grafico ----------
        self.widget = QtWidgets.QWidget(parent=self.main_content)
        self.widget.setMinimumSize(QtCore.QSize(0, 0))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # ---------- filtri ----------
        self.frame_3 = QtWidgets.QFrame(parent=self.widget)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.setMinimumSize(16777215, 100)
        self.frame_3.setMaximumSize(16777215, 100)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setContentsMargins(10, 5, 10, 5)  # Padding ridotto
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.label_25 = QtWidgets.QLabel(parent=self.frame_3)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout.addWidget(self.label_25)

        self.comboBox = QtWidgets.QComboBox(parent=self.frame_3)
        self.comboBox.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem(" ")
        self.comboBox.addItem("uomo")
        self.comboBox.addItem("donna")
        self.horizontalLayout.addWidget(self.comboBox)

        self.label_26 = QtWidgets.QLabel(parent=self.frame_3)
        self.label_26.setObjectName("label_26")
        self.horizontalLayout.addWidget(self.label_26)

        self.comboBox_2 = QtWidgets.QComboBox(parent=self.frame_3)
        self.comboBox_2.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBox_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem(" ")
        self.comboBox_2.addItem("calzatura")
        self.comboBox_2.addItem("borsa")
        self.comboBox_2.addItem("abbigliamento")
        self.horizontalLayout.addWidget(self.comboBox_2)

        self.label_27 = QtWidgets.QLabel(parent=self.frame_3)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout.addWidget(self.label_27)

        self.lineEdit_17 = QtWidgets.QLineEdit(parent=self.frame_3)
        self.lineEdit_17.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_17.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.horizontalLayout.addWidget(self.lineEdit_17)

        self.label_30 = QtWidgets.QLabel(parent=self.frame_3)
        self.label_30.setObjectName("label_30")
        self.horizontalLayout.addWidget(self.label_30)

        self.comboBox_3 = QtWidgets.QComboBox(parent=self.frame_3)
        self.comboBox_3.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBox_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem(" ")
        self.comboBox_3.addItem("Italia")
        self.comboBox_3.addItem("Germania")
        self.comboBox_3.addItem("Francia")
        self.comboBox_3.addItem("Spagna")
        self.horizontalLayout.addWidget(self.comboBox_3)

        self.pushButton_8 = QtWidgets.QPushButton(parent=self.frame_3)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(self.applicaFiltri)
        self.horizontalLayout.addWidget(self.pushButton_8)

        self.btn_reset = QtWidgets.QPushButton(parent=self.frame_3)
        self.btn_reset.setObjectName("btn_reset")
        self.btn_reset.setText("Reset")
        self.btn_reset.clicked.connect(self.reset_filtri)
        self.horizontalLayout.addWidget(self.btn_reset)

        self.gridLayout_2.addWidget(self.frame_3, 0, 1, 1, 1)

        # ---------- grafico ----------
        self.graphicsView = BarChartCanvas(self.widget)
        self.graphicsView.setMaximumSize(QtCore.QSize(16777215, 700))
        self.graphicsView.setStyleSheet("none")
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 1, 1, 1, 1)

        self.gridLayout.addWidget(self.widget, 1, 0, 3, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1193, 22))
        self.menubar.setObjectName("menubar")
        self.menuControlloMagazzino = QtWidgets.QMenu(parent=self.menubar)
        self.menuControlloMagazzino.setObjectName("menuControlloMagazzino")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuControlloMagazzino.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def show_user_menu(self):
        """metodo per la visualizzazione dei dati utente nel menu a tendina"""

        menu = QMenu(self.centralwidget)
        menu.setStyleSheet("""
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

        nome_completo = QAction(f"Nome: {self.user_data['nome']} {self.user_data['cognome']}", self.centralwidget)
        nome_completo.setEnabled(False)
        menu.addAction(nome_completo)

        ruolo = QAction(f"Ruolo: {self.user_data['ruolo']}", self.centralwidget)
        ruolo.setEnabled(False)
        menu.addAction(ruolo)

        user_id = QAction(f"ID: {self.user_data['codice']}", self.centralwidget)
        user_id.setEnabled(False)
        menu.addAction(user_id)

        menu.addSeparator()

        # ---------- logout button ----------
        logout_action = QAction("Logout", self.centralwidget)
        logout_action.triggered.connect(self.logout)
        menu.addAction(logout_action)

        menu.exec(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))

    def logout(self):
        """metodo per il logout"""

        self.logout_requested.emit()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pannello Amministratore"))
        self.label_9.setText(_translate("MainWindow", "Aggiungi Vendita"))
        self.label_5.setText(_translate("MainWindow", "SKU"))
        self.label_6.setText(_translate("MainWindow", "Quantità"))
        self.label_7.setText(_translate("MainWindow", "Paese"))
        self.pushButton.setText(_translate("MainWindow", "Conferma Operazione"))
        self.label_8.setText(_translate("MainWindow", "Aggiungi Giacenza"))
        self.label_3.setText(_translate("MainWindow", "SKU"))
        self.label_4.setText(_translate("MainWindow", "Quantità"))
        self.pushButton_2.setText(_translate("MainWindow", "Conferma Operazione"))
        self.label_10.setText(_translate("MainWindow", "Aggiungi Articolo"))
        self.label_11.setText(_translate("MainWindow", "SKU"))
        self.label_12.setText(_translate("MainWindow", "Genere"))
        self.label_13.setText(_translate("MainWindow", "Tipologia"))
        self.pushButton_3.setText(_translate("MainWindow", "Conferma Operazione"))
        self.label_28.setText(_translate("MainWindow", "Elimina Articolo"))
        self.label_29.setText(_translate("MainWindow", "SKU"))
        self.pushButton_7.setText(_translate("MainWindow", "Conferma Operazione"))
        self.label.setText(_translate("MainWindow", "Modifica Vendita"))
        self.label_15.setText(_translate("MainWindow", "ID Operazione"))
        self.label_2.setText(_translate("MainWindow", "SKU"))
        self.label_14.setText(_translate("MainWindow", "Quantità"))
        self.label_16.setText(_translate("MainWindow", "Paese"))
        self.pushButton_4.setText(_translate("MainWindow", "Modifica"))
        self.label_17.setText(_translate("MainWindow", "Modifica Giacenza"))
        self.label_18.setText(_translate("MainWindow", "ID Operazione"))
        self.label_19.setText(_translate("MainWindow", "SKU"))
        self.label_20.setText(_translate("MainWindow", "Quantità"))
        self.pushButton_5.setText(_translate("MainWindow", "Modifica"))
        self.label_21.setText(_translate("MainWindow", "Modifica Articolo"))
        self.label_22.setText(_translate("MainWindow", "SKU"))
        self.label_23.setText(_translate("MainWindow", "Genere"))
        self.label_24.setText(_translate("MainWindow", "Tipologia"))
        self.pushButton_6.setText(_translate("MainWindow", "Modifica"))
        self.label_25.setText(_translate("MainWindow", "Genere"))
        self.label_26.setText(_translate("MainWindow", "Tipologia"))
        self.label_27.setText(_translate("MainWindow", "SKU"))
        self.label_30.setText(_translate("MainWindow", "Paese"))
        self.pushButton_8.setText(_translate("MainWindow", "Applica Filtri"))
        self.menuControlloMagazzino.setTitle(_translate("MainWindow", "ControlloMagazzino"))
        self.menuControlloMagazzino.menuAction().setVisible(False)

    def reset_filtri(self):
        """Resetta tutti i campi di filtro e ripristina il grafico originale"""
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)

        self.lineEdit_17.clear()

        self.graphicsView.plot_data()

    def aggiuntaVendita(self):
        """ metodo lettura dati in input per l'aggiunta di una vendita"""

        SKU_AV = self.lineEdit_5.text()
        N_AV = self.spinBox.value()
        P_AV = self.paese_av.currentText()

        if SKU_AV == '' or P_AV == '':
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'Tutti i campi devono essere compilati'
            )
            return

        if N_AV <= 0:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'La quantità deve essere maggiore di zero'
            )
            return

        lista_articoli = letturaDatabaseArticoli("Model/databaseArticoli.txt")
        sku_exists = any(art['sku'] == SKU_AV for art in lista_articoli)

        if not sku_exists:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'SKU non esistente'
            )
            return

        try:
            O = Operazione()
            O.aggiungiVendita(SKU_AV, N_AV, P_AV)
            QMessageBox.information(
                self.centralwidget,
                'Successo',
                'Vendita aggiunta con successo'
            )
            self.lineEdit_5.clear()
            self.spinBox.setValue(0)
            self.paese_av.setCurrentIndex(-1)
        except Exception as e:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                f'Errore durante l\'aggiunta: {str(e)}'
            )

    def aggiuntaGiacenza(self):
        """ metodo lettura dati in input per l'aggiunta di una giacenza"""

        SKU_AG = self.lineEdit_3.text()
        N_AG = self.spinBox_2.value()

        if SKU_AG == '':
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'Il campo SKU è obbligatorio'
            )
            return

        if N_AG <= 0:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'La quantità deve essere maggiore di zero'
            )
            return

        lista_articoli = letturaDatabaseArticoli("Model/databaseArticoli.txt")
        sku_exists = any(art['sku'] == SKU_AG for art in lista_articoli)

        if not sku_exists:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'SKU non esistente'
            )
            return

        try:
            O = Operazione()
            O.aggiungiGiacenza(SKU_AG, N_AG)
            QMessageBox.information(
                self.centralwidget,
                'Successo',
                'Giacenza aggiunta con successo'
            )
            self.lineEdit_3.clear()
            self.spinBox_2.setValue(0)
        except Exception as e:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                f'Errore durante l\'aggiunta: {str(e)}'
            )

    def aggiuntaArticolo(self):
        """ metodo lettura dati in input per l'aggiunta di un articolo"""

        SKU_ART = self.lineEdit_4.text()
        GENERE_ART = self.genere_art_add.currentText()
        TIPO_ART = self.tipologia_art_add.currentText()

        if not all([SKU_ART, GENERE_ART, TIPO_ART]):
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'Tutti i campi devono essere compilati'
            )
            return

        if GENERE_ART.lower() not in ["uomo", "donna"]:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'Genere non valido. Valori accettati: "uomo" o "donna"'
            )
            return

        tipologie_valide = ["calzatura", "borsa", "abbigliamento"]
        if TIPO_ART.lower() not in tipologie_valide:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                f'Tipologia non valida. Valori accettati: {", ".join(tipologie_valide)}'
            )
            return

        lista_articoli = letturaDatabaseArticoli("Model/databaseArticoli.txt")
        sku_exists = any(art['sku'] == SKU_ART for art in lista_articoli)

        if sku_exists:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'SKU già esistente'
            )
            return

        try:
            A = Articolo(SKU_ART, GENERE_ART, TIPO_ART)
            A.aggiungiArticolo()
            QMessageBox.information(
                self.centralwidget,
                'Successo',
                'Articolo aggiunto con successo'
            )
            self.lineEdit_4.clear()
            self.genere_art_add.setCurrentIndex(-1)
            self.tipologia_art_add.setCurrentIndex(-1)
        except Exception as e:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                f'Errore durante l\'aggiunta: {str(e)}'
            )

    def modificaVendita(self):
        """ metodo lettura dati in input per la modifica di una vendita"""

        ID_OP = self.lineEdit_9.text()
        SKU_MV = self.lineEdit.text()
        QTA_MV = self.spinBox_3.value()
        PAESE_MV = self.paese_vendita_edit.currentText()

        if not ID_OP or not SKU_MV:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'ID Operazione e SKU sono campi obbligatori'
            )
            return

        if QTA_MV <= 0:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'La quantità deve essere maggiore di zero'
            )
            return

        lista_articoli = letturaDatabaseArticoli("Model/databaseArticoli.txt")
        sku_exists = any(art['sku'] == SKU_MV for art in lista_articoli)

        if not sku_exists:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'SKU non esistente'
            )
            return

        try:
            ID_OP = int(ID_OP)
            OpP = Operazione()
            result = OpP.modificaVendita(ID_OP, SKU_MV, QTA_MV, PAESE_MV)

            if result is True:
                QMessageBox.critical(
                    self.centralwidget,
                    'Errore',
                    "L'operazione selezionata non è una vendita"
                )
            elif result == 'non trovato':
                QMessageBox.critical(
                    self.centralwidget,
                    'Errore',
                    "Operazione non trovata"
                )
            else:
                QMessageBox.information(
                    self.centralwidget,
                    'Successo',
                    'Vendita modificata con successo'
                )
                self.lineEdit_9.clear()
                self.lineEdit.clear()
                self.spinBox_3.setValue(0)
                self.paese_vendita_edit.setCurrentIndex(-1)

        except ValueError:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                "ID Operazione deve essere un numero intero"
            )
        except Exception as e:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                f'Errore durante la modifica: {str(e)}'
            )

    def modificaGiacenza(self):
        """ metodo lettura dati in input per la modifica di una giacenza"""

        ID_OP = self.lineEdit_11.text()
        SKU_MG = self.lineEdit_12.text()
        QTA_MG = self.spinBox_4.value()

        if not ID_OP or not SKU_MG:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'ID Operazione e SKU sono campi obbligatori'
            )
            return

        if QTA_MG <= 0:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'La quantità deve essere maggiore di zero'
            )
            return

        lista_articoli = letturaDatabaseArticoli("Model/databaseArticoli.txt")
        sku_exists = any(art['sku'] == SKU_MG for art in lista_articoli)

        if not sku_exists:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'SKU non esistente'
            )
            return

        try:
            ID_OP = int(ID_OP)
            Opp = Operazione()
            result = Opp.modificaGiacenza(ID_OP, SKU_MG, QTA_MG, None)

            if result is True:
                QMessageBox.critical(
                    self.centralwidget,
                    'Errore',
                    "L'operazione selezionata non è una giacenza"
                )
            elif result == 'Errore':
                QMessageBox.critical(
                    self.centralwidget,
                    'Errore',
                    "Operazione non trovata"
                )
            else:
                QMessageBox.information(
                    self.centralwidget,
                    'Successo',
                    'Giacenza modificata con successo'
                )
                self.lineEdit_11.clear()
                self.lineEdit_12.clear()
                self.spinBox_4.setValue(0)

        except ValueError:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                "ID Operazione deve essere un numero intero"
            )
        except Exception as e:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                f'Errore durante la modifica: {str(e)}'
            )

    def modificaArticolo(self):
        """ metodo lettura dati in input per la modifica di un articolo"""

        SKU_ART = self.lineEdit_14.text()
        GENERE_SKU = self.genere_art_edit.currentText()
        TIPO_ART = self.tipologia_art_edit.currentText()

        if not all([SKU_ART, GENERE_SKU, TIPO_ART]):
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'Tutti i campi devono essere compilati'
            )
            return

        lista_articoli = letturaDatabaseArticoli("Model/databaseArticoli.txt")
        sku_exists = any(art['sku'] == SKU_ART for art in lista_articoli)

        if not sku_exists:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'SKU non esistente'
            )
            return

        if GENERE_SKU.lower() not in ["uomo", "donna"]:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'Genere non valido. Valori accettati: "uomo" o "donna"'
            )
            return

        tipologie_valide = ["calzatura", "borsa", "abbigliamento"]
        if TIPO_ART.lower() not in tipologie_valide:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                f'Tipologia non valida. Valori accettati: {", ".join(tipologie_valide)}'
            )
            return

        try:
            a = Articolo()
            t = a.modificaArticolo(SKU_ART, GENERE_SKU, TIPO_ART)
            QMessageBox.information(
                self.centralwidget,
                'Successo',
                'Articolo modificato con successo'
            )
            self.lineEdit_14.clear()
            self.genere_art_edit.setCurrentIndex(-1)
            self.tipologia_art_edit.setCurrentIndex(-1)
        except Exception as e:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                f'Errore durante la modifica: {str(e)}'
            )

    def eliminaArticolo(self):
        """ metodo lettura dati in input per l'eliminazione di un articolo"""

        SKU_ART = self.lineEdit_18.text()

        if not SKU_ART:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'Il campo SKU è obbligatorio'
            )
            return

        lista_articoli = letturaDatabaseArticoli("Model/databaseArticoli.txt")
        sku_exists = any(art['sku'] == SKU_ART for art in lista_articoli)

        if not sku_exists:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                'SKU non esistente'
            )
            return

        try:
            confirm = QMessageBox.question(
                self.centralwidget,
                'Conferma eliminazione',
                f'Sei sicuro di voler eliminare l\'articolo con SKU {SKU_ART}?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm == QMessageBox.StandardButton.Yes:
                A = Articolo()
                A.eliminaArticolo(SKU_ART)
                QMessageBox.information(
                    self.centralwidget,
                    'Successo',
                    'Articolo eliminato con successo'
                )
                self.lineEdit_18.clear()
        except Exception as e:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                f'Errore durante l\'eliminazione: {str(e)}'
            )

    def applicaFiltri(self):
        """ metodo lettura dati in input dei filtri desiderati"""

        try:
            lista_operazioni = letturaDatabaseOperazioni("Model/databaseOperazioni.txt")
            lista_articoli = letturaDatabaseArticoli("Model/databaseArticoli.txt")

            operazioniFiltrate = operation_service.filtraOperazioni(
                lista_operazioni,
                lista_articoli,
                [self.lineEdit_17.text()],
                [self.comboBox.currentText()],
                [self.comboBox_2.currentText()],
                [self.comboBox_3.currentText()]
            )

            if not operazioniFiltrate:
                QMessageBox.information(
                    self.centralwidget,
                    'Nessun risultato',
                    'Nessuna operazione trovata con i filtri selezionati'
                )
            else:
                self.graphicsView.update_data(operazioniFiltrate)

        except Exception as e:
            QMessageBox.critical(
                self.centralwidget,
                'Errore',
                f'Errore durante l\'applicazione dei filtri: {str(e)}'
            )


class BarChartCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(10, 4), tight_layout=True)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

        if parent:
            self.setParent(parent)

        self.setStyleSheet("""
            background-color: transparent;
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
        self.draw()

    def update_data(self, lista_operazioni):
        """metodo per l'aggiornamento dei valori del grafico una volta applicati i filtri"""

        vendite = calcolaVenditeTotali(lista_operazioni)
        giacenze = [giacenzaMediaMensile(ordinamentoOperazioni(lista_operazioni, i + 1), i + 1) for i in range(12)]
        self.plot_data(vendite, giacenze)