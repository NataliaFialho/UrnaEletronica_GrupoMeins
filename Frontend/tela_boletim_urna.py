import sys, os
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
    QDialog
)

ESTILO_MENU = """

    QWidget {
        font-family: Arial;
        font-size: 16px;
    }

    #info_boletim_urna {
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

    #conteudo_boletim {
        background: transparent;
    }

    #tela_menu {
        background-color:  #FFFFFF;
    }

    #boletim_urna_titulo {
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
        padding-left: 26px;
        text-align: center;
    }

    #menu_botao:hover {
        background-color: #F8F8FF;
        border-color: #3d4a63;
    }

"""

class TelaBoletimUrna(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(800, 500)
        self.setWindowTitle("Boletim de Urna")
        self.setWindowIcon(QIcon("Imagens/icone_boletim_urna.png"))

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(25, 25, 25, 25)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        icone_path = os.path.join(BASE_DIR, "..", "Imagens", "icone_boletim_urna.png")

        # ---------- Título com ícone ----------
        container = QHBoxLayout()
        container.setSpacing(12)
        container.setContentsMargins(0, 0, 0, 0)

        icone_tela_boletim_urna = QLabel()
        icone_tela_boletim_urna.setFixedSize(56, 56)
        icone_tela_boletim_urna.setPixmap(
            QPixmap(icone_path).scaled(56, 56, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        titulo_tela_boletim_urna = QLabel("BOLETIM DE URNA")
        titulo_tela_boletim_urna.setObjectName("boletim_urna_titulo")

        container.addWidget(icone_tela_boletim_urna)
        container.addWidget(titulo_tela_boletim_urna)
        container.addStretch()

        layout.addLayout(container)

        self.data_horario_boletim_urna = QLabel()
        self.data_horario_boletim_urna.setObjectName("zeresima_data")
        layout.addWidget(self.data_horario_boletim_urna)

        self.registrar_horario()

        conteudo_boletim = QWidget()
        conteudo_boletim.setObjectName("conteudo_boletim")
        conteudo_boletim.setMinimumHeight(450)

        layout_info = QVBoxLayout(conteudo_boletim)
        layout_info.setSpacing(1)
        layout_info.setAlignment(Qt.AlignTop)
        layout_info.setContentsMargins(25, 25, 25, 25)

        vencedor_boletim_urna = QLabel("Candidato vencedor: ")
        layout_info.addWidget(vencedor_boletim_urna)

        candidatos_boletim_urna = QLabel("Votos por candidato: ")
        layout_info.addWidget(candidatos_boletim_urna)

        layout_info.addStretch()

        votos_em_branco_boletim_urna = QLabel("Votos em branco:")
        layout_info.addWidget(votos_em_branco_boletim_urna)

        votos_em_nulo_boletim_urna = QLabel("Votos Nulos:")
        layout_info.addWidget(votos_em_nulo_boletim_urna)

        votos_totais_boletim_urna = QLabel("Votos Totais:")
        layout_info.addWidget(votos_totais_boletim_urna)

        layout_info.addStretch()

        eleitores_aptos_boletim_urna = QLabel("Eleitores aptos:")
        layout_info.addWidget(eleitores_aptos_boletim_urna)

        comparecimentos_boletim_urna = QLabel("Comparecimentos:")
        layout_info.addWidget(comparecimentos_boletim_urna)

        abstencoes_boletim_urna = QLabel("Abstenções:")
        layout_info.addWidget(abstencoes_boletim_urna)

        layout_info.addStretch()

        empate_boletim_urna = QLabel("Empate entre candidatos: ")
        layout_info.addWidget(empate_boletim_urna)

        layout_info.addStretch()

        situacao_eleitores_boletim_urna = QLabel("Situação dos eleitores:")
        layout_info.addWidget(situacao_eleitores_boletim_urna)

        scroll_boletim_urna = QScrollArea()
        scroll_boletim_urna.setObjectName("info_boletim_urna")
        scroll_boletim_urna.setWidgetResizable(True)
        scroll_boletim_urna.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_boletim_urna.setWidget(conteudo_boletim) 

        layout.addWidget(scroll_boletim_urna, 1)

        botao_voltar_ao_menu = QPushButton("Voltar ao Menu")
        botao_voltar_ao_menu.setObjectName("menu_botao")
        layout.addWidget(botao_voltar_ao_menu)

        self.setStyleSheet(ESTILO_MENU)

    def registrar_horario(self):
        horario_emitido = QDateTime.currentDateTime()
        horario_formatado = horario_emitido.toString("dd/MM/yyyy, HH:mm:ss")
        self.data_horario_boletim_urna.setText(f"Data e Horário da Emissão: {horario_formatado}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TelaBoletimUrna()
    window.show()
    sys.exit(app.exec())