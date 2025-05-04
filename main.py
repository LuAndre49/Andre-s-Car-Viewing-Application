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
from app.gui.builders.transition_animator import setup_page_transitions
from app.gui.builders.cars_page_builder import setup_cars_page  # <-- Import updated function

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        

        loadJsonStyle(self, self.ui, jsonFiles={"app/styles/style.json"})

        setup_page_transitions(self)
        
        run_etl()
        self.ui.setup_database_table_view()
        car_data = fetch_car_data()

        #setup_cars_page(self.ui, car_data) 
        #self.ui.set_cars_page(self.ui.carsPage)
        cars_page_widget = setup_cars_page(self.ui, car_data)
        self.ui.set_cars_page(cars_page_widget)

        self.show()

        QAppSettings.updateAppSettings(self)

# EXECUTE APP
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
