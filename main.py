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
# from Frontend.tela_eleitoral import TelaEleitoral  
  
class JanelaPrincipal(QWidget):  
  
    def __init__(self):  
        super().__init__()  
  
        self.setWindowTitle("Urna Eletrônica - Simulação")  
        self.resize(800, 500)  
  
        self.menu = TelaMenu()  
        self.zeresima = TelaZeresima()  
        self.boletim_urna = TelaBoletimUrna() 
        self.informar_titulo = TelaTituloEleitor() 
        #self.votar = TelaEleitoral()  
  
        self.stack = QStackedWidget()  
        self.stack.addWidget(self.menu)  
        self.stack.addWidget(self.zeresima) 
        self.stack.addWidget(self.boletim_urna) 
        self.stack.addWidget(self.informar_titulo) 
        #self.stack.addWidget(self.votar)  
  
        layout = QVBoxLayout()  
        layout.setContentsMargins(0, 0, 0, 0)  
        layout.addWidget(self.stack)  
        self.setLayout(layout)  
  
        self._conectar_sinais()  
  
    def _conectar_sinais(self):  
        self.menu.relatorio_inicial_clicado.connect( 
            self.ir_para_zeresima 
        ) #Troca pra tela da zerésima 
 
        self.menu.votar_clicado.connect( 
            self.ir_para_informar_titulo 
        ) #Troca pra tela de informar título 
 
        self.menu.relatorio_final_clicado.connect( 
            self.ir_para_boletim_urna 
        ) #Troca pra tela do relatório final 
 
        self.menu.sair_clicado.connect( 
            self.sair 
        ) #Sai do sistema 
 
        self.zeresima.zeresima_confirmada.connect( 
            self.confirmar_zeresima 
        ) #Volta para a tela de menu 
 
        self.boletim_urna.boletim_confirmado.connect( 
            self.confirmar_boletim 
        ) #Volta para a tela de menu

        self.informar_titulo.cancelar_clicado.connect(
            self.confirmar_informar_titulo
        ) #Volta para a tela de menu
  
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
  
def main():  
    app = QApplication(sys.argv)  
    janela = JanelaPrincipal()  
    janela.show()  
    sys.exit(app.exec())  
  
  
if __name__ == "__main__":  
    main()