import sys, os
from PySide6.QtCore import Qt, QDateTime, Signal
from PySide6.QtGui import QFont, QColor, QIcon, QPixmap
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
    QDialog,
    QScrollArea
)

from Backend.candidatos import candidatos
from Backend.eleitor import eleitores

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
        text-align: center;
    }

    #menu_botao:hover {
        background-color: #F8F8FF;
        border-color: #3d4a63;
    }

    #info_zeresima_scroll {
        border-width: 1px;
        border-style: solid;
        border-color: black;
        border-radius: 5px;
    }
 
    QScrollArea {
        background: transparent;
    }
 
    QScrollArea > QWidget > QWidget {
        background: transparent;
    }
 
    #zeresima_conteudo {
        background: transparent;
    }
"""

class TelaZeresima(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(800, 500)
        self.setWindowTitle("Relatório Inicial (Zerésima)")
        self.setWindowIcon(QIcon("Imagens/icone_zeresima_preto.png"))

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(25, 25, 25, 25)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        icone_path = os.path.join(BASE_DIR, "..", "Imagens", "icone_zeresima_preto.png")

        container = QHBoxLayout()
        container.setSpacing(8)
        container.setContentsMargins(0, 0, 0, 0)

        icone_tela_zeresima = QLabel()
        icone_tela_zeresima.setFixedSize(56,56)
        icone_tela_zeresima.setContentsMargins(0, 0, 0, 0)
        icone_tela_zeresima.setPixmap(QPixmap(icone_path).scaled(56, 56, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        titulo_tela_zeresima = QLabel("ZERÉSIMA")
        titulo_tela_zeresima.setObjectName("zeresima_titulo")

        container.addWidget(icone_tela_zeresima)
        container.addWidget(titulo_tela_zeresima)

        layout.addLayout(container)

        self.data_horario_zeresima = QLabel()
        self.data_horario_zeresima.setObjectName("zeresima_data")
        layout.addWidget(self.data_horario_zeresima)

        self.registrar_horario()

        info_zeresima = QWidget()
        info_zeresima.setObjectName("info_zeresima")

        conteudo_zeresima = QWidget()
        conteudo_zeresima.setObjectName ("zeresima_conteudo")
        conteudo_zeresima.setMinimumHeight (450)

        layout_info = QVBoxLayout(conteudo_zeresima)
        layout_info.setSpacing(1)
        layout_info.setAlignment(Qt.AlignTop)
        layout_info.setContentsMargins(25, 25, 25, 25)

        self.candidatos_zeresima = QLabel()
        self.candidatos_zeresima.setWordWrap(True)
        layout_info.addWidget(self.candidatos_zeresima)

        self.atualizar_candidatos(candidatos)

        layout_info.addStretch()

        votos_em_branco_zeresima = QLabel("Votos em branco:")
        layout_info.addWidget(votos_em_branco_zeresima)

        votos_em_nulo_zeresima = QLabel("Votos Nulos:")
        layout_info.addWidget(votos_em_nulo_zeresima)

        layout_info.addStretch()

        self.eleitores_aptos_zeresima = QLabel()
        layout_info.addWidget(self.eleitores_aptos_zeresima)

        self.eleitores_nao_votaram = QLabel()
        layout_info.addWidget(self.eleitores_nao_votaram)

        self.eleitores_que_votaram = QLabel()
        layout_info.addWidget(self.eleitores_que_votaram)


        self.atualizar_eleitores(eleitores)

        scroll_zeresima = QScrollArea()
        scroll_zeresima.setObjectName ("info_zeresima_scroll")
        scroll_zeresima.setWidgetResizable(True)
        scroll_zeresima.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_zeresima.setWidget(conteudo_zeresima)

        layout.addWidget(scroll_zeresima, 1)

        layout.addWidget(info_zeresima)

        botao_voltar_ao_menu = QPushButton("Voltar ao Menu")
        botao_voltar_ao_menu.setObjectName("menu_botao")
        layout.addWidget(botao_voltar_ao_menu)

        self.setStyleSheet(ESTILO_MENU)

    def registrar_horario(self):
        horario_zeresima_emitida = QDateTime.currentDateTime()
        horario_formatado = horario_zeresima_emitida.toString("dd/MM/yyyy, HH:mm:ss")
        self.data_horario_zeresima.setText(f"Data e Horário da Emissão: {horario_formatado}")

    def atualizar_candidatos(self, candidatos):
        texto = "Candidatos:\n\n"

        for numero, dados in candidatos.items():
            texto += (
                f"{numero} - {dados['nome']} "
                f"({dados['partido']})\n"
            )

        self.candidatos_zeresima.setText(texto)

    def atualizar_eleitores(self, eleitores):
        texto = f"Eleitores aptos: {len(eleitores)}\n\n"

        for titulo, dados in eleitores.items():
            status = "Votou" if dados["votou"] else "Não votou"

            texto += (
                f"{titulo} - {dados['nome']} "
                f"({status})\n"
            )

        self.eleitores_aptos_zeresima.setText(texto)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TelaZeresima()
    janela.exec()