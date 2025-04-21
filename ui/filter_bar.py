from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton,
    QRadioButton, QButtonGroup, QComboBox, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtCore import Qt, Signal

class FilterBar(QWidget):
    searchTriggered =  Signal()
    def __init__(self,parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search cars...")
        self.search_bar.setMinimumWidth(200)
        layout.addWidget(self.search_bar)
        # Condition filters (New, Used, Both)
        self.radio_both = QRadioButton("Both")
        self.radio_new = QRadioButton("New")
        self.radio_used = QRadioButton("Used")
        self.radio_both.setChecked(True)

        self.condition_group = QButtonGroup(self)
        self.condition_group.addButton(self.radio_both)
        self.condition_group.addButton(self.radio_new)
        self.condition_group.addButton(self.radio_used)

        # Now that they're defined, you can add them to the layout
        condition_widget = QWidget()
        condition_layout = QHBoxLayout(condition_widget)
        condition_layout.setContentsMargins(0, 0, 0, 0)
        condition_layout.setSpacing(5)
        condition_layout.addWidget(self.radio_both)
        condition_layout.addWidget(self.radio_new)
        condition_layout.addWidget(self.radio_used)

        layout.addWidget(condition_widget)


        layout.addWidget(condition_widget)


        self.brand_combo = QComboBox()
        self.brand_combo.addItems(["Toyota", "Ford", "Honda", "Mitsubishi", "Hyundai", "Nissan", "Mazda", "Subaru", "Suzuki", "Kia",
                                   "Chevrolet", "BMW", "Geely", "Isuzu", "MG", "Mercedes-Benz", "Lexus", "Jeep", "Volkswagen", "Porsche", 
                                   "Audi", "Mini", "Land Rover", "Chery", "Lamborghini", "Dodge", "Cadillac"])
        layout.addWidget(self.brand_combo)

        self.price_min = QComboBox()
        self.price_min.addItem("From price")
        self.price_max = QComboBox()
        self.price_max.addItem("To price")
        layout.addWidget(self.price_min)
        layout.addWidget(self.price_max)

        self.year_min = QComboBox()
        self.year_min.addItem("From year")
        self.year_max = QComboBox()
        self.year_max.addItem("To year")
        layout.addWidget(self.year_min)
        layout.addWidget(self.year_max)

        self.km_min = QComboBox()
        self.km_min.addItem("From km")
        self.km_max = QComboBox()
        self.km_max.addItem("To km")
        layout.addWidget(self.km_min)
        layout.addWidget(self.km_max)

        self.transmission_combo = QComboBox()
        self.transmission_combo.addItem("Transmission")
        layout.addWidget(self.transmission_combo)

        self.search_button = QPushButton("Search")
        layout.addWidget(self.search_button)

        
        # Connect enter key
        self.search_button.clicked.connect(self.search_button_click)
        self.search_bar.returnPressed.connect(self.search_button.click)

    def search_button_click(self):
        self.searchTriggered.emit()
