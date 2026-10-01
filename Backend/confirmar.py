from PySide6.QtWidgets import QMessageBox


def confirmar(urna):
    """Abre a etapa de confirmação; o backend só registra após aceite."""
    numero = urna.numero_digitado
    tamanho = urna.backend.obter_tamanho_codigo_candidato()
    if len(numero) != tamanho:
        QMessageBox.warning(
            urna,
            "Atenção",
            f"Digite o número completo de {tamanho} dígitos ou escolha BRANCO.",
        )
        return

    tipo = "candidato" if numero in urna.backend.candidatos else "nulo"
    urna.voto_solicitado.emit(tipo, numero)
