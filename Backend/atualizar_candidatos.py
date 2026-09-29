def atualizar_candidatos(label, candidatos):
    texto = "Candidatos:\n\n"

    for numero, dados in candidatos.items():
        texto += (
            f"{numero} - {dados['nome']} "
            f"({dados['partido']}) - "
            f"Votos: {dados['votos']}\n"
        )

    label.setText(texto)