import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget


class TelaConfirmacaoCandidato(QWidget):
    """Página de confirmação para votos válidos, nulos e em branco."""

    confirmar_clicado = Signal()
    cancelar_clicado = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmação de Voto")
        self.setMinimumSize(800, 500)
        self.setStyleSheet("""
            QWidget { background: white; font-family: Arial; color: #17212f; }
            QLabel#numero { font-size: 20px; font-weight: bold; }
            QLabel#nome { font-size: 20px; font-weight: bold; }
            QLabel#partido { font-size: 16px; }
            QLabel#pergunta { font-size: 17px; font-weight: 600; }
            QLabel#foto { border: 1px solid #2c3648; border-radius: 8px; }
            QPushButton { background: white; border: 1px solid #2c3648;
                border-radius: 8px; padding: 10px 25px; font-size: 16px; }
            QPushButton#confirmar { background: #2c3648; color: white; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 25, 50, 25)
        layout.setSpacing(12)

        self.foto_candidato = QLabel()
        self.foto_candidato.setObjectName("foto")
        self.foto_candidato.setFixedSize(210, 190)
        self.foto_candidato.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.foto_candidato, alignment=Qt.AlignHCenter)

        self.numero_candidato = QLabel()
        self.numero_candidato.setObjectName("numero")
        self.numero_candidato.setAlignment(Qt.AlignCenter)
        self.nome_candidato = QLabel()
        self.nome_candidato.setObjectName("nome")
        self.nome_candidato.setAlignment(Qt.AlignCenter)
        self.partido_candidato = QLabel()
        self.partido_candidato.setObjectName("partido")
        self.partido_candidato.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.numero_candidato)
        layout.addWidget(self.nome_candidato)
        layout.addWidget(self.partido_candidato)

        pergunta = QLabel("Confirma este voto?")
        pergunta.setObjectName("pergunta")
        pergunta.setAlignment(Qt.AlignCenter)
        layout.addWidget(pergunta)
        layout.addStretch()

        botoes = QHBoxLayout()
        botao_cancelar = QPushButton("Cancelar")
        botao_cancelar.clicked.connect(lambda checked=False: self.cancelar_clicado.emit())
        botao_confirmar = QPushButton("Confirmar voto")
        botao_confirmar.setObjectName("confirmar")
        botao_confirmar.clicked.connect(lambda checked=False: self.confirmar_clicado.emit())
        botoes.addWidget(botao_cancelar)
        botoes.addWidget(botao_confirmar)
        layout.addLayout(botoes)

    def configurar_voto(self, tipo, numero="", candidato=None):
        self.numero_candidato.setText(f"Número: {numero}" if numero else "")
        self.foto_candidato.clear()
        self.partido_candidato.clear()

        if tipo == "candidato" and candidato:
            self.nome_candidato.setText(candidato["nome"])
            self.partido_candidato.setText(candidato["partido"])
            pixmap = QPixmap(candidato["foto"])
            if not pixmap.isNull():
                self.foto_candidato.setPixmap(
                    pixmap.scaled(210, 190, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            else:
                self.foto_candidato.setText("Foto indisponível")
        elif tipo == "branco":
            self.numero_candidato.setText("")
            self.nome_candidato.setText("VOTO EM BRANCO")
            self.foto_candidato.setText("BRANCO")
        else:
            self.nome_candidato.setText("VOTO NULO")
            self.foto_candidato.setText(numero)

    def exibir_candidato(self, numero, candidato):
        """Mantém compatibilidade com chamadas antigas deste componente."""
        self.configurar_voto("candidato", numero, candidato)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TelaConfirmacaoCandidato()
    janela.show()
    sys.exit(app.exec())
