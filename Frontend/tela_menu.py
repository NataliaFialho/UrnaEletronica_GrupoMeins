from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class TelaMenu(QWidget):
    relatorio_inicial_clicado = Signal()
    votar_clicado = Signal()
    encerrar_votacao_clicado = Signal()
    relatorio_final_clicado = Signal()
    sair_clicado = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget { font-family: Arial; font-size: 16px; background: white; }
            QLabel#titulo { color: #000; font-size: 34px; font-weight: bold; }
            QLabel#subtitulo { color: #333; font-size: 13px; font-weight: bold; }
            QPushButton { background: white; color: #000; border: 1px solid #2c3648;
                border-radius: 10px; font-size: 17px; font-weight: 600; text-align: left;
                padding-left: 24px; }
            QPushButton:hover:enabled { background: #F8F8FF; }
            QPushButton:disabled { background: #e4e4e4; color: #888; border-color: #bbb; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(90, 32, 90, 28)
        layout.setSpacing(9)

        titulo = QLabel("URNA ELETRÔNICA")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo")
        subtitulo = QLabel("SISTEMA DE VOTAÇÃO • MENU PRINCIPAL")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setObjectName("subtitulo")
        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addSpacing(10)

        self.botao_zeresima = self._criar_botao("Relatório Inicial (Zerésima)", self.relatorio_inicial_clicado)
        self.botao_votar = self._criar_botao("Votar", self.votar_clicado)
        self.botao_encerrar = self._criar_botao("Encerrar votação", self.encerrar_votacao_clicado)
        self.botao_relatorio_final = self._criar_botao("Relatório Final", self.relatorio_final_clicado)
        self.botao_sair = self._criar_botao("Sair", self.sair_clicado)

        for botao in (
            self.botao_zeresima,
            self.botao_votar,
            self.botao_encerrar,
            self.botao_relatorio_final,
            self.botao_sair,
        ):
            layout.addWidget(botao)
        layout.addStretch()

    @staticmethod
    def _criar_botao(texto, sinal):
        botao = QPushButton(texto)
        botao.setCursor(Qt.PointingHandCursor)
        botao.setMinimumHeight(52)
        botao.clicked.connect(lambda checked=False: sinal.emit())
        return botao
