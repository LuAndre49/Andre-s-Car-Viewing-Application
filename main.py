import os
import sys

# IMPORT GUI FILE
from app.gui.ui_interface import *
from app.gui.components.custom_widgets import SlideMenu, AnimatedStackedWidget, ButtonGroup

from PySide6.QtCore import QEasingCurve
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtGui import QIcon
from app.etl.etl import run_etl
from app.gui.utils.db_reader import fetch_car_data
from app.gui.builders.cars_page_builder import setup_cars_page

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect signals to the custom widgets
        self._connect_signals()
        
        # Run ETL process to prepare data
        run_etl()
        
        # Setup the database table view
        self.ui.setup_database_table_view()
        
        # Get car data and set up cars page
        car_data = fetch_car_data()
        cars_page_widget = setup_cars_page(self.ui, car_data)
        self.ui.set_cars_page(cars_page_widget)
        
        # Connect currency selector signal
        self.ui.currency_selector.currentTextChanged.connect(self.ui.change_currency)
        
        # Show the window
        self.show()
    
    def _connect_signals(self):
        """Connect all signals for the custom widgets."""
        # Make sure the menu buttons are connected
        self.ui.menuBtn.clicked.connect(self.ui.leftMenu.toggle)
        self.ui.showUserFormBtn.clicked.connect(self.ui.rightMenu.toggle)
        
        # Ensure the navigation buttons are properly connected to the stacked widget
        button_page_map = {
            self.ui.homeBtn: 0,
            self.ui.carsBtn: 1, 
            self.ui.compareBtn: 2,
            self.ui.newsBtn: 3,
            self.ui.accountBtn: 4,
            self.ui.settingsBtn: 5,
            self.ui.helpBtn: 6,
            self.ui.aboutBtn: 7,
        }
        
        # Connect each button's clicked signal manually
        for button, page_index in button_page_map.items():
            button.clicked.connect(lambda checked=False, idx=page_index: self._goto_page(idx))
    
    def _goto_page(self, index):
        """Navigate to the specified page and update active button."""
        self.ui.mainPages.slide_to_index(index)
        
        # Set the active button based on index
        buttons = [
            self.ui.homeBtn, self.ui.carsBtn, self.ui.compareBtn, 
            self.ui.newsBtn, self.ui.accountBtn, self.ui.settingsBtn, 
            self.ui.helpBtn, self.ui.aboutBtn
        ]
        
        if 0 <= index < len(buttons):
            self.ui.nav_button_group.set_active(buttons[index])

# EXECUTE APP
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())