import sys

from PySide6.QtWidgets import  QApplication, QMessageBox
from PySide6.QtCore import Qt


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

        for botao in self.buttons():
            botao.setCursor(Qt.PointingHandCursor)

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
    def urna_fechada(cls, parent):

        cls.informacao(
            parent,
            "Sistema Eleitoral",
            "Votação encerrada!\n"
            
        )


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