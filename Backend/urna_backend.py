from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from Backend.candidatos import candidatos as CANDIDATOS
from Backend.eleitor import eleitores as ELEITORES


@dataclass(frozen=True)
class Boletim:
    votos_por_candidato: dict[str, int]
    votos_brancos: int
    votos_nulos: int
    votos_totais: int
    eleitores_aptos: int
    comparecimentos: int
    abstencoes: int
    vencedor: list[str]
    empate: bool
    situacao_eleitores: str


class UrnaBackend:
    """Fonte única de estado e regras da eleição."""

    def __init__(self):
        self.eleitores = ELEITORES
        self.candidatos = CANDIDATOS
        self.votos_brancos = 0
        self.votos_nulos = 0
        self.eleicao_iniciada = False
        self.urna_fechada = False

    @staticmethod
    def normalizar_titulo(titulo_eleitoral: str) -> str:
        if titulo_eleitoral is None:
            return ""
        return "".join(ch for ch in str(titulo_eleitoral).strip() if ch.isdigit())

    def buscar_eleitor(self, titulo_eleitoral: str) -> Optional[dict]:
        # Aceita pontuação, mas exige o número completo: sufixos e zeros
        # acrescentados poderiam identificar outra pessoa.
        return self.eleitores.get(self.normalizar_titulo(titulo_eleitoral))

    def validar_eleitor(self, titulo_eleitoral: str) -> bool:
        return self.buscar_eleitor(titulo_eleitoral) is not None

    def eleitor_ja_votou(self, titulo_eleitoral: str) -> bool:
        eleitor = self.buscar_eleitor(titulo_eleitoral)
        return bool(eleitor and eleitor.get("votou", False))

    def obter_tamanho_codigo_candidato(self) -> int:
        tamanhos = [len(chave) for chave in self.candidatos if chave.isdigit()]
        return min(tamanhos, default=0)

    def iniciar_eleicao(self) -> tuple[bool, str]:
        if self.eleicao_iniciada:
            return False, "A zerésima já foi confirmada."
        if self.urna_fechada:
            return False, "Esta eleição já foi encerrada."
        self.eleicao_iniciada = True
        return True, "Eleição iniciada."

    def encerrar_eleicao(self) -> tuple[bool, str]:
        if not self.eleicao_iniciada:
            return False, "A eleição ainda não foi iniciada."
        if self.urna_fechada:
            return False, "A eleição já foi encerrada."
        self.urna_fechada = True
        return True, "Eleição encerrada."

    def validar_eleitor_para_votar(self, titulo_eleitoral: str) -> tuple[bool, str]:
        titulo = self.normalizar_titulo(titulo_eleitoral)
        if not titulo:
            return False, "Digite o título eleitoral."
        eleitor = self.eleitores.get(titulo)
        if eleitor is None:
            return False, "Título eleitoral não cadastrado."
        if not self.eleicao_iniciada:
            return False, "A votação ainda não foi iniciada. Confirme a zerésima."
        if self.urna_fechada:
            return False, "A eleição já foi encerrada."
        if eleitor.get("votou", False):
            return False, "Este eleitor já votou."
        return True, "OK"

    def registrar_voto(
        self,
        titulo_eleitoral: str,
        tipo_voto: str,
        numero_candidato: str = "",
    ) -> tuple[bool, str]:
        ok, mensagem = self.validar_eleitor_para_votar(titulo_eleitoral)
        if not ok:
            return False, mensagem

        eleitor = self.eleitores[self.normalizar_titulo(titulo_eleitoral)]
        if tipo_voto == "branco":
            self.votos_brancos += 1
        elif tipo_voto == "nulo":
            codigo = str(numero_candidato)
            tamanho = self.obter_tamanho_codigo_candidato()
            if len(codigo) != tamanho:
                return False, f"Digite um número completo de {tamanho} dígitos para registrar voto nulo."
            if codigo in self.candidatos:
                return False, "O número digitado pertence a um candidato."
            self.votos_nulos += 1
        elif tipo_voto == "candidato":
            codigo = str(numero_candidato)
            tamanho = self.obter_tamanho_codigo_candidato()
            if len(codigo) != tamanho:
                return False, f"Digite o número completo ({tamanho} dígitos)."
            candidato = self.candidatos.get(codigo)
            if candidato is None:
                return False, "O candidato informado não existe."
            candidato["votos"] = int(candidato.get("votos", 0)) + 1
        else:
            return False, "Tipo de voto inválido."

        # A marcação e o contador acontecem juntos, somente depois da
        # confirmação explícita da tela de confirmação.
        eleitor["votou"] = True
        return True, "Voto registrado."

    def registrar_voto_candidato(self, titulo_eleitoral: str, numero_candidato: str) -> tuple[bool, str]:
        return self.registrar_voto(titulo_eleitoral, "candidato", numero_candidato)

    def registrar_voto_branco(self, titulo_eleitoral: str) -> tuple[bool, str]:
        return self.registrar_voto(titulo_eleitoral, "branco")

    def registrar_voto_nulo(self, titulo_eleitoral: str, numero_digitado: str) -> tuple[bool, str]:
        return self.registrar_voto(titulo_eleitoral, "nulo", numero_digitado)

    def obter_total_eleitores(self) -> int:
        return len(self.eleitores)

    def obter_total_eleitores_que_votaram(self) -> int:
        return sum(bool(eleitor.get("votou")) for eleitor in self.eleitores.values())

    def obter_total_eleitores_que_nao_votaram(self) -> int:
        return self.obter_total_eleitores() - self.obter_total_eleitores_que_votaram()

    def todos_votaram(self) -> bool:
        return self.eleicao_iniciada and all(
            bool(eleitor.get("votou")) for eleitor in self.eleitores.values()
        )

    def obter_vencedor_empate(self) -> tuple[list[str], bool]:
        votos = {codigo: int(dados.get("votos", 0)) for codigo, dados in self.candidatos.items()}
        maior_total = max(votos.values(), default=0)
        if maior_total == 0:
            return [], False
        vencedores = sorted(codigo for codigo, total in votos.items() if total == maior_total)
        return vencedores, len(vencedores) > 1

    def boletim_atual(self) -> Boletim:
        votos_por_candidato = {
            codigo: int(dados.get("votos", 0))
            for codigo, dados in self.candidatos.items()
        }
        eleitores_aptos = self.obter_total_eleitores()
        comparecimentos = self.obter_total_eleitores_que_votaram()
        vencedores, empate = self.obter_vencedor_empate()
        situacao = "\n".join(
            f"{titulo} - {dados.get('nome', '')} "
            f"({'Votou' if dados.get('votou') else 'Não votou'})"
            for titulo, dados in self.eleitores.items()
        )
        return Boletim(
            votos_por_candidato=votos_por_candidato,
            votos_brancos=self.votos_brancos,
            votos_nulos=self.votos_nulos,
            votos_totais=sum(votos_por_candidato.values()) + self.votos_brancos + self.votos_nulos,
            eleitores_aptos=eleitores_aptos,
            comparecimentos=comparecimentos,
            abstencoes=eleitores_aptos - comparecimentos,
            vencedor=vencedores,
            empate=empate,
            situacao_eleitores=situacao,
        )


urna_backend = UrnaBackend()
