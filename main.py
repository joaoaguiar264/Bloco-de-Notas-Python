import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from view.tela_principal import MainWindow
import qdarktheme


app = QApplication(sys.argv)
qdarktheme.setup_theme()

window = MainWindow()
icone = QIcon('images/notepad')
window.setWindowIcon(icone)
window.show()
app.exec()