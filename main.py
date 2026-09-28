import sys

from PySide6.QtWidgets import ( 
    QApplication,
    QVBoxLayout,
    QStackedWidget, 
    QWidget
)
from Frontend.tela_menu import TelaMenu
from Frontend.tela_zeresima import TelaZeresima
# from Frontend.tela_eleitoral import TelaEleitoral

class JanelaPrincipal(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Urna Eletrônica - Simulação")
        self.resize(800, 500)

        self.menu = TelaMenu()
        self.zeresima = TelaZeresima()
        #self.votar = TelaEleitoral()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.zeresima)
        #self.stack.addWidget(self.votar)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self._conectar_sinais()

    def _conectar_sinais(self):
        self.menu.relatorio_inicial_clicado.connect(self.ir_para_zeresima) #Troca pra tela da zerésima
        self.menu.sair_clicado.connect(self.sair) #Sai do sistema

    def ir_para_zeresima(self):
        self.stack.setCurrentWidget(self.zeresima)

    def sair(self):
        self.close()

def main():
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
