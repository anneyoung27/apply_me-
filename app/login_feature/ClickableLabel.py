from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QCursor

class ClickableLabel(QLabel):
    clicked = Signal()

    def __init__(self, text=""):
        super().__init__(text)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mousePressEvent(self, event):
        self.clicked.emit()
