import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import ( QApplication, QLabel, QPushButton, QVBoxLayout, QWidget,
)



class JanelaPrincipal(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Urna Eletrônica - Simulação")
        self.resize(800, 500)

        self.menu = TelaMenu()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.menu)
        self.setLayout(layout)

        self.setStyleSheet(ESTILO_MENU)


def main():

    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()