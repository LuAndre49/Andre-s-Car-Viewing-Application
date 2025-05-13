from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, Signal, QThreadPool
from PySide6.QtGui import QPixmap
from app.settings.app_settings import app_settings
from app.gui.components.car_widgets import ImageLoader

class SelectedCarDisplay(QWidget):
    change_requested = Signal()
    
    def __init__(self, car_data=None):
        super().__init__()
        self.car_data = car_data
        self.threadpool = QThreadPool.globalInstance()
        self.setup_ui()
        
        if car_data:
            self.update_car(car_data)
    
    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Car image
        self.car_image = QLabel("No car selected")
        self.car_image.setAlignment(Qt.AlignCenter)
        self.car_image.setFixedHeight(100)
        self.car_image.setStyleSheet("background-color: #374151; border-radius: 8px; padding: 10px;")
        layout.addWidget(self.car_image)
        
        # Car name and details
        self.car_name = QLabel("No car selected")
        self.car_name.setAlignment(Qt.AlignCenter)
        self.car_name.setWordWrap(True)
        self.car_name.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
            margin-top: 3px;
        """)
        layout.addWidget(self.car_name)
        
        # Car price
        self.car_price = QLabel("")
        self.car_price.setAlignment(Qt.AlignCenter)
        self.car_price.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #00d084;
            margin-bottom: 3px;
        """)
        layout.addWidget(self.car_price)
        
        # Selected indicator
        selected_layout = QHBoxLayout()
        selected_icon = QLabel("✓")
        selected_icon.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #10b981;
        """)
        selected_text = QLabel("Selected for Comparison")
        selected_text.setStyleSheet("""
            font-size: 12px;
            color: #10b981;
            font-weight: 600;
        """)
        selected_layout.addStretch()
        selected_layout.addWidget(selected_icon)
        selected_layout.addWidget(selected_text)
        selected_layout.addStretch()
        
        selected_widget = QWidget()
        selected_widget.setLayout(selected_layout)
        layout.addWidget(selected_widget)
        
        # Change selection button
        self.change_button = QPushButton("Change Selection")
        self.change_button.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border-radius: 4px;
                padding: 6px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        self.change_button.clicked.connect(self.change_requested.emit)
        layout.addWidget(self.change_button)
        
        # Add some stretch to align everything nicely
        layout.addStretch()
        
        # Give this widget a nice style
        self.setObjectName("SelectedCarDisplay")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #SelectedCarDisplay {
                background-color: #334155;
                border: 2px solid #10b981;
                border-radius: 12px;
                padding: 10px;
            }
        """)
    
    def update_car(self, car_data):
        self.car_data = car_data
        self.car_name.setText(car_data['title'])
        
        # Update price
        price = car_data.get("price")
        if price is None:
            formatted_price = "PRICE ON REQUEST"
        else:
            formatted_price = app_settings.format_price(price)
        self.car_price.setText(formatted_price)
        
        # Load image
        self.load_image_async()
    
    def load_image_async(self):
        if not self.car_data:
            return
            
        image_path = self.car_data.get('local_image_path') or self.car_data['image_url']
        loader = ImageLoader(image_path)
        loader.signals.finished.connect(self.set_image)
        loader.signals.failed.connect(self.set_image_failed)
        self.threadpool.start(loader)
    
    def set_image(self, pixmap):
        self.car_image.setPixmap(pixmap.scaled(200, 100, Qt.KeepAspectRatio))
    
    def set_image_failed(self):
        self.car_image.setText("Image not available")