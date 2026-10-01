import sys

from PySide6.QtWidgets import QApplication, QMessageBox, QStackedWidget, QVBoxLayout, QWidget

from Backend.som_confirmacao import tocar_som_confirmacao
from Backend.urna_backend import UrnaBackend, urna_backend
from Frontend.tela_boletim_urna import TelaBoletimUrna
from Frontend.tela_confirmacao_candidato import TelaConfirmacaoCandidato
from Frontend.tela_de_voto import UrnaEletronica
from Frontend.tela_informar_titulo import TelaTituloEleitor
from Frontend.tela_menu import TelaMenu
from Frontend.tela_zeresima import TelaZeresima


class JanelaPrincipal(QWidget):
    def __init__(self, backend: UrnaBackend = urna_backend):
        super().__init__()
        self.backend = backend
        self.setWindowTitle("Urna Eletrônica - Simulação")
        self.resize(800, 500)

        self.menu = TelaMenu()
        self.zeresima = TelaZeresima(backend)
        self.boletim_urna = TelaBoletimUrna(backend)
        self.informar_titulo = TelaTituloEleitor()
        self.confirmacao = TelaConfirmacaoCandidato()
        self.tela_urna = None
        self.titulo_atual = None
        self.voto_pendente = None

        self.stack = QStackedWidget()
        for tela in (self.menu, self.zeresima, self.boletim_urna, self.informar_titulo, self.confirmacao):
            self._adicionar_tela(tela)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)

        self._conectar_sinais()
        self._atualizar_menu()
        self.stack.setCurrentWidget(self.menu)

    def _adicionar_tela(self, tela):
        """Registra uma tela e reaplica seu QSS já na hierarquia do stack."""
        self.stack.addWidget(tela)

        # Cada tela define seu próprio stylesheet antes de ser anexada ao stack.
        # Reaplicá-lo depois do reparent garante que o Qt recalcule o estilo de
        # todos os widgets descendentes na hierarquia final da aplicação.
        widgets = (tela, *tela.findChildren(QWidget))
        for widget in widgets:
            estilo = widget.styleSheet()
            if estilo:
                widget.setStyleSheet("")
                widget.setStyleSheet(estilo)
            widget.ensurePolished()

    def _conectar_sinais(self):
        self.menu.relatorio_inicial_clicado.connect(self.ir_para_zeresima)
        self.menu.votar_clicado.connect(self.ir_para_informar_titulo)
        self.menu.relatorio_final_clicado.connect(self.ir_para_boletim_urna)
        self.menu.encerrar_votacao_clicado.connect(self.encerrar_eleicao)
        self.menu.sair_clicado.connect(self.close)

        self.zeresima.zeresima_confirmada.connect(self.confirmar_zeresima)
        self.zeresima.zeresima_cancelada.connect(self.voltar_ao_menu)
        self.boletim_urna.boletim_confirmado.connect(self.confirmar_boletim)
        self.informar_titulo.cancelar_clicado.connect(self.voltar_ao_menu)
        self.informar_titulo.titulo_validado.connect(self.abrir_urna)
        self.confirmacao.confirmar_clicado.connect(self.confirmar_voto)
        self.confirmacao.cancelar_clicado.connect(self.cancelar_confirmacao)

    def _atualizar_menu(self):
        eleicao_iniciada = self.backend.eleicao_iniciada and not self.backend.urna_fechada
        self.menu.botao_zeresima.setEnabled(not self.backend.eleicao_iniciada)
        self.menu.botao_votar.setEnabled(eleicao_iniciada)
        self.menu.botao_encerrar.setEnabled(eleicao_iniciada)
        self.menu.botao_relatorio_final.setEnabled(self.backend.urna_fechada)

    def ir_para_zeresima(self):
        if self.backend.eleicao_iniciada:
            return
        self.zeresima.atualizar_dados()
        self.stack.setCurrentWidget(self.zeresima)

    def confirmar_zeresima(self):
        ok, mensagem = self.backend.iniciar_eleicao()
        if not ok:
            QMessageBox.warning(self, "Zerésima", mensagem)
            return
        self._atualizar_menu()
        self.stack.setCurrentWidget(self.menu)

    def ir_para_informar_titulo(self):
        if not self.backend.eleicao_iniciada or self.backend.urna_fechada:
            QMessageBox.warning(self, "Votação indisponível", "A votação não está aberta.")
            self._atualizar_menu()
            return
        self.stack.setCurrentWidget(self.informar_titulo)

    def abrir_urna(self, titulo):
        ok, mensagem = self.backend.validar_eleitor_para_votar(titulo)
        if not ok:
            QMessageBox.warning(self, "Voto não permitido", mensagem)
            return

        self.titulo_atual = self.backend.normalizar_titulo(titulo)
        self.tela_urna = UrnaEletronica(self.titulo_atual, self.backend)
        self.tela_urna.voto_solicitado.connect(self.solicitar_confirmacao_voto)
        self._adicionar_tela(self.tela_urna)
        self.stack.setCurrentWidget(self.tela_urna)

    def solicitar_confirmacao_voto(self, tipo, numero):
        if self.titulo_atual is None:
            return
        ok, mensagem = self.backend.validar_eleitor_para_votar(self.titulo_atual)
        if not ok:
            QMessageBox.warning(self, "Voto não permitido", mensagem)
            self._finalizar_votacao()
            return

        candidato = self.backend.candidatos.get(numero) if tipo == "candidato" else None
        self.voto_pendente = (tipo, numero)
        self.confirmacao.configurar_voto(tipo, numero, candidato)
        self.stack.setCurrentWidget(self.confirmacao)

    def confirmar_voto(self):
        if self.titulo_atual is None or self.voto_pendente is None:
            return
        tipo, numero = self.voto_pendente
        ok, mensagem = self.backend.registrar_voto(self.titulo_atual, tipo, numero)
        if not ok:
            QMessageBox.warning(self, "Voto não registrado", mensagem)
            self.voto_pendente = None
            self._finalizar_votacao()
            return

        tocar_som_confirmacao()
        if tipo == "candidato":
            nome_voto = self.backend.candidatos[numero]["nome"]
        elif tipo == "branco":
            nome_voto = "em branco"
        else:
            nome_voto = "nulo"
        QMessageBox.information(self, "Voto confirmado", f"Voto {nome_voto} registrado.")
        self.voto_pendente = None
        self._finalizar_votacao()

    def cancelar_confirmacao(self):
        self.voto_pendente = None
        if self.tela_urna is not None:
            self.stack.setCurrentWidget(self.tela_urna)

    def _finalizar_votacao(self):
        self.stack.setCurrentWidget(self.informar_titulo)
        if self.tela_urna is not None:
            self.stack.removeWidget(self.tela_urna)
            self.tela_urna.deleteLater()
            self.tela_urna = None
        self.titulo_atual = None
        self.informar_titulo.limpar()

    def voltar_ao_menu(self):
        self.stack.setCurrentWidget(self.menu)

    def encerrar_eleicao(self):
        if not self.backend.eleicao_iniciada or self.backend.urna_fechada:
            self._atualizar_menu()
            return
        resposta = QMessageBox.question(
            self,
            "Encerrar votação",
            "Deseja encerrar a eleição? Não será mais possível registrar votos.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if resposta != QMessageBox.StandardButton.Yes:
            return
        ok, mensagem = self.backend.encerrar_eleicao()
        if not ok:
            QMessageBox.warning(self, "Encerrar votação", mensagem)
            return
        self._atualizar_menu()
        QMessageBox.information(self, "Votação encerrada", mensagem)

    def ir_para_boletim_urna(self):
        if not self.backend.urna_fechada:
            QMessageBox.warning(self, "Boletim indisponível", "Encerre a eleição antes de abrir o boletim final.")
            self._atualizar_menu()
            return
        self.boletim_urna.atualizar_dados()
        self.stack.setCurrentWidget(self.boletim_urna)

    def confirmar_boletim(self):
        self.stack.setCurrentWidget(self.menu)


def main():
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
