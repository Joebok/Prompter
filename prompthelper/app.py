from PySide6.QtWidgets import QApplication

from prompthelper.main_window import MainWindow


def main() -> int:
    app = QApplication([])
    app.setApplicationName("PromptHelper")
    app.setOrganizationName("PromptHelper")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
