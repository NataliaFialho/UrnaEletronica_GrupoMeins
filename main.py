from PySide6.QtWidgets import QApplication
from Frontend.tela_de_voto import UrnaEletronica
import sys

app = QApplication(sys.argv)

janela = UrnaEletronica()
janela.show()

sys.exit(app.exec())