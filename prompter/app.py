from PySide6.QtWidgets import QApplication

from Prompter.main_window import MainWindow


def main() -> int:
    app = QApplication([])
    app.setApplicationName("Prompter")
    app.setOrganizationName("Prompter")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
