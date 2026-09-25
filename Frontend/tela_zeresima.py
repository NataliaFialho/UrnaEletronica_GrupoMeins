import sys, os

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFrame,
)

class TelaZeresima(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(800, 500)