from PySide6.QtCore import Qt, QEasingCurve

def setup_page_transitions(window: object):
    stacked = window.ui.mainPages
    stacked.setSlideTransition(True)
    stacked.setFadeTransition(False)
    stacked.setTransitionSpeed(300)
    stacked.setTransitionDirection(Qt.Horizontal)
    stacked.setTransitionEasingCurve(QEasingCurve.OutBack)

    nav_map = {
        "homeBtn": "homePage",
        "carsBtn": "carsPage",
        "compareBtn": "comparePage",
        "newsBtn": "newsPage",
        "accountBtn": "accountPage",
        "aboutBtn": "aboutPage",
        "settingsBtn": "settingsPage",
        "helpBtn": "helpPage"
    }

    for btn_name, page_name in nav_map.items():
        if hasattr(window.ui, btn_name) and hasattr(window.ui, page_name):
            getattr(window.ui, btn_name).clicked.connect(
                lambda _, p=page_name: stacked.slideToWidget(getattr(window.ui, p))
            )
