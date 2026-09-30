import os
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QFrame, QSpacerItem, QSizePolicy,
                               QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap

from Backend.eleitor import eleitores

from Frontend.popup import PopUps
 
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
    titulo_validado = Signal(str)
    cancelar_clicado = Signal()
    titulo_validado = Signal(str)

    def __init__(self, eleitores):
        super().__init__()

        self.eleitores = eleitores
     
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
        raiz_projeto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho_icone = os.path.join(raiz_projeto, "Imagens", "icone_titulo_eleitoral.png")
        icone_label.setPixmap(QPixmap(caminho_icone))
 
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
        header_layout.addStretch() 
 
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
        self.input_titulo.setMaxLength(20)
        self.input_titulo.returnPressed.connect(self.continuar_para_votar)
 
        input_layout.addWidget(label_input) 
        input_layout.addWidget(self.input_titulo) 
        input_layout.addStretch() 
 
        botoes_layout = QHBoxLayout() 
        botoes_layout.addStretch() 
        botoes_layout.setSpacing(10) 
 
        btn_cancelar = QPushButton("Cancelar") 
        btn_cancelar.setObjectName("btnCancelar") 
        btn_cancelar.setCursor(Qt.PointingHandCursor)
 
        btn_continuar = QPushButton("Continuar") 
        btn_continuar.setObjectName("btnContinuar")
        btn_continuar.clicked.connect(self.validar_titulo)
        btn_continuar.setCursor(Qt.PointingHandCursor)
 
        # Faz o Cancelar voltar para o menu
        btn_cancelar.clicked.connect(self.voltar_ao_menu)
        btn_continuar.clicked.connect(self.continuar_para_votar)

        botoes_layout.addWidget(btn_cancelar)
        botoes_layout.addWidget(btn_continuar)

        card_layout.addLayout(header_layout) 
        card_layout.addWidget(input_frame) 
        card_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)) 
        card_layout.addLayout(botoes_layout) 
 
        layout_principal.addWidget(card) 
 
        card.setStyleSheet(ESTILO_TELA_TITULO) 

    def continuar_para_votar(self):
        titulo = self.input_titulo.text().strip()
        if not titulo:
            QMessageBox.warning(self, "Atenção", "Digite o título eleitoral.")
            return
        self.titulo_validado.emit(titulo)

    def voltar_ao_menu(self):
        self.cancelar_clicado.emit()

    def limpar(self):
        self.input_titulo.clear()
 
if __name__ == "__main__": 
    app = QApplication(sys.argv) 
    tela = TelaTituloEleitor() 
    tela.show() 
    sys.exit(app.exec())
