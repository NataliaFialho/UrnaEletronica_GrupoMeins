from PySide6.QtWidgets import QMessageBox
from Backend.corrigir import corrigir
from Backend.candidatos import candidatos
from Frontend.tela_confirmacao_candidato import TelaConfirmacaoCandidato
from Backend.eleitor import eleitores


def confirmar(urna):

    numero = urna.numero_digitado

    # VOTO EM BRANCO
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

    urna.tela_confirmacao = TelaConfirmacaoCandidato()

    urna.tela_confirmacao.exibir_candidato(
        numero,
        candidato
    )

    def confirmar_voto():

        urna.votos[numero] += 1

        QMessageBox.information(
            urna,
            "Voto",
            f"Voto confirmado para {candidato['nome']}!"
        )

        urna.tela_confirmacao.close()

        finalizar_votacao(urna)

    def cancelar():
        urna.tela_confirmacao.close()

    urna.tela_confirmacao.confirmar_clicado.connect(confirmar_voto)
    urna.tela_confirmacao.cancelar_clicado.connect(cancelar)

    urna.tela_confirmacao.show()


def finalizar_votacao(urna):

    eleitores[urna.titulo_eleitor]["votou"] = True

    print("Voto registrado com sucesso.")

    urna.votacao_finalizada.emit()