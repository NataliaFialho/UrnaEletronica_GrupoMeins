import os

from PySide6.QtCore import Qt, QDateTime, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget

from Backend.urna_backend import UrnaBackend, urna_backend


class TelaBoletimUrna(QWidget):
    boletim_confirmado = Signal()

    def __init__(self, backend: UrnaBackend = urna_backend, parent=None):
        super().__init__(parent)
        self.backend = backend

        raiz_projeto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icone = os.path.join(raiz_projeto, "Imagens", "icone_boletim_urna.png")
        self.setWindowTitle("Boletim de Urna")
        self.setWindowIcon(QIcon(icone))
        self.setStyleSheet("""
            QWidget { font-family: Arial; font-size: 14px; }
            QLabel#titulo { color: #000; font-size: 30px; font-weight: bold; }
            QLabel#data { color: #333; font-weight: bold; }
            QPushButton { background: white; border: 1px solid #2c3648;
                border-radius: 8px; padding: 10px; font-size: 15px; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(10)

        titulo = QLabel("BOLETIM DE URNA")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        self.data_horario = QLabel()
        self.data_horario.setObjectName("data")
        layout.addWidget(self.data_horario)

        self.conteudo = QLabel()
        self.conteudo.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.conteudo.setWordWrap(True)
        self.conteudo.setTextInteractionFlags(Qt.TextSelectableByMouse)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.conteudo)
        layout.addWidget(scroll, 1)

        botao_voltar = QPushButton("Voltar ao Menu")
        botao_voltar.clicked.connect(lambda checked=False: self.boletim_confirmado.emit())
        layout.addWidget(botao_voltar)

        self.atualizar_dados()

    def atualizar_dados(self):
        agora = QDateTime.currentDateTime().toString("dd/MM/yyyy, HH:mm:ss")
        self.data_horario.setText(f"Data e horário da emissão: {agora}")
        boletim = self.backend.boletim_atual()

        linhas_candidatos = [
            f"{codigo} - {self.backend.candidatos[codigo]['nome']}: {votos} voto(s)"
            for codigo, votos in boletim.votos_por_candidato.items()
        ]
        if boletim.empate:
            resultado = "Empate entre: " + ", ".join(
                self.backend.candidatos[codigo]["nome"] for codigo in boletim.vencedor
            )
        elif boletim.vencedor:
            codigo = boletim.vencedor[0]
            resultado = f"Vencedor: {self.backend.candidatos[codigo]['nome']} ({boletim.votos_por_candidato[codigo]} voto(s))"
        else:
            resultado = "Sem votos válidos para candidato."

        self.conteudo.setText(
            f"{resultado}\n\n"
            "Votos por candidato\n"
            f"{chr(10).join(linhas_candidatos)}\n\n"
            f"Votos em branco: {boletim.votos_brancos}\n"
            f"Votos nulos: {boletim.votos_nulos}\n"
            f"Votos totais: {boletim.votos_totais}\n\n"
            f"Eleitores aptos: {boletim.eleitores_aptos}\n"
            f"Comparecimentos: {boletim.comparecimentos}\n"
            f"Abstenções: {boletim.abstencoes}\n\n"
            f"Situação dos eleitores\n{boletim.situacao_eleitores}"
        )


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    janela = TelaBoletimUrna()
    janela.show()
    sys.exit(app.exec())
