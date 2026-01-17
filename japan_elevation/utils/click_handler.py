import json
import urllib.error
import urllib.request
from typing import Any

from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject
from qgis.gui import QgsMapCanvas, QgsMapMouseEvent, QgsMapTool


class ElevationClickHandler(QgsMapTool):
    """
    Map tool for handling click events and fetching elevation data.

    This tool transforms clicked coordinates to WGS84 and queries
    the GSI Japan Elevation API for elevation information.
    """

    GSI_API_URL = (
        "https://cyberjapandata2.gsi.go.jp/general/dem/scripts/getelevation.php"
    )

    def __init__(self, iface, canvas: QgsMapCanvas, dialog) -> None:
        """
        Initializes the click handler with map canvas and dialog references.
        """
        super().__init__(canvas)
        self.iface = iface
        self.canvas = canvas
        self.dialog = dialog

    def canvasPressEvent(self, event: QgsMapMouseEvent) -> None:
        """
        Processes mouse press events on the map canvas, converting the click location
        to WGS84 coordinates and fetching elevation data.
        """
        self.dialog.show()

        try:
            lon, lat = self._get_wgs84_coordinates(event)
            elevation_data = self._fetch_elevation(lon, lat)
            self._update_dialog(elevation_data)
        except urllib.error.URLError as e:
            self._show_error(f"Network error: {e}")
        except json.JSONDecodeError as e:
            self._show_error(f"Invalid response: {e}")
        except Exception as e:
            self._show_error(f"Error: {e}")

    def _get_wgs84_coordinates(self, event: QgsMapMouseEvent) -> tuple[float, float]:
        """
        Transforms clicked position to WGS84 coordinates.

        Args:
            event (QgsMapMouseEvent): The mouse event containing click position.

        Returns:
            tuple[float, float]: A tuple of (longitude, latitude) in WGS84.
        """
        click_position = event.pos()
        map_position = self.toMapCoordinates(click_position)

        source_crs = self.canvas.mapSettings().destinationCrs()
        target_crs = QgsCoordinateReferenceSystem(4326)
        transform = QgsCoordinateTransform(
            source_crs, target_crs, QgsProject.instance()
        )

        wgs84_position = transform.transform(map_position)
        return wgs84_position.x(), wgs84_position.y()

    def _fetch_elevation(self, lon: float, lat: float) -> dict[str, Any]:
        """
        Fetches elevation data from the GSI API.

        Args:
            lon (float): Longitude in WGS84.
            lat (float): Latitude in WGS84.

        Returns:
            dict[str, Any]: Dictionary containing elevation data from the API.
        """
        url = f"{self.GSI_API_URL}?lon={lon}&lat={lat}&outtype=JSON"

        with urllib.request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))

    def _update_dialog(self, data: dict[str, Any]) -> None:
        """
        Updates the dialog with elevation data.
        """
        elevation = data.get("elevation", "N/A")
        if elevation != "-----":
            elevation_text = f"{elevation} m"
        else:
            elevation_text = "No data"

        data_source = data.get("hsrc", "Unknown")

        self.dialog.set_elevation(elevation_text)
        self.dialog.set_data_source(data_source)
        self.dialog.show()

    def _show_error(self, message: str) -> None:
        """
        Displays an error message in the dialog.
        """
        self.dialog.set_elevation("Error")
        self.dialog.set_data_source(message)
        self.dialog.show()
