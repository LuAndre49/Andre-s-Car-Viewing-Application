########################################################################
## QT GUI BY SPINN TV(YOUTUBE)
########################################################################

########################################################################
## IMPORTS
########################################################################
import os
import sys
########################################################################
# IMPORT GUI FILE
from ui.ui_interface import *
########################################################################

########################################################################
# IMPORT Custom widgets
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from PySide6.QtCore import QEasingCurve

# For spider
from run_scraper import run_scraper
from load_car_data import load_car_listings
from ui.carsPage import CarsPage
from ui.carDetailsPage import CarDetailsPage
########################################################################

########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        loadJsonStyle(self, self.ui, jsonFiles = {
            "json-styles/style.json"
        }) 
        animatePageTransitions(self)
        run_scraper()
        car_data = load_car_listings()
        cars_layout = QVBoxLayout(self.ui.carsPage)  # <-- Add to existing QWidget
        self.cars_page = CarsPage(car_data, self.show_car_details)
        cars_layout.addWidget(self.cars_page)

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


########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ########################################################################
    ## 
    ########################################################################
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
########################################################################
## END===>
########################################################################  
