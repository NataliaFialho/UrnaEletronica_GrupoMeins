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
        layout.addWidget(titulo_tela_zeresima)

        self.data_horario_zeresima = QLabel()
        layout.addWidget(self.data_horario_zeresima)

        self.registrar_horario()

        layout.addStretch()
        
        candidatos_zeresima = QLabel("Candidatos:")
        layout.addWidget(candidatos_zeresima)

        layout.addStretch()

        votos_em_branco_zeresima = QLabel("Votos em branco:")
        layout.addWidget(votos_em_branco_zeresima)

        votos_em_nulo_zeresima = QLabel("Votos Nulos:")
        layout.addWidget(votos_em_nulo_zeresima)

        layout.addStretch()

        eleitores_aptos_zeresima = QLabel("Eleitores aptos:")
        layout.addWidget(eleitores_aptos_zeresima)

    def registrar_horario(self):
        horario_zeresima_emitida = QDateTime.currentDateTime()
        horario_formatado = horario_zeresima_emitida.toString("dd/MM/yyyy, HH:mm:ss")
        self.data_horario_zeresima.setText(f"Data e Horário da Emissão: {horario_formatado}")