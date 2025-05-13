from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, 
                             QLabel, QPushButton, QFrame, QGridLayout)
from PySide6.QtCore import Qt, QThreadPool, Signal
from PySide6.QtGui import QPixmap
from app.gui.components.car_widgets import ImageLoader
from app.settings.app_settings import app_settings

class ComparisonPanel(QWidget):
    reset_left_car = Signal()
    reset_right_car = Signal()
    
    def __init__(self):
        super().__init__()
        self.left_car = None
        self.right_car = None
        self.threadpool = QThreadPool.globalInstance()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Heading
        heading_layout = QHBoxLayout()
        comparison_heading = QLabel("Car Comparison")
        comparison_heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        comparison_heading.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white;
        """)
        
        reset_button = QPushButton("Reset Comparison")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border-radius: 6px;
                padding: 6px 10px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        reset_button.clicked.connect(self.reset_comparison)
        
        heading_layout.addWidget(comparison_heading)
        heading_layout.addStretch()
        heading_layout.addWidget(reset_button)
        
        main_layout.addLayout(heading_layout)
        
        
        # Empty state message - Initially visible
        self.empty_state = QLabel(
            "Select cars from both sides to see a detailed comparison.\n"
            "The comparison will display automatically as you make your selections."
        )
        self.empty_state.setAlignment(Qt.AlignCenter)
        self.empty_state.setStyleSheet("""
            color: #94a3b8;
            font-size: 16px;
            padding: 40px;
            background-color: #1e293b;
            border-radius: 8px;
            margin: 20px 0;
        """)
        main_layout.addWidget(self.empty_state)
        
        # Scroll area for comparison content - Initially hidden
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #1f2937;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #374151;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.comparison_container = QWidget()
        self.comparison_layout = QVBoxLayout(self.comparison_container)
        
        # Car images and names section
        self.cars_header = QHBoxLayout()
        
        # VS label
        vs_label = QLabel("VS")
        vs_label.setAlignment(Qt.AlignCenter)
        vs_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #ff9800;
        """)
        # Partial comparison message
        self.partial_message = QLabel("")
        self.partial_message.setAlignment(Qt.AlignCenter)
        self.partial_message.setStyleSheet("""
            color: #94a3b8;
            padding: 20px;
            font-size: 14px;
            margin: 10px 0;
        """)
        self.comparison_layout.addWidget(self.partial_message)
        
        # Categories grid for comparison data
        self.comparison_grid = QGridLayout()
        self.comparison_grid.setSpacing(10)
        self.comparison_grid.setContentsMargins(0, 20, 0, 0)
        
        # Add empty grid as placeholder
        self.comparison_layout.addLayout(self.comparison_grid)
        
        # Set up the scroll area
        self.scroll_area.setWidget(self.comparison_container)
        main_layout.addWidget(self.scroll_area)
        
        
        self.setLayout(main_layout)
        
    def set_left_car(self, car):
        self.left_car = car
        self.update_display_state()
        
    def set_right_car(self, car):
        self.right_car = car
        self.update_display_state()
    
    def update_display_state(self):
        """Update visibility of elements based on car selection state"""
        # Always show the comparison view
        self.empty_state.show() if not self.left_car and not self.right_car else self.empty_state.hide()
        self.scroll_area.show()

        
        if not self.left_car and not self.right_car:
            # No cars selected, show empty guidance
            self.partial_message.setText("Select cars from both sides to see a detailed comparison")
            self.partial_message.show()
            self.clear_comparison_grid()
        elif self.left_car and self.right_car:
            # Both cars selected, show full comparison
            self.partial_message.hide()
            self.update_comparison()
        else:
            # Only one car selected, show partial message
            if self.left_car:
                self.partial_message.setText("Left car selected. Now select a right car to compare")
            else:
                self.partial_message.setText("Right car selected. Now select a left car to compare")
            self.partial_message.show()
            self.clear_comparison_grid()
    
    def reset_comparison(self):
        self.reset_left_car_selection()  
        self.reset_right_car_selection()
        self.update_display_state()
    
    def reset_left_car_selection(self):
        self.left_car = None
        self.reset_left_car.emit()
    
    def reset_right_car_selection(self):
        self.right_car = None
        self.reset_right_car.emit()
    
    def clear_comparison_grid(self):
        # Clear the comparison grid
        while self.comparison_grid.count():
            item = self.comparison_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def update_comparison(self):
        self.clear_comparison_grid()
        
        if not self.left_car or not self.right_car:
            return
        
        # Define comparison categories and their display order
        categories = [
            {"name": "Basic Information", "fields": [
                {"key": "price", "label": "Price"},
                {"key": "brand", "label": "Brand"},
                {"key": "model", "label": "Model"},
                {"key": "year", "label": "Year"},
                {"key": "condition", "label": "Condition"},
                {"key": "body_type", "label": "Body Type"}
            ]},
            {"name": "Technical Specifications", "fields": [
                {"key": "engine_size", "label": "Engine Size"},
                {"key": "transmission", "label": "Transmission"},
                {"key": "fuel_type", "label": "Fuel Type"},
                {"key": "drivetrain", "label": "Drivetrain"},
                {"key": "mileage", "label": "Mileage"}
            ]},
            {"name": "Performance", "fields": [
                {"key": "max_power", "label": "Max Power"},
                {"key": "max_torque", "label": "Max Torque"},
                {"key": "fuel_economy", "label": "Fuel Economy"}
            ]},
            {"name": "Dimensions", "fields": [
                {"key": "length", "label": "Length"},
                {"key": "width", "label": "Width"},
                {"key": "height", "label": "Height"},
                {"key": "wheelbase", "label": "Wheelbase"},
                {"key": "doors", "label": "Number of Doors"},
                {"key": "seating_capacity", "label": "Seating Capacity"}
            ]},
            {"name": "Safety Features", "fields": [
                {"key": "airbags", "label": "Airbags"},
                {"key": "abs", "label": "ABS"},
                {"key": "stability_control", "label": "Stability Control"},
                {"key": "security_system", "label": "Security System"}
            ]},
            {"name": "Comfort & Convenience", "fields": [
                {"key": "air_conditioning", "label": "Air Conditioning"},
                {"key": "entertainment", "label": "Entertainment System"},
                {"key": "upholstery", "label": "Upholstery"},
                {"key": "cruise_control", "label": "Cruise Control"},
                {"key": "push_start", "label": "Push Start Button"}
            ]}
        ]
        
        # Field mapping for different keys that might be used
        field_mappings = {
            "brand": ["brand", "make"],
            "body_type": ["body_type", "body type"],
            "engine_size": ["engine_size", "engine size", "displacement"],
            "mileage": ["mileage"],
            "fuel_type": ["fuel_type", "fuel type"],
            "max_power": ["max_power", "max output", "horsepower"],
            "max_torque": ["max_torque"],
            "fuel_economy": ["fuel_economy", "fuel consumption"],
            "length": ["length"],
            "width": ["width"],
            "height": ["height"],
            "wheelbase": ["wheelbase"],
            "doors": ["doors", "number of doors"],
            "seating_capacity": ["seating_capacity", "number of seats"],
            "airbags": ["airbags", "driver's airbag", "airbag: driver"],
            "abs": ["abs", "anti-lock brake system"],
            "stability_control": ["stability_control", "electronic stability control"],
            "security_system": ["security_system", "security alarm", "immobilizer"],
            "air_conditioning": ["air_conditioning", "air conditioning"],
            "entertainment": ["entertainment", "entertainment system"],
            "upholstery": ["upholstery", "leather upholstery"],
            "cruise_control": ["cruise_control", "cruise control"],
            "push_start": ["push_start", "push start"]
        }
        
        # Helper function to get value from car data with field mappings
        def get_car_value(car, field_key):
            # Direct key match first
            if field_key in car:
                return car[field_key]
            
            # Try alternate keys from mapping
            if field_key in field_mappings:
                for alt_key in field_mappings[field_key]:
                    if alt_key in car:
                        return car[alt_key]
            
            # For special case handling
            if field_key == "price":
                price = car.get("price")
                if price is None:
                    return "PRICE ON REQUEST"
                    return app_settings.format_price(price)
                
            return "N/A"
        
        # Add category headers and values to grid
        row = 0
        
        for category in categories:
            # Category header
            category_label = QLabel(category["name"])
            category_label.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #60a5fa;
                padding: 10px 0;
            """)
            self.comparison_grid.addWidget(category_label, row, 0, 1, 3)
            row += 1
            
            # Add field headers
            field_header = QLabel("Specification")
            left_header = QLabel("First Car")
            right_header = QLabel("Second Car")
            
            field_header.setStyleSheet("font-weight: bold; color: #d1d5db;")
            left_header.setStyleSheet("font-weight: bold; color: #d1d5db;")
            right_header.setStyleSheet("font-weight: bold; color: #d1d5db;")
            
            self.comparison_grid.addWidget(field_header, row, 0)
            self.comparison_grid.addWidget(left_header, row, 1)
            self.comparison_grid.addWidget(right_header, row, 2)
            row += 1
            
            # Add separator
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            separator.setStyleSheet("background-color: #4b5563; min-height: 1px;")
            self.comparison_grid.addWidget(separator, row, 0, 1, 3)
            row += 1
            
            # Add fields for this category
            for field in category["fields"]:
                # Get values from both cars
                left_value = get_car_value(self.left_car, field["key"])
                right_value = get_car_value(self.right_car, field["key"])
                
                # Create labels
                field_label = QLabel(field["label"])
                left_value_label = QLabel(str(left_value))
                right_value_label = QLabel(str(right_value))
                
                # Style based on comparison
                field_label.setStyleSheet("color: white;")
                
                # Highlight differences
                if str(left_value).lower() != str(right_value).lower() and left_value != "N/A" and right_value != "N/A":
                    left_style = "color: white; font-weight: bold;"
                    right_style = "color: white; font-weight: bold;"
                    
                    # Color code for numeric comparisons
                    try:
                        left_num = float(str(left_value).replace(",", "").replace("$", ""))
                        right_num = float(str(right_value).replace(",", "").replace("$", ""))
                        
                        # For price and other metrics where lower is better
                        if field["key"] in ["price", "mileage", "fuel_consumption"]:
                            if left_num < right_num:
                                left_style += " color: #22c55e;"  # Green for better value
                                right_style += " color: #ef4444;"  # Red for worse value
                            else:
                                left_style += " color: #ef4444;"
                                right_style += " color: #22c55e;"
                        # For metrics where higher is better
                        elif field["key"] in ["max_power", "max_torque", "fuel_economy"]:
                            if left_num > right_num:
                                left_style += " color: #22c55e;"
                                right_style += " color: #ef4444;"
                            else:
                                left_style += " color: #ef4444;"
                                right_style += " color: #22c55e;"
                    except:
                        # Not numeric values, just highlight differences
                        left_style += " color: #60a5fa;"
                        right_style += " color: #60a5fa;"
                        
                    left_value_label.setStyleSheet(left_style)
                    right_value_label.setStyleSheet(right_style)
                else:
                    left_value_label.setStyleSheet("color: #d1d5db;")
                    right_value_label.setStyleSheet("color: #d1d5db;")
                
                # Add to grid
                self.comparison_grid.addWidget(field_label, row, 0)
                self.comparison_grid.addWidget(left_value_label, row, 1)
                self.comparison_grid.addWidget(right_value_label, row, 2)
                row += 1
            
            # Add space between categories
            spacer = QLabel("")
            spacer.setFixedHeight(20)
            self.comparison_grid.addWidget(spacer, row, 0, 1, 3)
            row += 1

    def highlight_differences(self):
        """Highlight the key differences between the two cars"""
        if not self.left_car or not self.right_car:
            return

        # Logic to extract and display key differences
        differences = []
        
        # Compare price difference
        try:
            left_price = self.left_car.get("price")
            right_price = self.right_car.get("price")
            
            if left_price is not None and right_price is not None:
                price_diff = abs(left_price - right_price)
                price_pct = (price_diff / min(left_price, right_price)) * 100
                
                if price_pct > 5:  # If price difference is significant (more than 5%)
                    cheaper = "first" if left_price < right_price else "second"
                    from app.settings.app_settings import app_settings
                    differences.append(f"The {cheaper} car is {app_settings.format_price(price_diff)} cheaper ({price_pct:.1f}% less)")
                    
        except (ValueError, TypeError):
            pass