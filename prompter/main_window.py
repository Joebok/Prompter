from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from prompter.prompt_engine import (
    DEFAULT_CODEX_CONSTRAINTS,
    PromptRequest,
    TargetPreset,
    build_prompt,
)
from prompter.settings import AppSettings


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.settings = AppSettings()
        self.setWindowTitle("prompter")

        self.target_combo = QComboBox()
        self.target_combo.addItems([preset.value for preset in TargetPreset])

        self.run_tests_checkbox = QCheckBox("Run Tests")
        self.run_tests_checkbox.setToolTip(
            "When checked, the generated prompt asks the assistant to run the smallest relevant test set. "
            "When unchecked, it asks the assistant not to run tests unless necessary."
        )

        self.copy_button = QPushButton("Copy Prompt")
        self.copy_button.setDefault(True)
        self.clear_button = QPushButton("Clear")

        self.goal_edit = self._text_edit()
        self.context_edit = self._text_edit()
        self.constraints_edit = self._text_edit(DEFAULT_CODEX_CONSTRAINTS)
        self.success_edit = self._text_edit()
        self.preview_edit = self._text_edit(readonly=True)

        self._build_layout()
        self._restore_settings()
        self._connect_signals()
        self._add_shortcuts()
        self.update_preview()

    def closeEvent(self, event) -> None:
        self.settings.set_target(TargetPreset(self.target_combo.currentText()))
        self.settings.set_run_tests(self.run_tests_checkbox.isChecked())
        self.settings.set_window_size(self.size())
        super().closeEvent(event)

    def update_preview(self) -> None:
        request = PromptRequest(
            goal=self.goal_edit.toPlainText(),
            context=self.context_edit.toPlainText(),
            constraints=self.constraints_edit.toPlainText(),
            success=self.success_edit.toPlainText(),
            target=TargetPreset(self.target_combo.currentText()),
            run_tests=self.run_tests_checkbox.isChecked(),
        )
        self.preview_edit.setPlainText(build_prompt(request))

    def copy_prompt(self) -> None:
        QApplication.clipboard().setText(self.preview_edit.toPlainText())

    def clear_fields(self, confirm: bool = False) -> None:
        if confirm:
            result = QMessageBox.question(self, "Clear Fields", "Clear all prompt fields?")
            if result != QMessageBox.StandardButton.Yes:
                return
        for edit in (self.goal_edit, self.context_edit, self.constraints_edit, self.success_edit):
            edit.clear()
        self.update_preview()

    def _build_layout(self) -> None:
        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("Target:"))
        top_bar.addWidget(self.target_combo)
        top_bar.addSpacing(12)
        top_bar.addWidget(self.run_tests_checkbox)
        top_bar.addStretch(1)
        top_bar.addWidget(self.copy_button)

        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        self._add_labeled_edit(layout, "Goal:", self.goal_edit)
        self._add_labeled_edit(layout, "Context:", self.context_edit)
        self._add_labeled_edit(layout, "Constraints:", self.constraints_edit)
        self._add_labeled_edit(layout, "Success:", self.success_edit)
        self._add_labeled_edit(layout, "Generated Prompt:", self.preview_edit)
        layout.addWidget(self.clear_button, alignment=Qt.AlignmentFlag.AlignRight)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _restore_settings(self) -> None:
        self.resize(self.settings.window_size())
        self.target_combo.setCurrentText(self.settings.target().value)
        self.run_tests_checkbox.setChecked(self.settings.run_tests())

    def _connect_signals(self) -> None:
        for edit in (self.goal_edit, self.context_edit, self.constraints_edit, self.success_edit):
            edit.textChanged.connect(self.update_preview)
        self.target_combo.currentTextChanged.connect(self.update_preview)
        self.run_tests_checkbox.toggled.connect(self.update_preview)
        self.copy_button.clicked.connect(self.copy_prompt)
        self.clear_button.clicked.connect(self.clear_fields)

    def _add_shortcuts(self) -> None:
        QShortcut(QKeySequence("Ctrl+Return"), self, activated=self.copy_prompt)
        QShortcut(QKeySequence("Ctrl+Enter"), self, activated=self.copy_prompt)
        QShortcut(QKeySequence("Ctrl+L"), self, activated=lambda: self.clear_fields(True))
        QShortcut(QKeySequence("Ctrl+1"), self, activated=lambda: self._set_target(TargetPreset.CODEX))
        QShortcut(QKeySequence("Ctrl+2"), self, activated=lambda: self._set_target(TargetPreset.OLLAMA))
        QShortcut(QKeySequence("Ctrl+3"), self, activated=lambda: self._set_target(TargetPreset.VSCODE_CLAUDE))

    def _text_edit(self, text: str = "", readonly: bool = False) -> QTextEdit:
        edit = QTextEdit()
        edit.setPlainText(text)
        edit.setReadOnly(readonly)
        edit.setAcceptRichText(False)
        edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        return edit

    def _add_labeled_edit(self, layout: QVBoxLayout, label: str, edit: QTextEdit) -> None:
        layout.addWidget(QLabel(label))
        layout.addWidget(edit)

    def _set_target(self, target: TargetPreset) -> None:
        self.target_combo.setCurrentText(target.value)
