import sys
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        # Menu Bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        quit_action = file_menu.addAction("&Quit")
        quit_action.triggered.connect(self.quit_app)

        # Central Widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout(central_widget)


        # Tool Bar
        tool_bar = self.addToolBar("&Toolbar")
        tool_bar.setMovable(False)
        tool_bar.setIconSize(QSize(16, 16))

        # Input fields
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter name")
        layout.addWidget(self.name_input)

        self.age_input = QLineEdit(self)
        self.age_input.setPlaceholderText("Enter age")
        layout.addWidget(self.age_input)

        # Buttons
        create_button = QPushButton("Create", self)
        layout.addWidget(create_button)
        create_button.clicked.connect(self.create_record)

        read_button = QPushButton("Read", self)
        layout.addWidget(read_button)
        read_button.clicked.connect(self.read_record)

        update_button = QPushButton("Update", self)
        layout.addWidget(update_button)
        update_button.clicked.connect(self.update_record)

        delete_button = QPushButton("Delete", self)
        layout.addWidget(delete_button)
        delete_button.clicked.connect(self.delete_record)

        self.setLayout(layout)
        self.setWindowTitle("CRUD")

    def quit_app(self):
        self.app.quit()

    def create_record(self):
        name = self.name_input.text()
        age = self.age_input.text()
        # Implement your create logic here
        print(f"Creating record: {name}, {age}")

    def read_record(self):
        # Implement your read logic here
        print("Reading record")

    def update_record(self):
        # Implement your update logic here
        print("Updating record")

    def delete_record(self):
        # Implement your delete logic here
        print("Deleting record")

if __name__ == "__main__":
    # print(QStyleFactory.keys())
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())
