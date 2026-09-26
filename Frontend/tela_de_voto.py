import sys, os
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

from Backend.confirmar import confirmar
from Backend.corrigir import corrigir
from Backend.voto_branco import voto_branco
from Frontend.candidados import candidatos

ESTILOS = """
    QLabel#titulo {
        color: black;
    }

    QPushButton#numericos {
        background-color: #E8EDF3;
        color: black;
    }

    QPushButton#btn-branco {
        background-color: white;
        color: black;
        border: 2px solid #618CAA;
    }

    QPushButton#btn-corrige {
        background-color: orange;
    }

    QPushButton#btn-confirma {
        background-color: green; color: white;
    }

    QWidget#teclado-widget {
        background-color: white;
        border: 2px solid #618CAA;
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
        self.setStyleSheet(ESTILOS)
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
        branco.clicked.connect(lambda: voto_branco(self))

        corrige = QPushButton("CORRIGE")
        corrige.setFixedSize(70, 50)
        corrige.setObjectName("btn-corrige")
        corrige.clicked.connect(lambda: corrigir(self))

        confirma = QPushButton("CONFIRMA")
        confirma.setFixedSize(70, 50)
        confirma.setObjectName("btn-confirma")
        confirma.clicked.connect(lambda: confirmar(self))

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

    def digitar_numero(self, numero):
        if len(self.numero_digitado) < 2:
            self.numero_digitado += numero
            self.numero_label.setText(self.numero_digitado)

            if len(self.numero_digitado) == 2:
                self.mostrar_candidato()

    def mostrar_candidato(self):
        if self.numero_digitado in candidatos:
            candidato = candidatos[self.numero_digitado]

            self.nome_label.setText(candidato["nome"])
            self.partido_label.setText(candidato["partido"])

            pixmap = QPixmap(candidato["foto"])
            self.foto_label.setPixmap(
                pixmap.scaled(
                    self.foto_label.size(),
                    Qt.KeepAspectRatio
                )
            )
        else:
            self.nome_label.setText("VOTO NULO")
            self.partido_label.setText("")
            self.foto_label.clear()