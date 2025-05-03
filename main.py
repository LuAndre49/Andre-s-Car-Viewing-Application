# IMPORTS
import os
import sys

# IMPORT GUI FILE
from app.gui.ui_interface import *
# IMPORT Custom widgets
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from PySide6.QtCore import QEasingCurve

from app.etl.etl import run_etl
from app.gui.utils.db_reader import fetch_car_data
from app.gui.pages.cars_page import CarsPage
from app.gui.pages.car_detailed_page import CarDetailsPage

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.setup_database_table_view() 

        loadJsonStyle(self, self.ui, jsonFiles = {
            "app/styles/style.json"
        }) 

        # Add page animations
        animatePageTransitions(self)

        # Run scraper then save car data
        #run_scraper()
        #car_data = extract_car_listings()
        run_etl()
        car_data = fetch_car_data()
        # Create vertical box layout to contain the search bar and cars to be displayed in the cars page
        cars_page_layout = QVBoxLayout(self.ui.carsPage) 
        
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

        image_cache = {}
        cars = CarsPage(car_data, self.show_car_details, image_cache)
        cars_page_layout.addWidget(cars)
        search_button.clicked.connect(lambda: cars.filter_cars(search_bar.text()))
        search_bar.returnPressed.connect(lambda: cars.filter_cars(search_bar.text()))

        self.show() 

        # self = QMainWindow class
        QAppSettings.updateAppSettings(self)

    def show_car_details(self, car_data):
        
        self.details_page = CarDetailsPage(car_data)
        self.ui.mainPages.addWidget(self.details_page)
        self.ui.mainPages.setCurrentWidget(self.details_page)

def animatePageTransitions(self):
    if hasattr(self.ui, 'mainPages'):  
        stacked = self.ui.mainPages
        
        
        stacked.setSlideTransition(True)
        stacked.setFadeTransition(False)
        stacked.setTransitionSpeed(300) 
        stacked.setTransitionDirection(Qt.Horizontal)
        
        stacked.setTransitionEasingCurve(QEasingCurve.OutBack)
        
        # Connect navigation buttons
        button_map = {
            "homeBtn": "homePage",
            "carsBtn": "carsPage",
            "compareBtn": "comparePage",
            "newsBtn": "newsPage",
            "accountBtn": "accountPage",
            "aboutBtn": "aboutPage",
            "settingsBtn": "settingsPage",
            "helpBtn": "helpPage"
        }
        
        for btn_name, page_name in button_map.items():
            if hasattr(self.ui, btn_name) and hasattr(self.ui, page_name):
                getattr(self.ui, btn_name).clicked.connect(
                    lambda _, p=page_name: stacked.slideToWidget(getattr(self.ui, p))
                )

# EXECUTE APP
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
  
