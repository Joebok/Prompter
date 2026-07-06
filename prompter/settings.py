from PySide6.QtCore import QSize
from PySide6.QtCore import QSettings

from prompter.prompt_engine import TargetPreset


class AppSettings:
    def __init__(self) -> None:
        self._settings = QSettings()

    def target(self) -> TargetPreset:
        value = self._settings.value("target", TargetPreset.CODEX.value)
        try:
            return TargetPreset(value)
        except ValueError:
            return TargetPreset.CODEX

    def set_target(self, target: TargetPreset) -> None:
        self._settings.setValue("target", target.value)

    def run_tests(self) -> bool:
        return self._settings.value("run_tests", True, type=bool)

    def set_run_tests(self, run_tests: bool) -> None:
        self._settings.setValue("run_tests", run_tests)

    def window_size(self) -> QSize:
        return self._settings.value("window_size", QSize(900, 800), type=QSize)

    def set_window_size(self, size: QSize) -> None:
        self._settings.setValue("window_size", size)
