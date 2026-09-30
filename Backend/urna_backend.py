from typing import Optional

class UrnaBackend:
    def __init__(
        self,
        eleitores: Optional[dict] = None,
        votos_brancos: int = 0,
        votos_nulos: int = 0,
    ):
        if eleitores is None:
            # Evita criar dependência circular em tempo de import.
            from Frontend.eleitor import Eleitor

            eleitores = Eleitor().eleitores

        self.eleitores = eleitores
        self.votos_brancos = votos_brancos
        self.votos_nulos = votos_nulos

    def _normalizar_titulo(self, titulo_eleitoral: str) -> str:
        # Aceita qualquer entrada do frontend (QLineEdit) e normaliza.
        # Mantém zeros à esquerda quando possível.
        if titulo_eleitoral is None:
            return ""
        return "".join(ch for ch in str(titulo_eleitoral).strip() if ch.isdigit())

    def _candidatos_titulo_para_busca(self, titulo_eleitoral: str) -> list[str]:
        """Gera chaves possíveis para buscar no dict de eleitores.

        Ajuda quando o frontend manda o título com/sem zeros, com tamanhos
        diferentes (ex: 10 vs 12 dígitos) ou com pontuação.
        """
        titulo_digitado = self._normalizar_titulo(titulo_eleitoral)
        if not titulo_digitado:
            return []

        chaves_existentes = list(self.eleitores.keys())
        tamanhos = sorted({len(k) for k in chaves_existentes if isinstance(k, str)})

        candidatos = []

        # 1) Tentativa exata (já normalizada sem pontuação)
        candidatos.append(titulo_digitado)

        # 2) Se for menor que alguma chave existente, completa com zeros à esquerda
        for tam in tamanhos:
            if len(titulo_digitado) < tam:
                candidatos.append(titulo_digitado.zfill(tam))

        # 3) Se for maior do que alguma chave existente, tenta pelo sufixo
        for tam in tamanhos:
            if len(titulo_digitado) > tam:
                candidatos.append(titulo_digitado[-tam:])

        # Remove duplicados preservando ordem
        dedup: list[str] = []
        seen = set()
        for c in candidatos:
            if c not in seen:
                dedup.append(c)
                seen.add(c)
        return dedup

    def buscar_eleitor(self, titulo_eleitoral: str) -> Optional[dict]:
        """Busca um eleitor pelo título eleitoral (com normalização)."""
        for chave in self._candidatos_titulo_para_busca(titulo_eleitoral):
            eleitor = self.eleitores.get(chave)
            if eleitor is not None:
                return eleitor
        return None

    def validar_eleitor(self, titulo_eleitoral: str) -> bool:
        """Verifica se o título eleitoral está cadastrado (com normalização)."""
        return self.buscar_eleitor(titulo_eleitoral) is not None

    def eleitor_ja_votou(self, titulo_eleitoral: str) -> bool:
        """Verifica se o eleitor já realizou o voto (com normalização)."""
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