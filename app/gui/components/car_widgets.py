from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import QRunnable, QThreadPool, Signal, QObject, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import requests
from app.settings.app_settings import AppSettings  

class CarBox(QWidget):
    def __init__(self, car_data, on_click, image_cache=None):
        super().__init__()

        self.car_data = car_data
        self.on_click = on_click
        self.image_cache = {}
        self.setup_ui()
        self.threadpool = QThreadPool.globalInstance()

        # Set up layout for the car box
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        # Add car image placeholder
        self.car_image = QLabel("Loading image...")
        self.car_image.setAlignment(Qt.AlignCenter)
        
        # Add car name
        car_name = QLabel(self.car_data['title'])
        car_name.setAlignment(Qt.AlignCenter)
        car_name.setWordWrap(True)
        car_name.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #ffffff;
            padding-bottom: 4px;
        """)
        price = self.car_data.get('price')

        if price is None:
            formatted_price = "PRICE ON REQUEST"
        else:
            formatted_price = AppSettings.format_price(price)

        print(f"Final display price: {formatted_price}")
        car_price = QLabel(formatted_price)
        car_price.setAlignment(Qt.AlignCenter)
        car_price.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #00d084;
            padding-top: 4px;
        """)
        
        # Button to view details
        button = QPushButton("View Details")
        button.clicked.connect(lambda: self.on_click(self.car_data))
        button.setStyleSheet("""
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

        # Add widgets to layout
        layout.addWidget(self.car_image)
        layout.addWidget(car_name)
        layout.addWidget(car_price)
        layout.addWidget(button)
        self.setLayout(layout)
        self.setObjectName("CarBox")
        self.setAttribute(Qt.WA_StyledBackground, True)  # ensures background is drawn

        self.setStyleSheet("""
            #CarBox {
                background-color: #334155;
                border: 1px solid #3c4a5a;
                border-radius: 12px;
                padding: 10px;
            }
        """)



        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMaximumWidth(500)
        self.load_image_async()


    def setup_ui(self):
        image_path = self.car_data.get('local_image_path') or self.car_data['image_url']
        if image_path in self.image_cache:
            pixmap = self.image_cache[image_path]
        else:
            pixmap = QPixmap(image_path)
            self.image_cache[image_path] = pixmap

    def load_image_async(self):
        image_path = self.car_data.get('local_image_path') or self.car_data['image_url']
        print(f"[DEBUG] Loading image from: {image_path}")
        loader = ImageLoader(image_path)
        loader.signals.finished.connect(self.set_image)
        loader.signals.failed.connect(self.set_image_failed)
        self.threadpool.start(loader)

    def set_image(self, pixmap):
        self.car_image.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))
    def set_image_failed(self):
        self.car_image.setText("Image not available")

class ImageLoader(QRunnable):
    class Signals(QObject):
        finished = Signal(QPixmap)
        failed = Signal()

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            pixmap = QPixmap()
            if self.image_path.startswith("http"):
                response = requests.get(self.image_path, timeout=10)
                response.raise_for_status()
                pixmap.loadFromData(response.content)
            else:
                if not pixmap.load(self.image_path):
                    raise ValueError("Failed to load local image.")
            self.signals.finished.emit(pixmap)
        except Exception as e:
            print(f"[ImageLoader] Failed to load: {self.image_path} - {e}")
            self.signals.failed.emit()
