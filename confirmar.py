from PySide6.QtWidgets import QMessageBox

from candidatos import CANDIDATOS


def confirmar(urna):

    numero = urna.numero_digitado

    if not numero:

        QMessageBox.warning(
            urna,
            "Atenção",
            "Digite o número do candidato."
        )

        return

    # Número inexistente
    if numero not in CANDIDATOS:

        resposta = QMessageBox.question(
            urna,
            "Voto nulo",
            "Esse candidato não existe.\n\n"
            "Deseja confirmar o VOTO NULO?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:

            urna.votos["NULO"] += 1

            QMessageBox.information(
                urna,
                "Voto confirmado",
                "VOTO NULO CONFIRMADO!"
            )

            urna.proximo_voto()

        return

    # Candidato encontrado
    candidato = CANDIDATOS[numero]

    resposta = QMessageBox.question(
        urna,
        "Confirmar voto",
        f"Nome: {candidato['nome']}\n"
        f"Partido: {candidato['partido']}\n\n"
        "CONFIRMAR ESTE VOTO?",
        QMessageBox.Yes | QMessageBox.No
    )

    if resposta == QMessageBox.Yes:

        urna.votos[numero] += 1

        QMessageBox.information(
            urna,
            "Voto confirmado",
            f"VOTO PARA {candidato['nome']} "
            "CONFIRMADO!"
        )

        urna.proximo_voto()