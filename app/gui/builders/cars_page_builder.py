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
    # Create vertical box layout to contain the search bar and cars to be displayed in the cars page
    cars_page_layout = QVBoxLayout(ui.carsPage)
    
    # Create search bar and button layout
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
    
    # Wrap the search layout in a widget and add it to the page layout
    search_widget = QWidget()
    search_widget.setLayout(search_layout)
    cars_page_layout.addWidget(search_widget)
    
    # Initialize the CarsPage widget
    image_cache = {}
    
    cars = CarsPage(car_data, lambda c: show_car_details(c, ui), image_cache)
    
    # Create and add the filter bar (add it before adding cars widget)
    filter_bar = FilterBar(ui.carsPage, lambda condition: apply_filters(cars, car_data, condition))
    cars_page_layout.addWidget(filter_bar)
    
    # Add cars widget after filter bar
    cars_page_layout.addWidget(cars)
    
    # Connect the search button and search bar to filter cars based on input
    def perform_search():
        condition = 'Both'
        if filter_bar.radio_new.isChecked():
            condition = 'New'
        elif filter_bar.radio_used.isChecked():
            condition = 'Used'
        
        # Make sure to convert condition to lowercase to match car_condition in search_cars
        cars.search_cars(search_bar.text(), condition.lower())
        
    search_button.clicked.connect(perform_search)
    search_bar.returnPressed.connect(perform_search)
    
    return cars

def apply_filters(cars_page, car_data, condition):
    """
    Apply the selected filters and update the car listings on the page.
    """
    filtered_data = car_data

    if condition != 'Both':
        filtered_data = [car for car in car_data if car.get("condition", "") == condition]

    cars_page.display_cars(filtered_data)