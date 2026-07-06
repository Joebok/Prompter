from PySide6.QtWidgets import QApplication

from prompter.main_window import MainWindow


def main() -> int:
    app = QApplication([])
    app.setApplicationName("prompter")
    app.setOrganizationName("prompter")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
