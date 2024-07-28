import sys
from PySide6.QtWidgets import QApplication
from ButtonHolder import ButtonHolder

app = QApplication(sys.argv)
window = ButtonHolder()
window.show()
app.exec()