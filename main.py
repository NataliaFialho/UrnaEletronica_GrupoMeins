import sys

from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QStackedWidget,
    QWidget
)

from Frontend.tela_menu import TelaMenu
from Frontend.tela_zeresima import TelaZeresima
from Frontend.tela_boletim_urna import TelaBoletimUrna
from Frontend.tela_informar_titulo import TelaTituloEleitor
from Backend.eleitor import eleitores
from Frontend.tela_de_voto import UrnaEletronica

class JanelaPrincipal(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Urna Eletrônica - Simulação")
        self.resize(800, 500)

        self.menu = TelaMenu()
        self.zeresima = TelaZeresima()
        self.boletim_urna = TelaBoletimUrna()
        self.informar_titulo = TelaTituloEleitor(eleitores)

        # A urna só será criada depois que o título for validado
        self.tela_urna = None
        self.titulo_atual = None

        self.stack = QStackedWidget()

        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.zeresima)
        self.stack.addWidget(self.boletim_urna)
        self.stack.addWidget(self.informar_titulo)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)

        self.setLayout(layout)

        self._conectar_sinais()

    def _conectar_sinais(self):

        self.menu.relatorio_inicial_clicado.connect(
            self.ir_para_zeresima
        )

        self.menu.votar_clicado.connect(
            self.ir_para_informar_titulo
        )

        self.menu.relatorio_final_clicado.connect(
            self.ir_para_boletim_urna
        )

        self.menu.sair_clicado.connect(
            self.sair
        )

        self.zeresima.zeresima_confirmada.connect(
            self.confirmar_zeresima
        )

        self.boletim_urna.boletim_confirmado.connect(
            self.confirmar_boletim
        )

        self.informar_titulo.cancelar_clicado.connect(
            self.confirmar_informar_titulo
        )

        self.informar_titulo.titulo_validado.connect(
            self.abrir_urna
        )

    def ir_para_zeresima(self):
        self.stack.setCurrentWidget(self.zeresima)

    def ir_para_informar_titulo(self):
        self.stack.setCurrentWidget(self.informar_titulo)

    def ir_para_boletim_urna(self):
        self.stack.setCurrentWidget(self.boletim_urna)

    def confirmar_zeresima(self):
        self.stack.setCurrentWidget(self.menu)

    def confirmar_boletim(self):
        self.stack.setCurrentWidget(self.menu)

    def confirmar_informar_titulo(self):
        self.stack.setCurrentWidget(self.menu)

    def sair(self):
        self.close()

    def abrir_urna(self, titulo):

        self.titulo_atual = titulo

        print(f"Título validado: {titulo}")
        print(f"Eleitor: {eleitores[titulo]['nome']}")

        self.tela_urna = UrnaEletronica(titulo)

        self.tela_urna.votacao_finalizada.connect(
            self.finalizar_votacao
        )

        self.stack.addWidget(self.tela_urna)
        self.stack.setCurrentWidget(self.tela_urna)

    def finalizar_votacao(self):

        self.stack.setCurrentWidget(self.informar_titulo)

        if self.tela_urna is not None:
            self.stack.removeWidget(self.tela_urna)
            self.tela_urna.close()
            self.tela_urna.deleteLater()
            self.tela_urna = None

        self.titulo_atual = None

        self.informar_titulo.input_titulo.clear()

def main():
    app = QApplication(sys.argv)

    janela = JanelaPrincipal()
    janela.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()