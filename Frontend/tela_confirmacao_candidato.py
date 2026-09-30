import sys
import os
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QKeySequence, QPixmap, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ESTILO_CONFIRMACAO = """

    QWidget {
        font-family: Arial;
        font-size: 16px;
    }

    #tela_confirmacao {
        background-color: #FFFFFF;
    }

    #confirmacao_foto {
        background-color: #F8F8FF;
        border: 1px solid #2c3648;
        border-radius: 10px;
        color: #4d5a75;
        font-size: 13px;
    }

    #confirmacao_numero {
        color: #000000;
        font-size: 18px;
        font-weight: bold;
    }

    #confirmacao_nome {
        color: #000000;
        font-size: 18px;
        font-weight: bold;
    }

    #confirmacao_partido {
        color: #000000;
        font-size: 18px;
    }

    #confirmacao_pergunta {
        color: #000000;
        font-size: 16px;
        font-weight: 600;
    }

    #menu_botao {
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #2c3648;
        border-radius: 10px;
        font-size: 18px;
        font-weight: 600;
    }

    #menu_botao:hover {
        background-color: #F8F8FF;
        border-color: #3d4a63;
    }

    #botao_confirmar {
        background-color: #2c3648;
        color: #FFFFFF;
        border: 1px solid #2c3648;
        border-radius: 10px;
        font-size: 18px;
        font-weight: 600;
    }

    #botao_confirmar:hover {
        background-color: #3d4a63;
    }
"""

class TelaConfirmacaoCandidato(QWidget):

    confirmar_clicado = Signal()
    cancelar_clicado = Signal()
    voltar_menu_clicado = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("tela_confirmacao")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedSize(800, 500)
        self.setWindowTitle("Confirmação de Candidato")
        self.setStyleSheet(ESTILO_CONFIRMACAO)

        self._atalhos = []

        self._criar_widgets()
        self._criar_atalhos()

    def _criar_widgets(self):

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(50, 25, 50, 25)
        layout_principal.setSpacing(15)

        self.foto_candidato = QLabel()
        self.foto_candidato.setObjectName("confirmacao_foto")
        self.foto_candidato.setFixedSize(230, 220)
        self.foto_candidato.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(self.foto_candidato, alignment=Qt.AlignHCenter)

        layout_informacoes = QVBoxLayout()
        layout_informacoes.setSpacing(4)
        layout_informacoes.setAlignment(Qt.AlignTop)

        self.numero_candidato = QLabel()
        self.numero_candidato.setObjectName("confirmacao_numero")
        self.numero_candidato.setAlignment(Qt.AlignCenter)

        self.nome_candidato = QLabel()
        self.nome_candidato.setObjectName("confirmacao_nome")
        self.nome_candidato.setAlignment(Qt.AlignCenter)
        self.nome_candidato.setWordWrap(True)

        self.partido_candidato = QLabel()
        self.partido_candidato.setObjectName("confirmacao_partido")
        self.partido_candidato.setAlignment(Qt.AlignCenter)
        self.partido_candidato.setWordWrap(True)

        layout_informacoes.addWidget(self.numero_candidato)
        layout_informacoes.addWidget(self.nome_candidato)
        layout_informacoes.addWidget(self.partido_candidato)

        layout_principal.addLayout(layout_informacoes, 1)

        pergunta_confirmacao = QLabel("Confirmar o voto?")
        pergunta_confirmacao.setObjectName("confirmacao_pergunta")
        pergunta_confirmacao.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(pergunta_confirmacao)

        layout_botoes = QHBoxLayout()
        layout_botoes.setSpacing(20)

        botao_cancelar = QPushButton("Cancelar")
        botao_cancelar.setObjectName("menu_botao")
        botao_cancelar.setCursor(Qt.PointingHandCursor)
        botao_cancelar.setMinimumHeight(36)
        botao_cancelar.clicked.connect(self.cancelar_clicado.emit)

        botao_confirmar = QPushButton("Confirmar (S)")
        botao_confirmar.setObjectName("botao_confirmar")
        botao_confirmar.setCursor(Qt.PointingHandCursor)
        botao_confirmar.setMinimumHeight(36)
        botao_confirmar.clicked.connect(self.confirmar_clicado.emit)

        layout_botoes.addWidget(botao_cancelar)
        layout_botoes.addWidget(botao_confirmar)
        layout_principal.addLayout(layout_botoes)

        botao_voltar_menu = QPushButton("Voltar ao Menu")
        botao_voltar_menu.setObjectName("menu_botao")
        botao_voltar_menu.setCursor(Qt.PointingHandCursor)
        botao_voltar_menu.setMinimumHeight(36)
        botao_voltar_menu.clicked.connect(self.voltar_menu_clicado.emit)
        layout_principal.addWidget(botao_voltar_menu)

    def _criar_atalhos(self):

        mapa_atalhos = {
            "S": self.confirmar_clicado,
            "Esc": self.cancelar_clicado,
        }

        for tecla, sinal in mapa_atalhos.items():
            atalho = QShortcut(QKeySequence(tecla), self)
            atalho.activated.connect(sinal.emit)
            self._atalhos.append(atalho)

    @Slot(str, dict)
    def exibir_candidato(self, numero, candidato):
        """Slot que atualiza a tela com o candidato votado.

        Conecte diretamente ao sinal da tela de votação que carrega o
        candidato escolhido, por exemplo:

            tela_de_voto.candidato_selecionado.connect(
                tela_confirmacao_candidato.exibir_candidato
            )

        onde `candidato_selecionado = Signal(str, dict)` é emitido pela
        tela de votação com o número digitado e o dicionário do
        candidato (mesmo formato de `candidatos.py`).
        """
        self.numero_candidato.setText(numero)
        self.nome_candidato.setText(f"Nome: {candidato['nome']}")
        self.partido_candidato.setText(f"Partido: {candidato['partido']}")
        self._carregar_foto(candidato["foto"])

    def _carregar_foto(self, caminho_foto):
        caminho_completo = os.path.join(BASE_DIR, "..", caminho_foto)

        pixmap = QPixmap(caminho_completo)

        if pixmap.isNull():
            self.foto_candidato.clear()
            self.foto_candidato.setText("Foto indisponível")
            return

        self.foto_candidato.setPixmap(
            pixmap.scaled(
                230,
                220,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

if __name__ == "__main__":
    # Demonstração isolada: na integração real, quem chama exibir_candidato
    # é o sinal candidato_selecionado da tela de votação (veja o docstring
    # do método), não uma chamada direta como abaixo.
    # Só para demonstrar como ficaria a tela de confirmação com um candidato específico.
    aplicacao = QApplication(sys.argv)
    janela_confirmacao = TelaConfirmacaoCandidato()
    janela_confirmacao.exibir_candidato(
        "01",
        {
            "nome": "Evelyn Palbueno",
            "partido": "Professor",
            "foto": "Imagens/candidato1.jpg",
        },
    )
    janela_confirmacao.show()
    sys.exit(aplicacao.exec())