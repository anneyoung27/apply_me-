from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QDoubleValidator

class SalaryLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        # hanya angka dan desimal
        validator = QDoubleValidator(0.00, 999999999.99, 2)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.setValidator(validator)

        # listen perubahan
        self.textChanged.connect(self.format_live_input)

    def format_live_input(self, text):
        # hilangkan koma dulu
        clean = text.replace(",", "")

        if clean == "":
            return

        if clean.isdigit():
            # format ribuan
            formatted = f"{int(clean):,}"
            # remove .00 di realtime
            self.blockSignals(True)
            self.setText(formatted)
            self.blockSignals(False)

    def focusOutEvent(self, event):
        """
        Saat input kehilangan fokus:
        → auto tambahkan .00
        """
        text = self.text().replace(",", "")
        if text != "":
            try:
                value = float(text)
                formatted = f"{value:,.2f}"  # format final x,xxx.xx
                self.setText(formatted)
            except:
                pass

        super().focusOutEvent(event)
