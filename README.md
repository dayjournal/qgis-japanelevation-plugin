# Japan Elevation Plugin

Read this in other languages: [Japanese](./README_ja.md)

![logo](img/logo.png)

Display elevation value of specified position on QGIS using [Elevation API](https://maps.gsi.go.jp/development/elevation_s.html) by Geospatial Information Authority of Japan (GSI).

## QGIS Python Plugins Repository

[Japan Elevation Pluginn](https://plugins.qgis.org/plugins/japan_elevation)  

## blog


## Usage

![menu](./img/menu.gif)

1. Click "Japan Elevation".
2. Click anywhere on the map canvas.
3. The elevation value and data source will be displayed in a dialog.

## Development

### Requirements

- [uv](https://docs.astral.sh/uv/)
- QGIS 3.x

### Setup

```bash
# Install dependencies
uv sync

# Lint
uv run ruff check .

# Format
uv run ruff format .
```

### Local Development

Create a symbolic link to the QGIS plugins directory:

**macOS:**
```bash
ln -s /path/to/japan_elevation ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/japan_elevation
```

**Windows:**
```powershell
mklink /D "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\japan_elevation" "C:\path\to\japan_elevation"
```

**Linux:**
```bash
ln -s /path/to/japan_elevation ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/japan_elevation
```

After editing the code, reload the plugin in QGIS to see the changes.

## License

Python modules are released under the GNU General Public License v2.0

Copyright (c) 2018-2026 Yasunori Kirimoto
