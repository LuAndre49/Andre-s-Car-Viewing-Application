from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QGridLayout, QSizePolicy, QLabel
from PySide6.QtCore import Qt
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

         # If no cars match, show a message
        if not data:
            no_cars_label = QLabel("No cars match your search criteria")
            no_cars_label.setStyleSheet("color: white; font-size: 14px;")
            no_cars_label.setAlignment(Qt.AlignCenter)
            self.grid_layout.addWidget(no_cars_label, 0, 0)
            return

        self.car_boxes = []
        for index, car in enumerate(data):
            row = index//self.max_cars_per_row
            col = index%self.max_cars_per_row
            box = CarBox(car, self.on_car_click, self.image_cache)
            self.car_boxes.append(box)
            self.grid_layout.addWidget(box, row, col)

    def search_cars(self, query, condition_filter):
        terms = query.lower().split()
        filtered = []

        for car in self.car_data_all:
            title = car['title'].lower()
            car_condition = car.get('condition', '').lower()
            
            # Check if search terms match and condition matches (if not 'both')
            if all(term in title for term in terms) and (condition_filter.lower() == 'both' or condition_filter.lower() == car_condition):
                filtered.append(car)

        self.display_cars(filtered)

    def refresh_all_prices(self):
        print("[DEBUG] refresh_all_prices called")
        for box in getattr(self, "car_boxes", []):
            print(f"[DEBUG] Updating price for car: {box.car_data.get('title')}")
            box.update_price()


    