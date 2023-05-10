from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox,\
    QSizePolicy, QComboBox, QTableWidget, QAbstractItemView, QTableWidgetItem, QTextEdit
from infra.configs.connection import DBConnectionHandler
from infra.entities.nota import Nota
from infra.repository.nota_repository import NotaRepository
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        conn = DBConnectionHandler()

        self.setWindowTitle('BlocoDeNotas')
        self.setMinimumSize(500, 900)

        self.lbl_id = QLabel('Bloco de notas')

        self.lbl_titulo = QLabel('Título', self)
        self.txt_titulo = QLineEdit(self)
        self.lbl_nota = QLabel('Nota', self)
        self.txt_nota = QTextEdit(self)


        self.btn_salvar = QPushButton('Salvar')
        self.btn_limpar = QPushButton('Limpar')
        self.btn_remover = QPushButton('Remover')
        self.tabela_notas = QTableWidget()

        self.tabela_notas.setColumnCount(4)
        self.tabela_notas.setHorizontalHeaderLabels(['id', 'Título', 'Nota', 'Data'])

        self.tabela_notas.setSelectionMode(QAbstractItemView.NoSelection)
        self.tabela_notas.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tabela_notas.horizontalHeader().setDefaultSectionSize(115)
        self.tabela_notas.verticalHeader().setDefaultSectionSize(60)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.txt_titulo)
        layout.addWidget(self.lbl_nota)
        layout.addWidget(self.txt_nota)
        layout.addWidget(self.tabela_notas)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_limpar)
        layout.addWidget(self.btn_remover)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.btn_remover.setVisible(False)
        self.btn_remover.clicked.connect(self.deletar_nota)
        self.btn_salvar.clicked.connect(self.criar_nota)
        self.btn_limpar.clicked.connect(self.limpar_campos)

        self.tabela_notas.cellDoubleClicked.connect(self.carrega_dados)
        self.popula_tabela_notas()
        self.atualiza_id()



    def criar_nota(self):
        db = NotaRepository()

        nota = Nota(
            id=self.lbl_id.text().split('#')[1],
            titulo=self.txt_titulo.text(),
            nota=self.txt_nota.toPlainText(),
            data=datetime.today().strftime('%d-%m-%Y')
        )

        if self.btn_salvar.text() == 'Salvar':
            retorno = db.insert(nota.titulo, nota.nota, nota.data)
            if retorno == None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Nota criada')
                msg.setText('Nota criada com sucesso')
                msg.exec()

                self.limpar_campos()
        elif self.btn_salvar.text() == 'Atualizar':
            retorno = db.update(nota.id, nota.titulo, nota.nota)

            if retorno == None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Atualizar')
                msg.setText('Nota editada com sucesso')
                msg.exec()

        self.limpar_campos()
        self.popula_tabela_notas()
        self.atualiza_id()

    def deletar_nota(self):
        db = NotaRepository()
        retorno = db.delete(self.lbl_id.text().split('#')[1])

        if retorno == 'OK':
            msg = QMessageBox()
            msg.setWindowTitle('Remover Nota')
            msg.setText(f'A Nota {self.lbl_id.text()} foi deletada')
            msg.exec()

            self.limpar_campos()

        self.popula_tabela_notas()
        self.atualiza_id()

    def limpar_campos(self):
        for widget in self.container.children():
            if isinstance(widget, QLineEdit):
                widget.setText("")
            elif isinstance(widget, QTextEdit):
                widget.setText("")
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)

        self.btn_salvar.setText('Salvar')
        self.btn_remover.setVisible(False)


    def popula_tabela_notas(self):
        self.tabela_notas.setRowCount(0)
        db = NotaRepository()
        lista_notas = db.select_all()
        self.tabela_notas.setRowCount(len(lista_notas))
        numero = 0
        for linha, nota in enumerate(lista_notas):
            numero += 1
            valoresNota = [nota.id, nota.titulo, nota.nota, nota.data]
            for coluna, valor in enumerate(valoresNota):
                self.tabela_notas.setItem(linha, coluna, QTableWidgetItem(str(valor)))
                if(numero % 2 == 0):
                    self.tabela_notas.item(linha, coluna).setBackground(QColor(105, 105, 105))
                else:
                    self.tabela_notas.item(linha, coluna).setBackground(QColor(128, 128, 128))

    def carrega_dados(self, row, column):
        self.lbl_id.setText('Bloco de notas #' + self.tabela_notas.item(row, 0).text())
        self.txt_titulo.setText(self.tabela_notas.item(row, 1).text())
        self.txt_nota.setText(self.tabela_notas.item(row, 2).text())

        self.btn_salvar.setText('Atualizar')
        self.btn_limpar.setVisible(False)
        self.btn_remover.setVisible(True)

    def atualiza_id(self):
        db = NotaRepository()
        lista_notas = db.select_all()

        if len(lista_notas) != 0:
            self.lbl_id.setText(f'Bloco de notas #{lista_notas[len(lista_notas) - 1].id + 1}')
        else:
            self.lbl_id.setText(f'Bloco de notas #')


