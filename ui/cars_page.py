from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QGridLayout, QSizePolicy
from ui.car_widgets import CarBox


class CarsPage(QWidget):
    def __init__(self, car_data, on_car_click):
        super().__init__()

        layout = QVBoxLayout(self)
        
        # Scroll area for car listings
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        grid_layout = QGridLayout()

        # Number of cars per row
        max_cars_per_row = 3
        # For each car
        for index, car in enumerate(car_data):
            # Compute their position in the grid
            row = index // max_cars_per_row
            col = index % max_cars_per_row
            # Create car box for them to be added to the grid
            car_box = CarBox(car, on_car_click)
            car_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            grid_layout.addWidget(car_box, row, col)

        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(20)
        grid_layout.setContentsMargins(10,10,10,10)
        container.setLayout(grid_layout)
        scroll_area.setWidget(container)
        
        layout.addWidget(scroll_area)
        self.setLayout(layout)
