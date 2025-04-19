from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import requests

class CarBox(QWidget):
    def __init__(self, car_data, on_click):
        super().__init__()

        self.car_data = car_data
        self.on_click = on_click

        # Set up layout for the car box
        layout = QVBoxLayout()

        # Add car image
        car_image = QLabel()
        pixmap = QPixmap()
        try:
            response = requests.get(self.car_data['image'])
            response.raise_for_status()
            pixmap.loadFromData(response.content)
        except Exception as e:
            print(f"Failed to load image for {self.car_data['title']}: {e}")
            car_image.setText("Image not available")
        else:
            car_image.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        car_image.setAlignment(Qt.AlignCenter)

        
        # Add car name
        car_name = QLabel(self.car_data['title'])
        car_name.setAlignment(Qt.AlignCenter)
        
        # Button to view details
        button = QPushButton("View Details")
        button.clicked.connect(self.on_click)

        # Add widgets to layout
        layout.addWidget(car_image)
        layout.addWidget(car_name)
        layout.addWidget(button)

        self.setLayout(layout)
