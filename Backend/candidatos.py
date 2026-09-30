import os


RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _caminho_imagem(nome_arquivo):
    return os.path.join(RAIZ_PROJETO, "Imagens", nome_arquivo)


candidatos = {
    "01": {
        "nome": "Evelyn Palbueno",
        "partido": "Professor",
        "foto": _caminho_imagem("candidato1.jpg"),
        "votos": 0
    },
    "02": {
        "nome": "Mauricio de Souza",
        "partido": "Desenvolvedor de Jogos",
        "foto": _caminho_imagem("candidato2.jpg"),
        "votos": 0
    },
    "03": {
        "nome": "Ederson da Costa",
        "partido": "Desenvolvedor de Software",
        "foto": _caminho_imagem("candidato3.jpg"),
        "votos": 0
    }
}
