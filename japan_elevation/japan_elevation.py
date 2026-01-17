import os
from typing import Callable, Optional

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget

from .ui.dialog.dialog import ElevationDialog
from .utils.click_handler import ElevationClickHandler


class JapanElevation:
    """
    QGIS Plugin for displaying elevation values using GSI Japan Elevation API.

    This plugin allows users to click on the map canvas and retrieve
    elevation data from the Geospatial Information Authority of Japan.
    """

    PLUGIN_NAME = "Japan Elevation"

    def __init__(self, iface) -> None:
        """
        Initializes the plugin interface, setting up UI components
        and internal variables.
        """
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.main_window = self.iface.mainWindow()
        self.plugin_directory = os.path.dirname(__file__)
        self.actions: list[QAction] = []
        self.toolbar = self.iface.addToolBar(self.PLUGIN_NAME)
        self.toolbar.setObjectName(self.PLUGIN_NAME)
        self.dialog = ElevationDialog()
        self.dialog.hide()
        self.click_handler: Optional[ElevationClickHandler] = None

    def add_action(
        self,
        icon_path: str,
        text: str,
        callback: Callable,
        enabled_flag: bool = True,
        add_to_menu: bool = True,
        add_to_toolbar: bool = True,
        status_tip: Optional[str] = None,
        whats_this: Optional[str] = None,
        parent: Optional[QWidget] = None,
    ) -> QAction:
        """
        Adds an action to the plugin menu and toolbar.

        Args:
            icon_path (str): Path to the icon file.
            text (str): Display text for the action.
            callback (Callable): Function to call when action is triggered.
            enabled_flag (bool): Whether the action is enabled by default.
            add_to_menu (bool): Whether to add the action to the menu.
            add_to_toolbar (bool): Whether to add the action to the toolbar.
            status_tip (Optional[str]): Text for status bar on hover.
            whats_this (Optional[str]): Longer description of the action.
            parent (Optional[QWidget]): Parent widget for the action.

        Returns:
            QAction: The created action.
        """
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        if add_to_menu:
            self.iface.addPluginToMenu(self.PLUGIN_NAME, action)
        if add_to_toolbar:
            self.toolbar.addAction(action)

        self.actions.append(action)
        return action

    def initGui(self) -> None:
        """
        Initializes the GUI components and adds actions to the interface.
        """
        icon_path = os.path.join(self.plugin_directory, "ui", "icon.png")
        self.add_action(
            icon_path=icon_path,
            text=self.PLUGIN_NAME,
            callback=self.run,
            status_tip="Click on map to get elevation",
            whats_this="Display elevation value using GSI Japan Elevation API",
            parent=self.main_window,
        )

    def unload(self) -> None:
        """
        Cleans up the plugin interface by removing actions and toolbar.
        """
        for action in self.actions:
            self.iface.removePluginMenu(self.PLUGIN_NAME, action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self) -> None:
        """
        Activates the elevation click tool on the map canvas.
        """
        self.click_handler = ElevationClickHandler(
            iface=self.iface,
            canvas=self.canvas,
            dialog=self.dialog,
        )
        self.canvas.setMapTool(self.click_handler)
