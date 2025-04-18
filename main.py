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
########################################################################

########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ########################################################################
        # APPLY JSON STYLESHEET
        ########################################################################
        # self = QMainWindow class
        # self.ui = Ui_MainWindow / user interface class
        #Use this if you only have one json file named "style.json" inside the root directory, "json" directory or "jsonstyles" folder.
        # loadJsonStyle(self, self.ui) 

        # Use this to specify your json file(s) path/name
        loadJsonStyle(self, self.ui, jsonFiles = {
            "json-styles/style.json"
        }) 
        
        animatePageTransitions(self)
        ########################################################################

        #######################################################################
        # SHOW WINDOW
        #######################################################################
        self.show() 

        ########################################################################
        # UPDATE APP SETTINGS LOADED FROM JSON STYLESHEET 
        # ITS IMPORTANT TO RUN THIS AFTER SHOWING THE WINDOW
        # THIS PROCESS WILL RUN ON A SEPARATE THREAD WHEN GENERATING NEW ICONS
        # TO PREVENT THE WINDOW FROM BEING UNRESPONSIVE
        ########################################################################
        # self = QMainWindow class
        QAppSettings.updateAppSettings(self)

def animatePageTransitions(self):
    if hasattr(self.ui, 'mainPages'):  
        stacked = self.ui.mainPages
        
        
        stacked.setSlideTransition(True)
        stacked.setFadeTransition(False)
        
        # Set animation properties
        stacked.setTransitionSpeed(300)  # Duration in ms
        stacked.setTransitionDirection(Qt.Horizontal)  
        
        # Set easing curve
        
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
