from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QComboBox, QLineEdit, QFormLayout, \
    QFileDialog, QMessageBox

from app.import_feature.CSVFieldMappingWindow import CSVFieldMappingWindow


class CSVSettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("File import")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        header = QLabel("<h2>File import</h2>")
        desc = QLabel(
            "You are about to start the CSV file import process. "
            "To learn more about it, please read our documentation."
        )
        desc.setWordWrap(True)

        # ---- Choose File ----
        file_layout = QHBoxLayout()
        self.btn_choose = QPushButton("Choose File")
        self.btn_choose.clicked.connect(self.choose_file)
        self.file_label = QLabel("No file selected")

        file_layout.addWidget(self.btn_choose)
        file_layout.addWidget(self.file_label)

        # ---- Encoding ----
        self.encoding = QComboBox()
        self.encoding.addItems(["UTF-8"])
        self.encoding.setDisabled(True)

        # ---- Delimiters ----
        self.csv_delim = QLineEdit(",")
        self.csv_delim.setDisabled(True)
        self.list_delim = QLineEdit(";")
        self.list_delim.setDisabled(True)

        form = QFormLayout()
        form.addRow("File:", file_layout)
        form.addRow("File Encoding", self.encoding)
        form.addRow("CSV Delimiter", self.csv_delim)
        form.addRow("List value delimiter", self.list_delim)

        # ---- Buttons ----
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_back = QPushButton("Back")
        btn_next = QPushButton("Next")
        btn_next.setStyleSheet("background-color: #1976d2; color: white;")

        btn_back.clicked.connect(self.go_back)
        btn_next.clicked.connect(self.go_next)

        btn_layout.addWidget(btn_back)
        btn_layout.addWidget(btn_next)

        layout.addWidget(header)
        layout.addWidget(desc)
        layout.addSpacing(15)
        layout.addLayout(form)
        layout.addSpacing(10)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.selected_file = None

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose CSV File",
            "",
            "CSV Files (*.csv)"
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path.split("/")[-1])

    def go_back(self):
        # self.close()
        #
        # parent = self.parent()
        # if parent:
        #     parent.exec()
        self.close()
        parent = self.parent()
        if parent and isinstance(parent, QDialog):
            parent.show()


    def go_next(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please choose a file first.")
            return

        # tutup settings window (secara benar)
        self.done(QDialog.Accepted)

        mapping_win = CSVFieldMappingWindow(self.parent(), self.selected_file)
        mapping_win.exec()

