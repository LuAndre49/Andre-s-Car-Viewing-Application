from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QGridLayout, QSizePolicy
from app.gui.components.car_widgets import CarBox


class CarsPage(QWidget):
    def __init__(self, car_data, on_car_click, image_cache):
        super().__init__()
        self.car_data_all = car_data
        self.on_car_click = on_car_click
        self.image_cache = image_cache
        self.max_cars_per_row = 3
        

        self.page_layout = QVBoxLayout(self)
        
        # Scroll area for car listings
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.container = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(15)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)

        self.container.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.container)
        self.page_layout.addWidget(self.scroll_area)
        self.setLayout(self.page_layout)
        
        self.display_cars(self.car_data_all)
    def display_cars(self, data):
        while self.grid_layout.count() > 0:
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for index, car in enumerate(data):
            row = index//self.max_cars_per_row
            col = index%self.max_cars_per_row
            box = CarBox(car, self.on_car_click, self.image_cache)
            self.grid_layout.addWidget(box, row, col)

    def filter_cars(self, query):
        terms = query.lower().split()
        filtered = []

        for car in self.car_data_all:
            title = car['title'].lower()
            if all(term in title for term in terms):
                filtered.append(car)
        self.display_cars(filtered)

    