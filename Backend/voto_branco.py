from PySide6.QtWidgets import QMessageBox
from Backend.corrigir import corrigir

def voto_branco(urna):
    urna.votos["branco"] += 1

    QMessageBox.information(
        urna,
        "Voto",
        "Voto em branco confirmado!"
    )

    corrigir(urna)