from PySide6.QtWidgets import QMessageBox
from Backend.corrigir import corrigir
from Frontend.candidados import candidatos

def confirmar(urna):
    if urna.numero_digitado in candidatos:
        urna.votos[urna.numero_digitado] += 1

        QMessageBox.information(
            urna,
            "Voto",
            f"Voto confirmado para "
            f"{candidatos[urna.numero_digitado]['nome']}!"
        )

    elif urna.numero_digitado:
        urna.votos["nulo"] += 1

        QMessageBox.information(
            urna,
            "Voto",
            "Voto nulo!"
        )

    else:
        QMessageBox.warning(
            urna,
            "Atenção",
            "Digite um número ou escolha BRANCO."
        )
        return

    corrigir(urna)

    # Botões Prontos