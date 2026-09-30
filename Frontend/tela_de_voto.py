from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from Backend.urna_backend import UrnaBackend, urna_backend


ESTILOS = """
QWidget { background-color: #EEF2F5; font-family: Arial; }
QLabel { color: #334E68; }
QLabel#titulo { color: #334E68; font-size: 28px; font-weight: bold; padding: 15px; }
QPushButton#numericos { background: #E8EDF3; color: #334E68; border: 1px solid #C7D0D9;
    border-radius: 8px; font-size: 22px; font-weight: bold; }
QPushButton#numericos:hover { background: #DDE6EE; }
QPushButton#btn-branco { background: white; border: 1px solid #C7D0D9;
    border-radius: 8px; color: #334E68; font-weight: bold; }
QPushButton#btn-corrige { background: #F4B64E; border: none; border-radius: 8px;
    color: #334E68; font-weight: bold; }
QPushButton#btn-confirma { background: #3F9D8B; border: none; border-radius: 8px;
    color: white; font-weight: bold; }
QWidget#teclado-widget { background: white; border: 1px solid #D6DDE4; border-radius: 10px; padding: 20px; }
QLabel#foto-label { background: #F7F9FB; border: 1px solid #D6DDE4; border-radius: 8px; }
QFrame#painel-esquerdo { background: white; border: 1px solid #D6DDE4; border-radius: 10px; }
"""


class UrnaEletronica(QWidget):
    voto_solicitado = Signal(str, str)

    def __init__(self, titulo_eleitor: str, backend: UrnaBackend = urna_backend):
        super().__init__()
        self.backend = backend
        self.titulo_eleitor = backend.normalizar_titulo(titulo_eleitor)
        self.numero_digitado = ""

        self.setWindowTitle("Urna Eletrônica")
        self.setFixedSize(800, 500)
        self._criar_interface()

    def _criar_interface(self):
        self.setStyleSheet(ESTILOS)
        layout_principal = QHBoxLayout(self)

        painel_esquerdo = QFrame()
        painel_esquerdo.setObjectName("painel-esquerdo")
        painel = QVBoxLayout(painel_esquerdo)

        titulo = QLabel("SEU VOTO PARA")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo")
        self.numero_label = QLabel("")
        self.numero_label.setAlignment(Qt.AlignCenter)
        self.numero_label.setStyleSheet("font-size: 30px;")
        self.nome_label = QLabel("")
        self.nome_label.setAlignment(Qt.AlignCenter)
        self.partido_label = QLabel("")
        self.partido_label.setAlignment(Qt.AlignCenter)
        self.foto_label = QLabel()
        self.foto_label.setFixedSize(200, 230)
        self.foto_label.setAlignment(Qt.AlignCenter)
        self.foto_label.setObjectName("foto-label")

        for widget in (titulo, self.numero_label, self.nome_label, self.partido_label):
            painel.addWidget(widget)
        painel.addWidget(self.foto_label, alignment=Qt.AlignCenter)

        teclado = QGridLayout()
        teclado.setContentsMargins(20, 0, 20, 0)
        for indice, digito in enumerate("123456789"):
            linha, coluna = divmod(indice, 3)
            self._adicionar_botao_numero(teclado, digito, linha, coluna)
        self._adicionar_botao_numero(teclado, "0", 3, 1)

        botao_branco = QPushButton("BRANCO")
        botao_branco.setFixedSize(90, 55)
        botao_branco.setObjectName("btn-branco")
        botao_branco.clicked.connect(lambda: self.voto_solicitado.emit("branco", ""))

        botao_corrigir = QPushButton("CORRIGE")
        botao_corrigir.setFixedSize(90, 55)
        botao_corrigir.setObjectName("btn-corrige")
        botao_corrigir.clicked.connect(self.corrigir)

        botao_confirmar = QPushButton("CONFIRMA")
        botao_confirmar.setFixedSize(90, 55)
        botao_confirmar.setObjectName("btn-confirma")
        botao_confirmar.clicked.connect(self.confirmar)

        teclado.addWidget(botao_branco, 4, 0)
        teclado.addWidget(botao_corrigir, 4, 1)
        teclado.addWidget(botao_confirmar, 4, 2)

        teclado_widget = QWidget()
        teclado_widget.setObjectName("teclado-widget")
        teclado_widget.setLayout(teclado)
        teclado_widget.setMaximumWidth(400)

        layout_principal.addWidget(painel_esquerdo, 2)
        layout_principal.addWidget(teclado_widget, 1)

    def _adicionar_botao_numero(self, teclado, digito, linha, coluna):
        botao = QPushButton(digito)
        botao.setObjectName("numericos")
        botao.setFixedSize(90, 55)
        botao.clicked.connect(lambda checked=False, valor=digito: self.digitar_numero(valor))
        teclado.addWidget(botao, linha, coluna)

    def digitar_numero(self, numero: str):
        tamanho = self.backend.obter_tamanho_codigo_candidato()
        if len(self.numero_digitado) >= tamanho:
            return
        self.numero_digitado += numero
        self.numero_label.setText(self.numero_digitado)
        self.nome_label.clear()
        self.partido_label.clear()
        self.foto_label.clear()

        if len(self.numero_digitado) == tamanho:
            self.mostrar_candidato()

    def mostrar_candidato(self):
        candidato = self.backend.candidatos.get(self.numero_digitado)
        if candidato is None:
            self.nome_label.setText("VOTO NULO")
            return
        self.nome_label.setText(candidato["nome"])
        self.partido_label.setText(candidato["partido"])
        pixmap = QPixmap(candidato["foto"])
        if not pixmap.isNull():
            self.foto_label.setPixmap(
                pixmap.scaled(self.foto_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )

    def confirmar(self):
        if not self.numero_digitado:
            QMessageBox.warning(self, "Atenção", "Digite o número do candidato ou escolha BRANCO.")
            return
        tamanho = self.backend.obter_tamanho_codigo_candidato()
        if len(self.numero_digitado) != tamanho:
            QMessageBox.warning(self, "Atenção", f"Digite os {tamanho} dígitos do número.")
            return
        tipo = "candidato" if self.numero_digitado in self.backend.candidatos else "nulo"
        self.voto_solicitado.emit(tipo, self.numero_digitado)

    def corrigir(self):
        self.numero_digitado = ""
        self.numero_label.clear()
        self.nome_label.clear()
        self.partido_label.clear()
        self.foto_label.clear()
