import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QLineEdit
import io
from contextlib import redirect_stdout
from folder import run_folder
from file import run_file


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.setWindowTitle('Patriot Data Processing')

        # Create central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)  

        # Create layout for central widget
        layout = QGridLayout(central_widget)

        # Create text box to display output
        self.textbox = QPlainTextEdit(self)
        self.textbox.setReadOnly(True)
        layout.addWidget(self.textbox, 1, 0, 1, 2)

        # Create line edit to display dropped file name
        self.file_line_edit = QLineEdit(self)
        self.file_line_edit.setReadOnly(True)
        layout.addWidget(self.file_line_edit, 0, 0, 1, 2)

        # Create buttons
        button1 = QPushButton('File', self)
        button2 = QPushButton('Folder', self)

        # Add buttons to layout
        layout.addWidget(button1, 2, 0)
        layout.addWidget(button2, 2, 1)

        # Connect buttons to functions
        button1.clicked.connect(self.function1)
        button2.clicked.connect(self.function2)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.file_line_edit.setText(file_path)
        self.filename = file_path

    def function1(self):
        self.textbox.clear()
        input_file = self.filename
        f = io.StringIO()
        with redirect_stdout(f):
            run_file(input_file)
        output = f.getvalue()
        self.textbox.insertPlainText(output)
        
    def function2(self):
        self.textbox.clear()
        input_file = self.filename
        f = io.StringIO()
        with redirect_stdout(f):
            run_folder(input_file)
        output = f.getvalue()
        self.textbox.insertPlainText(output)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())
