import os

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), "dialog.ui"))


class ElevationDialog(QDialog, FORM_CLASS):
    """
    Dialog for displaying elevation information.

    Shows the elevation value and data source from the GSI API.
    """

    def __init__(self, parent=None) -> None:
        """
        Initializes the elevation dialog by loading the UI components.
        """
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # type: ignore
        self.setupUi(self)

    def set_elevation(self, value: str) -> None:
        """
        Sets the elevation value display.
        """
        self.label_elevation_value.setText(value)

    def set_data_source(self, value: str) -> None:
        """
        Sets the data source display.
        """
        self.label_data_value.setText(value)
