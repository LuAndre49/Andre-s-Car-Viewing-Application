from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import QRunnable, QThreadPool, Signal, QObject, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import requests

class CarBox(QWidget):
    def __init__(self, car_data, on_click):
        super().__init__()

        self.car_data = car_data
        self.on_click = on_click
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
        # Add car price
        car_price = QLabel(self.car_data['price'])
        car_price.setAlignment(Qt.AlignCenter)
        
        # Button to view details
        button = QPushButton("View Details")
        button.clicked.connect(lambda: self.on_click(self.car_data))

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
                background-color: #2e2e2e;
                border: 2px solid #555;
                border-radius: 12px;
                padding: 10px;
            }
        """)



        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMaximumWidth(500)
        self.load_image_async()

    def load_image_async(self):
        loader = ImageLoader(self.car_data['image'])
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

    def __init__(self, image_url):
        super().__init__()
        self.image_url = image_url
        self.signals = self.Signals()

    @Slot()
    def run(self):
        try:
            response = requests.get(self.image_url, timeout=10)
            response.raise_for_status()
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.signals.finished.emit(pixmap)
        except Exception as e:
            print(f"[ImageLoader] Failed to load: {self.image_url} - {e}")
            self.signals.failed.emit()
