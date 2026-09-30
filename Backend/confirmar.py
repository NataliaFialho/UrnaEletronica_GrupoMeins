from PySide6.QtWidgets import QMessageBox

from Backend.candidatos import candidatos
from Backend.eleitor import eleitores

def confirmar(urna):

    numero = urna.numero_digitado

    # Nenhum número foi digitado
    if not numero:

        QMessageBox.warning(
            urna,
            "Atenção",
            "Digite um número ou escolha BRANCO."
        )

        return

    # VOTO NULO
    if numero not in candidatos:

        urna.votos["nulo"] += 1

        QMessageBox.information(
            urna,
            "Voto",
            "Voto nulo!"
        )

        finalizar_votacao(urna)

        return

    # VOTO EM CANDIDATO
    candidato = candidatos[numero]

    urna.candidato_selecionado.emit(
        numero,
        candidato
    )


def registrar_voto(urna, numero):

    if numero not in candidatos:
        return False

    candidato = candidatos[numero]

    urna.votos[numero] += 1

    QMessageBox.information(
        urna,
        "Voto",
        f"Voto confirmado para {candidato['nome']}!"
    )

    finalizar_votacao(urna)

    return True


def finalizar_votacao(urna):

    eleitores[
        urna.titulo_eleitor
    ]["votou"] = True

    urna.votacao_finalizada.emit()