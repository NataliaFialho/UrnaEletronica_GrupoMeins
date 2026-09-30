def voto_branco(urna):
    """Solicita confirmação de branco sem alterar os totais eleitorais."""
    urna.voto_solicitado.emit("branco", "")
