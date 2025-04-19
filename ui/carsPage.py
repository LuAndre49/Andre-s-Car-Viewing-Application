from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from ui.car_widgets import CarBox

class CarsPage(QWidget):
    def __init__(self, car_data, on_car_click):
        super().__init__()

        layout = QVBoxLayout()
        
        # Scroll area for car listings
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout()

        # Create a CarBox for each car and add to layout
        for car in car_data:
            car_box = CarBox(car, on_car_click)
            container_layout.addWidget(car_box)

        container.setLayout(container_layout)
        scroll_area.setWidget(container)
        
        layout.addWidget(scroll_area)
        self.setLayout(layout)
