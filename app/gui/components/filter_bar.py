from PySide6.QtWidgets import QWidget, QHBoxLayout, QRadioButton, QButtonGroup, QPushButton
from PySide6.QtCore import Signal

class FilterBar(QWidget):
    searchTriggered = Signal()

    def __init__(self, parent=None, on_filter_change=None):
        super().__init__(parent)
        
        self.on_filter_change = on_filter_change

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Condition filters (New, Used, Both)
        self.radio_both = QRadioButton("Both")
        self.radio_new = QRadioButton("New")
        self.radio_used = QRadioButton("Used")
        self.radio_both.setChecked(True)

        self.condition_group = QButtonGroup(self)
        self.condition_group.addButton(self.radio_both)
        self.condition_group.addButton(self.radio_new)
        self.condition_group.addButton(self.radio_used)

        condition_widget = QWidget()
        condition_layout = QHBoxLayout(condition_widget)
        condition_layout.setContentsMargins(0, 0, 0, 0)
        condition_layout.setSpacing(5)
        condition_layout.addWidget(self.radio_both)
        condition_layout.addWidget(self.radio_new)
        condition_layout.addWidget(self.radio_used)

        layout.addWidget(condition_widget)

        # Connect to signal
        self.condition_group.buttonClicked.connect(self.on_filter_changed)

    def on_filter_changed(self):
        selected_condition = None
        if self.radio_new.isChecked():
            selected_condition = 'New'
        elif self.radio_used.isChecked():
            selected_condition = 'Used'
        else:
            selected_condition = 'Both'
        
        if self.on_filter_change:
            self.on_filter_change(selected_condition)
