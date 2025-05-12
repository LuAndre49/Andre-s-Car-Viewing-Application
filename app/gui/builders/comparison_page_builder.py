from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QLabel, QSplitter
from PySide6.QtCore import Qt
from app.gui.components.filter_bar import FilterBar
from app.gui.components.comparison_car_selector import ComparisonCarSelector
from app.gui.components.comparison_panel import ComparisonPanel

def setup_comparison_page(ui, car_data):
    comparison_page_layout = QVBoxLayout(ui.comparePage)
    splitter = QSplitter(Qt.Horizontal)

    # Create both panels using shared setup function
    left_selector, left_filter_bar, left_search_bar = create_selector_panel("First Car", car_data, splitter, ui)
    right_selector, right_filter_bar, right_search_bar = create_selector_panel("Second Car", car_data, splitter, ui)

    # Setup search functionality for left
    def perform_left_search():
        condition = get_selected_condition(left_filter_bar)
        left_selector.search_cars(left_search_bar.text(), condition.lower())
    
    # Setup search functionality for right
    def perform_right_search():
        condition = get_selected_condition(right_filter_bar)
        right_selector.search_cars(right_search_bar.text(), condition.lower())

    left_filter_bar.filterChanged.connect(lambda condition, _: apply_filters(left_selector, car_data, condition))
    right_filter_bar.filterChanged.connect(lambda condition, _: apply_filters(right_selector, car_data, condition))

    left_search_bar.returnPressed.connect(perform_left_search)
    right_search_bar.returnPressed.connect(perform_right_search)

    # Final layout
    comparison_page_layout.addWidget(splitter)

    # Comparison panel
    comparison_panel = ComparisonPanel()
    comparison_page_layout.addWidget(comparison_panel)
    comparison_panel.hide()

    # Selection signals
    left_selector.car_selected.connect(lambda car: handle_car_selection(car, "left", left_selector, right_selector, comparison_panel))
    right_selector.car_selected.connect(lambda car: handle_car_selection(car, "right", left_selector, right_selector, comparison_panel))

    return comparison_page_layout

def create_selector_panel(title, car_data, splitter, ui):
    panel = QWidget()
    layout = QVBoxLayout(panel)

    label = QLabel(title)
    label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
    layout.addWidget(label)

    # Search bar
    search_bar = QLineEdit()
    search_bar.setPlaceholderText(f"Search for {title.lower()}")
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
    search_button.setStyleSheet("""
        QPushButton {
            background-color: #059669;
            color: white;
            border-radius: 6px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: #10b981;
        }
    """)

    search_layout = QHBoxLayout()
    search_layout.addWidget(search_bar)
    search_layout.addWidget(search_button)
    search_widget = QWidget()
    search_widget.setLayout(search_layout)
    layout.addWidget(search_widget)

    selector = ComparisonCarSelector(car_data, "left" if "First" in title else "right")

    # Filter bar
    filter_bar = FilterBar(panel)
    filter_bar.filterChanged.connect(lambda condition, _: apply_filters(selector, car_data, condition))

    layout.addWidget(filter_bar)
    layout.addWidget(selector)

    # Connect search button separately
    search_button.clicked.connect(lambda: perform_search(search_bar, filter_bar, selector, car_data))

    splitter.addWidget(panel)
    return selector, filter_bar, search_bar

def perform_search(search_bar, filter_bar, selector, car_data):
    """
    Handles search functionality using the original search bar and filters.
    """
    condition = filter_bar.condition_dropdown.currentText()
    search_query = search_bar.text()
    apply_filters(selector, car_data, condition, search_query)

def get_selected_condition(filter_bar):
    return filter_bar.condition_dropdown.currentText()

def apply_filters(selector, car_data, condition, search_query=""):
    filtered = car_data

    # Filter based on condition
    if condition != 'Both':
        filtered = [car for car in car_data if car.get("condition", "").lower() == condition.lower()]

    # Filter based on search query
    if search_query:
        search_query = search_query.lower()
        filtered = [
            car for car in filtered
            if search_query in car.get("title", "").lower()
            or search_query in car.get("model", "").lower()
        ]

    selector.display_cars(filtered)

def handle_car_selection(car, side, left_selector, right_selector, comparison_panel):
    if side == "left":
        comparison_panel.set_left_car(car)
    else:
        comparison_panel.set_right_car(car)

    if comparison_panel.left_car and comparison_panel.right_car:
        comparison_panel.update_comparison()
        comparison_panel.show()
