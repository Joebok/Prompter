import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from prompter.main_window import MainWindow


def _icon_path() -> Path:
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    if sys.platform == "darwin":
        return base_path / "img" / "PrompterLogo_1024.icns"
    return base_path / "img" / "PrompterLogo_256.ico"


def main() -> int:
    app = QApplication([])
    app.setApplicationName("prompter")
    app.setOrganizationName("prompter")
    app.setWindowIcon(QIcon(str(_icon_path())))
    window = MainWindow()
    window.setWindowIcon(app.windowIcon())
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
