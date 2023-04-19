import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from controller.nota_dao import Database
from view.tela_principal import MainWindow
import qdarktheme


db = Database()
db.connect()
db.create_table_nota()
db.close_connection()

app = QApplication(sys.argv)
qdarktheme.setup_theme()

window = MainWindow()
icone = QIcon('images/notepad')
window.setWindowIcon(icone)
window.show()
app.exec()