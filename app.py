import sys
import os
from PyPDF2 import PdfMerger
from PyQt6.QtWidgets import (
    QCheckBox,
    QErrorMessage,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QApplication,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QFileDialog
)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("Lonbal")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.internal_layout = QVBoxLayout()
        self.central_widget.setLayout(self.internal_layout)
        self.InitalConfig()


    def InitalConfig(self):
        self.open_button = QPushButton("new")
        self.open_button.clicked.connect(self.select_folder)

        self.internal_layout.addWidget(self.open_button)        
        self.pdf_list = []

    def select_folder(self):

        folder = QFileDialog.getExistingDirectory()

        if not os.path.lexists(folder):
            msg = QErrorMessage()
            msg.showMessage("The Folder doesn't excist")

        for file in os.listdir(folder):
            if file.endswith(".pdf"):
                checkbox = QCheckBox(file)
                checkbox.setChecked(True)
                self.pdf_list.append(
                    {
                        "filename" : file,
                        "path": os.path.join(folder,file),
                        "selected" :True,
                        "widget": checkbox
                    }
                )
                self.internal_layout.addWidget(checkbox)

        if len(self.pdf_list) > 0:
            # save button
            self.save_button = QPushButton("Save Join")
            self.internal_layout.addWidget(self.save_button)
            self.save_button.clicked.connect(self.save_file)
             

    def save_file(self):
        join_file = QFileDialog.getSaveFileName()[0]

        if not join_file:
            msg = QErrorMessage()
            msg.showMessage(f"file: {join_file} is not valid")

        merger = PdfMerger()

        for row in self.pdf_list:
            if row["widget"].isChecked():
                with open(row["path"], "rb") as pdf:
                    merger.append(pdf)

        with open(join_file, "wb") as output_file:
            merger.write(output_file)

        merger.close()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
