from PySide6.QtWidgets import QMessageBox
from Backend.corrigir import corrigir
from Backend.candidatos import candidatos

def confirmar(urna):

    if not urna.numero_digitado:
        QMessageBox.warning(
            urna,
            "Atenção",
            "Digite um número ou escolha BRANCO."
        )
        return

    if urna.numero_digitado in candidatos:

        candidato = candidatos[urna.numero_digitado]

        resposta = QMessageBox.question(
            urna,
            "Confirmar voto",
            f"Nome: {candidato['nome']}\n"
            f"Partido: {candidato['partido']}\n"
            f"Número: {urna.numero_digitado}\n\n"
            "Confirmar o voto?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.No:
            return

        urna.votos[urna.numero_digitado] += 1

        QMessageBox.information(
            urna,
            "Voto",
            f"Voto confirmado para {candidato['nome']}!"
        )

    else:

        resposta = QMessageBox.question(
            urna,
            "Voto nulo",
            f"Número digitado: {urna.numero_digitado}\n\n"
            "Confirmar voto nulo?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.No:
            return

        urna.votos["nulo"] += 1

        QMessageBox.information(
            urna,
            "Voto",
            "Voto nulo confirmado!"
        )

    corrigir(urna)