import sys
from PySide6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Application")
        # self.setGeometry(100, 100, 800, 600)
        # Add your GUI components here

if __name__ == "__main__":
    # print(QStyleFactory.keys())
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())