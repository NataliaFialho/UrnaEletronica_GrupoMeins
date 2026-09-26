import sys, os

from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QFont, QColor, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFrame,
)

class TelaZeresima(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(800, 500)
        self.setWindowTitle("Relatório Inicial (Zerésima)")

        layout = QVBoxLayout(self)
        layout.setSpacing(1)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(25, 25, 25, 25)

        titulo_tela_zeresima = QLabel("ZERÉSIMA")
        titulo_tela_zeresima.setObjectName("zeresima_titulo")
        layout.addWidget(titulo_tela_zeresima)

        self.data_horario_zeresima = QLabel()
        self.data_horario_zeresima.setObjectName("zeresima_data")
        layout.addWidget(self.data_horario_zeresima)

        self.registrar_horario()

        info_zeresima = QWidget()
        info_zeresima.setObjectName("info_zeresima")
        layout_info = QVBoxLayout(info_zeresima)
        layout_info.setSpacing(1)
        layout_info.setAlignment(Qt.AlignTop)
        layout_info.setContentsMargins(25, 25, 25, 25)
        
        candidatos_zeresima = QLabel("Candidatos:")
        layout_info.addWidget(candidatos_zeresima)

        layout_info.addStretch()

        votos_em_branco_zeresima = QLabel("Votos em branco:")
        layout_info.addWidget(votos_em_branco_zeresima)

        votos_em_nulo_zeresima = QLabel("Votos Nulos:")
        layout_info.addWidget(votos_em_nulo_zeresima)

        layout_info.addStretch()

        eleitores_aptos_zeresima = QLabel("Eleitores aptos:")
        layout_info.addWidget(eleitores_aptos_zeresima)

        layout.addWidget(info_zeresima)

        ESTILO_MENU = """

            QWidget {
                font-family: Arial;
                font-size: 16px;
            }

            #info_zeresima {
                border-width: 1px;
                border-style: solid;
                border-color: black;
                border-radius: 5px;
            }

            #tela_menu {
                background-color:  #FFFFFF;
            }

            #zeresima_titulo {
                color: #000000;
                font-size: 36px;
                font-weight: bold;
            }

            #zeresima_data {
                color: #000000;
                font-size: 13px;
                font-weight: bold;
                padding-top: 6px;
                padding-bottom: 10px;
            }

            #menu_rodape {
                color: #4d5a75;
                font-size: 12px;
            }

            #menu_botao {
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #2c3648;
                border-radius: 10px;
                font-size: 18px;
                font-weight: 600;
                text-align: left;
                padding-left: 26px;
            }

            #menu_botao:hover {
                background-color: #F8F8FF;
                border-color: #3d4a63;
            }

        """

        self.setStyleSheet(ESTILO_MENU)

    def registrar_horario(self):
        horario_zeresima_emitida = QDateTime.currentDateTime()
        horario_formatado = horario_zeresima_emitida.toString("dd/MM/yyyy, HH:mm:ss")
        self.data_horario_zeresima.setText(f"Data e Horário da Emissão: {horario_formatado}")