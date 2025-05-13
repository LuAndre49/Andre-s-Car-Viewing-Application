from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget
from app.gui.pages.cars_page import CarsPage
from app.gui.pages.car_detailed_page import CarDetailsPage
from app.gui.components.filter_bar import FilterBar

def show_car_details(car_data, ui):
    """
    Show car details in a new page when a car is selected.
    """
    details_page = CarDetailsPage(car_data)
    ui.mainPages.addWidget(details_page)
    ui.mainPages.setCurrentWidget(details_page)

def setup_cars_page(ui, car_data):
    """
    Set up the cars page UI elements: layout, search bar, and the car listings.
    """
    cars_page_layout = QVBoxLayout(ui.carsPage)

    # Existing search bar
    search_layout = QHBoxLayout()
    search_bar = QLineEdit()
    search_bar.setPlaceholderText("Search for a car here")
    search_bar.setFixedHeight(35)
    search_bar.setStyleSheet("""
        QLineEdit {
            padding: 8px;
            border-radius: 6px;
            border: 1px solid #4B5563;
            background-color: #1f2937; 
            color: white;
        }
    """)
    search_button = QPushButton("Search")
    search_layout.addWidget(search_bar)
    search_layout.addWidget(search_button)

    search_widget = QWidget()
    search_widget.setLayout(search_layout)
    cars_page_layout.addWidget(search_widget)

    # CarsPage
    image_cache = {}
    cars = CarsPage(car_data, lambda c: show_car_details(c, ui), image_cache)

    # FilterBar
    filter_bar = FilterBar(ui.carsPage)
    filter_bar.filterChanged.connect(lambda condition, brand: apply_filters(
        cars, car_data, condition, brand, search_bar.text()
    ))

    cars_page_layout.addWidget(filter_bar)
    cars_page_layout.addWidget(cars)

    # Connect search actions to the existing search bar
    search_button.clicked.connect(lambda: apply_filters(
        cars, car_data,
        filter_bar.condition_dropdown.currentText(),
        filter_bar.brand_dropdown.currentText(),
        search_bar.text()
    ))

    search_bar.returnPressed.connect(lambda: apply_filters(
        cars, car_data,
        filter_bar.condition_dropdown.currentText(),
        filter_bar.brand_dropdown.currentText(),
        search_bar.text()
    ))

    return cars

def perform_search(cars_page, car_data, filter_bar, search_bar):
    """
    Perform search with condition, brand, and search query.
    """
    condition = filter_bar.condition_dropdown.currentText()
    brand = filter_bar.brand_dropdown.currentText()
    search_query = search_bar.text()

    apply_filters(cars_page, car_data, condition, brand, search_query)

def apply_filters(cars_page, car_data, condition, brand, search_query=""):
    """
    Filter cars data based on the selected condition, brand, and search query.
    """
    filtered_data = car_data

    # Filter based on condition
    if condition != "Both":
        filtered_data = [car for car in filtered_data if car.get("condition", "") == condition]

    # Filter based on brand
    if brand and brand != "All":
        filtered_data = [car for car in filtered_data if car.get("brand", "").lower() == brand.lower()]

    # Filter based on search query
    if search_query:
        search_query = search_query.lower()
        filtered_data = [
            car for car in filtered_data
            if search_query in car.get("title", "").lower()
        ]

    # Update the displayed cars
    cars_page.display_cars(filtered_data)
