from typing import Optional
from Frontend.eleitor import Eleitor

class UrnaBackend:
    def __init__(self, eleitores: dict, votos_brancos: int = 0, votos_nulos: int = 0):
        self.eleitores = eleitores
        self.votos_brancos = votos_brancos
        self.votos_nulos = votos_nulos

    def buscar_eleitor(self, titulo_eleitoral: str) -> Optional[dict]:
        """Busca um eleitor pelo título eleitoral."""
        return self.eleitores.get(titulo_eleitoral)

    def validar_eleitor(self, titulo_eleitoral: str) -> bool:
        """Verifica se o título eleitoral está cadastrado."""
        return titulo_eleitoral in self.eleitores

    def eleitor_ja_votou(self, titulo_eleitoral: str) -> bool:
        """Verifica se o eleitor já realizou o voto."""
        eleitor = self.buscar_eleitor(titulo_eleitoral)

        if eleitor is None:
            return False

        return eleitor["votou"]

    def registrar_voto(self, titulo_eleitoral: str) -> tuple[bool, str]:
        """Registra que o eleitor realizou o voto."""
        eleitor = self.buscar_eleitor(titulo_eleitoral)

        if eleitor is None:
            return False, "Título eleitoral não encontrado."

        if eleitor["votou"]:
            return False, "Este eleitor já realizou o voto."

        eleitor["votou"] = True

        return True, f"Eleitor {eleitor['nome']} liberado para votação."

    def registrar_voto_branco(self) -> None:
        """Incrementa o contador de votos em branco."""
        self.votos_brancos += 1

    def registrar_voto_nulo(self) -> None:
        """Incrementa o contador de votos nulos."""
        self.votos_nulos += 1

    def obter_votos_brancos(self) -> int:
        """Retorna a quantidade de votos em branco."""
        return self.votos_brancos

    def obter_votos_nulos(self) -> int:
        """Retorna a quantidade de votos nulos."""
        return self.votos_nulos

    def obter_total_eleitores(self) -> int:
        """Retorna a quantidade total de eleitores cadastrados."""
        return len(self.eleitores)

    def obter_total_eleitores_que_votaram(self) -> int:
        """Retorna a quantidade de eleitores que já votaram."""
        return sum(
            1
            for eleitor in self.eleitores.values()
            if eleitor["votou"]
        )

    def obter_total_eleitores_que_nao_votaram(self) -> int:
        """Retorna a quantidade de eleitores que ainda não votaram."""
        return sum(
            1
            for eleitor in self.eleitores.values()
            if not eleitor["votou"]
        )