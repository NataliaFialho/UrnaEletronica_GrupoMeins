import sys, os
from PySide6.QtCore import Qt, QDateTime
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
        text-align: left;
        padding-left: 26px;
        text-align: center;
    }

    #menu_botao:hover {
        background-color: #F8F8FF;
        border-color: #3d4a63;
    }

"""

class TelaZeresima(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(800, 500)
        self.setWindowTitle("Boletim de Urna")
        self.setWindowIcon(QIcon("Imagens/icone_boletim_urna.png"))

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(25, 25, 25, 25)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        icone_path = os.path.join(BASE_DIR, "..", "Imagens", "icone_boletim_urna.png")

        container = QHBoxLayout()
        container.setSpacing(12)
        container.setContentsMargins(0, 0, 0, 0)

        icone_tela_boletim_urna = QLabel()
        icone_tela_boletim_urna.setFixedSize(56,56)
        icone_tela_boletim_urna.setContentsMargins(0, 0, 0, 0)
        icone_tela_boletim_urna.setPixmap(QPixmap(icone_path).scaled(56, 56, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        titulo_tela_boletim_urna = QLabel("BOLETIM DE URNA")
        titulo_tela_boletim_urna.setObjectName("boletim_urna_titulo")

        container.addWidget(icone_tela_boletim_urna)
        container.addWidget(titulo_tela_boletim_urna)

        layout.addLayout(container)

        titulo_tela_boletim_urna = QLabel("ZERÉSIMA")
        titulo_tela_boletim_urna.setObjectName("boletim_urna_titulo")

        self.data_horario_boletim_urna = QLabel()
        self.data_horario_boletim_urna.setObjectName("zeresima_data")
        layout.addWidget(self.data_horario_boletim_urna)

        self.registrar_horario()

        info_boletim_urna = QWidget()
        info_boletim_urna.setObjectName("info_boletim_urna")
        layout_info = QVBoxLayout(info_boletim_urna)
        layout_info.setSpacing(1)
        layout_info.setAlignment(Qt.AlignTop)
        layout_info.setContentsMargins(25, 25, 25, 25)
        
        vencedor_boletim_urna = QLabel("Candidato vencedor: ")
        layout_info.addWidget(vencedor_boletim_urna)

        layout.addStretch()

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

        eleitores_aptos_boletim_urna = QLabel("Situação dos eleitores:")
        layout_info.addWidget(eleitores_aptos_boletim_urna)

        layout.addWidget(info_boletim_urna, 1)

        botao_voltar_ao_menu = QPushButton("Voltar ao Menu")
        botao_voltar_ao_menu.setObjectName("menu_botao")
        layout.addWidget(botao_voltar_ao_menu)

        self.setStyleSheet(ESTILO_MENU)

    def registrar_horario(self):
        horario_zeresima_emitida = QDateTime.currentDateTime()
        horario_formatado = horario_zeresima_emitida.toString("dd/MM/yyyy, HH:mm:ss")
        self.data_horario_boletim_urna.setText(f"Data e Horário da Emissão: {horario_formatado}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TelaZeresima()
    window.show()
    sys.exit(app.exec())