import sys

from PySide6.QtWidgets import  QApplication, QMessageBox


ESTILO_POPUP = """

    QMessageBox {
        background-color: #ffffff;
    }

    QMessageBox QLabel {
        color: #000000;
        padding: 10px;
        font-weight: normal;
    }

    QMessageBox QLabel#qt_msgbox_label {
        color: #000000;
        font-weight: normal;
    }

    QMessageBox QPushButton {
        background-color: #ffffff;
        color: #000000;

        /* Borda fina */
        border: 1px solid #000000;

        border-radius: 8px;
        font-weight: normal;
        padding: 10px 30px;
        min-width: 80px;
    }

    
    QMessageBox QPushButton:hover {
        background-color: #F8F8FF;
        color: #000000;
        border: 1px solid #000000;
    }

    QMessageBox QPushButton:pressed {
        background-color: #f2f2f2;
        color: #000000;
        border: 1px solid #000000;
    }

"""


class PopUps(QMessageBox):
    """
    Classe responsável pelos popups do sistema.

    Ela herda de QMessageBox, então podem ser usados todoss os recursos de um QMessageBox normalmente.
    """

    def __init__(
        self,
        parent=None,
        titulo="Aviso",
        mensagem="",
        icone=QMessageBox.Warning,
        botoes=QMessageBox.Ok
    ):

        # Inicializa a classe QMessageBox
        super().__init__(parent)

        # Configura o popup
        self.setWindowTitle(titulo)
        self.setText(mensagem)
        self.setIcon(icone)
        self.setStandardButtons(botoes)

        # Aplica o estilo
        self.setStyleSheet(ESTILO_POPUP)


    @classmethod
    def acao_negada(cls, parent, titulo, mensagem):

        popup = cls(
            parent,
            titulo,
            mensagem,
            QMessageBox.Warning,
            QMessageBox.Ok
        )

        popup.exec()



    @classmethod
    def informacao(cls, parent, titulo, mensagem):

        popup = cls(
            parent,
            titulo,
            mensagem,
            QMessageBox.Information,
            QMessageBox.Ok
        )

        popup.exec()



    @classmethod
    def erro(cls, parent, titulo, mensagem):

        popup = cls(
            parent,
            titulo,
            mensagem,
            QMessageBox.Critical,
            QMessageBox.Ok
        )

        popup.exec()



    @classmethod
    def confirmar(cls, parent, titulo, mensagem):

        popup = cls(
            parent,
            titulo,
            mensagem,
            QMessageBox.Question,
            QMessageBox.Yes | QMessageBox.No
        )

        resposta = popup.exec()

        return resposta == QMessageBox.Yes


    @classmethod
    def zeresima_nao_realizada(cls, parent):

        cls.acao_negada(
            parent,
            "Votação não iniciada",
            "A votação ainda não foi iniciada.\n"
            "É necessário realizar a zerésima "
            "antes de começar a votação."
        )


    @classmethod
    def eleitor_ja_votou(cls, parent):

        cls.acao_negada(
            parent,
            "Voto não permitido",
            "Este eleitor já realizou seu voto.\n"
            "Não é permitido votar duas vezes."
        )



def main():

    app = QApplication(sys.argv)

    PopUps.zeresima_nao_realizada(None)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()