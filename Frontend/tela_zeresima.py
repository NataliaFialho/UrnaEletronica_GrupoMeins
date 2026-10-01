import os, sys

from PySide6.QtCore import Qt, QDateTime, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from Backend.urna_backend import UrnaBackend, urna_backend

class TelaZeresima(QWidget):
    zeresima_confirmada = Signal()
    zeresima_cancelada = Signal()

    def __init__(self, backend: UrnaBackend = urna_backend, parent=None):
        super().__init__(parent)
        self.backend = backend

        raiz_projeto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icone = os.path.join(raiz_projeto, "Imagens", "icone_zeresima_preto.png")
        self.setFixedSize(800, 500)
        self.setWindowTitle("Relatório Inicial (Zerésima)")
        self.setWindowIcon(QIcon(icone))
        self.setStyleSheet("""
            QWidget {
                    font-family: Arial; 
                    font-size: 16px; 
                    background: #F4F8FB;
                }
                
                QLabel {
                    background-color: white;
                }

                QLabel#titulo {
                    background-color: transparent;
                    color: #283A50;
                    font-size: 34px;
                    font-weight: bold;
                }

                QLabel#data {
                    background-color: transparent;
                    color: #283A50;
                    font-size: 13px;
                    font-weight: bold;
                }

                #info_zerezima {
                    padding: 10px;
                    border-style: solid;
                    border-width: 0.5px;
                    border-color: #283A50;
                }    

                QPushButton {
                    height: 30px;
                    background: #FFFFFF;
                    color: #283A50;
                    border: 1px solid #C0CCD6;
                    border-radius: 10px;
                    font-size: 17px;
                    font-weight: 600;
                    text-align: center;
                    padding-left: 24px;
                }

                QPushButton:hover:enabled {
                    background: #b6c1d1;
                }

                QPushButton:disabled {
                    background: #e4e4e4;
                    color: #888;
                    border-color: #bbb;
                }
            """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(10)

        self.titulo = QLabel("ZERÉSIMA")
        self.titulo.setObjectName("titulo")
        self.titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.titulo)

        self.data_horario = QLabel()
        self.data_horario.setObjectName("data")
        layout.addWidget(self.data_horario)

        self.conteudo = QLabel()
        self.conteudo.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.conteudo.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.conteudo.setWordWrap(True)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.conteudo)
        layout.addWidget(scroll, 1)

        botoes = QVBoxLayout()
        botao_voltar = QPushButton("Voltar ao Menu")
        botao_voltar.clicked.connect(lambda checked=False: self.zeresima_cancelada.emit())
        botoes.addWidget(botao_voltar)

        self.botao_confirmar = QPushButton("Confirmar zerésima e iniciar votação")
        self.botao_confirmar.clicked.connect(lambda checked=False: self.zeresima_confirmada.emit())
        botoes.addWidget(self.botao_confirmar)
        layout.addLayout(botoes)

        self.atualizar_dados()

    def atualizar_dados(self):
        agora = QDateTime.currentDateTime().toString("dd/MM/yyyy, HH:mm:ss")
        self.data_horario.setText(f"Data e horário da emissão: {agora}")
        boletim = self.backend.boletim_atual()
        candidatos = "\n".join(
            f"{codigo} - {self.backend.candidatos[codigo]['nome']} "
            f"({self.backend.candidatos[codigo]['partido']}) - Votos: {votos}"
            for codigo, votos in boletim.votos_por_candidato.items()
        )
        eleitores = "\n".join(
            f"{titulo} - {dados['nome']} (Não votou)"
            for titulo, dados in self.backend.eleitores.items()
        )
        self.conteudo.setText(
            "Candidatos\n"
            f"{candidatos}\n\n"
            f"Votos em branco: {boletim.votos_brancos}\n"
            f"Votos nulos: {boletim.votos_nulos}\n"
            f"Votos totais: {boletim.votos_totais}\n\n"
            f"Eleitores aptos: {boletim.eleitores_aptos}\n"
            f"{eleitores}"
        )