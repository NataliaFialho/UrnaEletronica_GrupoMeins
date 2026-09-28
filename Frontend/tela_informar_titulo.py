import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QFrame, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from Backend.urna_backend import UrnaBackend

ESTILO_TELA_TITULO = """
            #cardPrincipal {
                background-color: white;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
            }
            #tituloVotar {
                font-size: 17px;
                font-weight: bold;
                color: #1a2a40;
                background-color: white;
            }
            #subtitulo {
                font-size: 13px;
                color: #6b7280;
                background-color: white;
            }
            #frameInput {
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                background-color: #DBDBDB;
            }
            #labelInput {
                font-size: 13px;
                font-weight: bold;
                color: #374151;
                border: none;
                background-color: #DBDBDB;
            }
            #inputTitulo {
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 10px;
                font-size: 13px;
                background-color: #ffffff;
                color: #333333;
            }
            #inputTitulo:focus {
                border: 1px solid #6b9cce;
            }
            #btnCancelar {
                background-color: #f3f4f6;
                color: #4b5563;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            #btnCancelar:hover {
                background-color: #e5e7eb;
            }
            #btnContinuar {
                background-color: #6486aa;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            #btnContinuar:hover {
                background-color: #4a6b8c;
            }
            """

class TelaTituloEleitor(QWidget):
    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("Urna Eletrônica - Informar Título")
        self.setMinimumSize(800, 500)
        self.setStyleSheet("background-color: #f0f4f8;") 

        layout_principal = QVBoxLayout(self)
        layout_principal.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("cardPrincipal")
        card.setFixedSize(700, 400)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        header_layout = QHBoxLayout()
        
        icone_label = QLabel()
        icone_label.setPixmap(QPixmap("Imagens/icone_titulo_eleitoral.png"))

        textos_layout = QVBoxLayout()
        textos_layout.setSpacing(2)
        
        titulo_label = QLabel("VOTAR")
        titulo_label.setObjectName("tituloVotar")
        
        subtitulo_label = QLabel("Informe seu titulo de eleitor")
        subtitulo_label.setObjectName("subtitulo")

        textos_layout.addWidget(titulo_label)
        textos_layout.addWidget(subtitulo_label)

        header_layout.addWidget(icone_label)
        header_layout.addLayout(textos_layout)
        header_layout.addStretch() # Empurra tudo para a esquerda

        input_frame = QFrame()
        input_frame.setObjectName("frameInput")
        input_frame.setFixedHeight(200)
        
        input_layout = QVBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 15, 15, 15)
        input_layout.setSpacing(8)

        label_input = QLabel("Título de eleitor:")
        label_input.setObjectName("labelInput")

        self.input_titulo = QLineEdit()
        self.input_titulo.setPlaceholderText("Digite o número do seu título")
        self.input_titulo.setObjectName("inputTitulo")

        input_layout.addWidget(label_input)
        input_layout.addWidget(self.input_titulo)
        input_layout.addStretch()

        botoes_layout = QHBoxLayout()
        botoes_layout.addStretch() # Empurra os botões para a direita
        botoes_layout.setSpacing(10)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btnCancelar")

        btn_continuar = QPushButton("Continuar")
        btn_continuar.setObjectName("btnContinuar")

        botoes_layout.addWidget(btn_cancelar)
        botoes_layout.addWidget(btn_continuar)

        card_layout.addLayout(header_layout)
        card_layout.addWidget(input_frame)
        card_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        card_layout.addLayout(botoes_layout)

        layout_principal.addWidget(card)

        card.setStyleSheet(ESTILO_TELA_TITULO)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela = TelaTituloEleitor()
    tela.show()
    sys.exit(app.exec())