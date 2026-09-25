import sys
from PySide6.QtWidgets import QApplication
from Frontend.tela_zeresima import TelaZeresima

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TelaZeresima()
    window.show()
    sys.exit(app.exec())