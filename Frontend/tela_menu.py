from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget
)

ESTILO_MENU = """

    QWidget {
        font-family: Arial;
        font-size: 16px;
    }

    #tela_menu {
        background-color: #FFFFFF;
    }

    #menu_titulo {
        color: #000000;
        font-size: 36px;
        font-weight: bold;
    }

    #menu_subtitulo {
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

    #menu_botao:disabled {
        background-color: #d9d9d9;
        color: #808080;
        border: 1px solid #b0b0b0;
    }
"""

class TelaMenu(QWidget):

    relatorio_inicial_clicado = Signal()
    votar_clicado = Signal()
    relatorio_final_clicado = Signal()
    sair_clicado = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("tela_menu")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(ESTILO_MENU)

        self._atalhos = []

        self._criar_widgets()
        self._criar_atalhos()

    def _criar_widgets(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(90, 70, 90, 50)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        titulo = QLabel("URNA ELETRÔNICA")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("menu_titulo")

        subtitulo = QLabel("SISTEMA DE VOTAÇÃO   •   MENU PRINCIPAL")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setObjectName("menu_subtitulo")

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addSpacing(45)

        self.botao_zeresima = self._criar_botao(
            "1",
            "Relatório Inicial (Zerésima)",
            self.relatorio_inicial_clicado
        )

        self.botao_zeresima.clicked.connect(
            self.habilitar_votar
        )

        layout.addWidget(self.botao_zeresima)

        layout.addSpacing(14)

        self.botao_votar = self._criar_botao(
            "2",
            "Votar",
            self.votar_clicado
        )

        self.botao_votar.setEnabled(False)

        layout.addWidget(self.botao_votar)

        layout.addSpacing(14)

        layout.addWidget(
            self._criar_botao(
                "3",
                "Relatório Final",
                self.relatorio_final_clicado
            )
        )

        layout.addSpacing(14)

        layout.addWidget(
            self._criar_botao(
                "4",
                "Sair",
                self.sair_clicado
            )
        )

        layout.addStretch()

        rodape = QLabel("")
        rodape.setAlignment(Qt.AlignCenter)
        rodape.setObjectName("menu_rodape")

        layout.addWidget(rodape)

        self.setLayout(layout)

    def _criar_botao(self, numero, texto, sinal):

        botao = QPushButton(f"{numero}      {texto}")
        botao.setObjectName("menu_botao")
        botao.setCursor(Qt.PointingHandCursor)
        botao.setMinimumHeight(64)

        botao.clicked.connect(sinal.emit)

        return botao

    def _criar_atalhos(self):

        mapa = {
            "1": self.relatorio_inicial_clicado,
            "2": self.votar_clicado,
            "3": self.relatorio_final_clicado,
            "4": self.sair_clicado,
        }

        for tecla, sinal in mapa.items():

            atalho = QShortcut(QKeySequence(tecla), self)
            atalho.activated.connect(sinal.emit)

            self._atalhos.append(atalho)

    def habilitar_votar(self):
        self.botao_votar.setEnabled(True)