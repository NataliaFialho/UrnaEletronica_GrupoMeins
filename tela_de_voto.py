import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

ESTILOS = """
    QLabel#titulo {
        color: black;
    }

    QPushButton#numericos {
        background-color: #444;
        color: white;
    }

    QPushButton#btn-branco {
        background-color: white;
    }

    QPushButton#btn-corrige {
        background-color: orange;
    }

    QPushButton#btn-confirma {
        background-color: green; color: white;
    }

    QWidget#teclado-widget {
        background-color: #444;
    }

    QLabel#foto-label {
        border: 1px solid black;
    }
"""

class UrnaEletronica(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Urna Eletrônica")
        self.setFixedSize(800, 500)

        # Candidatos fictícios
        self.candidatos = {
            "01": {
                "nome": "Evelyn Palbueno",
                "partido": "Professor",
                "foto": "fotos/candidato1.jpg"
            },
            "02": {
                "nome": "Mauricio de Souza",
                "partido": "Desenvolvedor de Jogos",
                "foto": "fotos/candidato2.jpg"
            },
            "03": {
                "nome": "Ederson",
                "partido": "Desenvolvedor de Software",
                "foto": "fotos/candidato3.jpg"
            }
        }
            
        self.votos = {
            "01": 0,
            "02": 0,
            "03": 0,
            "nulo": 0,
            "branco": 0
        }

        self.numero_digitado = ""

        self.criar_interface()

    def criar_interface(self):
        layout_principal = QHBoxLayout()

        # Tela da urna
        tela = QVBoxLayout()

        titulo = QLabel("SEU VOTO PARA")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Arial", 18))
        titulo.setObjectName("titulo")

        self.numero_label = QLabel("")
        self.numero_label.setAlignment(Qt.AlignCenter)
        self.numero_label.setFont(QFont("Arial", 30))

        self.nome_label = QLabel("")
        self.partido_label = QLabel("")

        self.nome_label.setFont(QFont("Arial", 14))
        self.partido_label.setFont(QFont("Arial", 14))

        self.foto_label = QLabel()
        self.foto_label.setFixedSize(200, 250)
        self.foto_label.setObjectName ("foto-label")

        tela.addWidget(titulo)
        tela.addWidget(self.numero_label)
        tela.addWidget(self.nome_label)
        tela.addWidget(self.partido_label)
        tela.addWidget(self.foto_label)

        # Teclado
        teclado = QGridLayout()
        teclado.setContentsMargins(30, 0, 0, 0)

        numeros = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('0', 3, 1)
        ]

        for texto, linha, coluna in numeros:
            botao = QPushButton(texto)
            botao.setObjectName("numericos")
            botao.setFixedSize(70, 50)
            botao.clicked.connect(
                lambda checked, t=texto: self.digitar_numero(t)
            )
            teclado.addWidget(botao, linha, coluna)

        branco = QPushButton("BRANCO")
        branco.setFixedSize(70, 50)
        branco.setObjectName("btn-branco")
        # branco.clicked.connect(self.voto_branco)

        corrige = QPushButton("CORRIGE")
        corrige.setFixedSize(70, 50)
        corrige.setObjectName("btn-corrige")
        # corrige.clicked.connect(self.corrigir)

        confirma = QPushButton("CONFIRMA")
        confirma.setFixedSize(70, 50)
        confirma.setObjectName("btn-confirma")
        # confirma.clicked.connect(self.confirmar)

        teclado.addWidget(branco, 4, 0)
        teclado.addWidget(corrige, 4, 1)
        teclado.addWidget(confirma, 4, 2)
        
        teclado_widget = QWidget()
        teclado_widget.setObjectName("teclado-widget")
        teclado_widget.setLayout(teclado)
        teclado_widget.setMaximumWidth(400)

        layout_principal.addLayout(tela, 2)
        layout_principal.addWidget(teclado_widget, 1)

        self.setLayout(layout_principal)

app = QApplication(sys.argv)
app.setStyleSheet(ESTILOS)
janela = UrnaEletronica()
janela.show()
sys.exit(app.exec())