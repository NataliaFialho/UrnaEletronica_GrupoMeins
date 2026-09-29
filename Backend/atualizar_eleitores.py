def atualizar_eleitores(label, eleitores):
    texto = f"Eleitores aptos: {len(eleitores)}\n\n"

    for titulo, dados in eleitores.items():
        status = "Votou" if dados["votou"] else "Não votou"

        texto += (
            f"{titulo} - {dados['nome']} "
            f"({status})\n"
        )

    label.setText(texto)