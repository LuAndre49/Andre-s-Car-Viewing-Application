from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QFrame, QSizePolicy
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os
import webbrowser
from app.settings.app_settings import app_settings

class CarDetailsPage(QWidget):
    def __init__(self, car_data):
        super().__init__()

        self.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
            }
            QFrame#ImageSection {
                background-color: #1E293B;
                border-radius: 10px;
            }
            QFrame#DetailsSection {
                background-color: #0F172A;
                border-radius: 10px;
                padding: 20px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        # Title
        # Title Frame
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: ##334155;
                border-radius: 10px;
                padding: 16px;
            }
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: white;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setAlignment(Qt.AlignCenter)

        title = QLabel(car_data["title"])
        title.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        title_layout.addWidget(title)

        main_layout.addWidget(title_frame)

        

        # Main horizontal split: image + details
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)

        # Image Section
        image_frame = QFrame()
        image_frame.setObjectName("ImageSection")
        image_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        image_layout = QVBoxLayout(image_frame)
        image_layout.setAlignment(Qt.AlignCenter)
        image_layout.setContentsMargins(20, 20, 20, 20)
    

        if car_data.get("local_image_path") and os.path.exists(car_data["local_image_path"]):
            pixmap = QPixmap(car_data["local_image_path"]).scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            image_layout.addWidget(image_label)
        else:
            image_layout.addWidget(QLabel("No image available"))

        # Details Section 
        details_frame = QFrame()
        details_frame.setObjectName("DetailsSection")
        details_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.details_layout = QVBoxLayout(details_frame)
        self.details_layout.setSpacing(12)


        self.price_label = QLabel()  


        price_text = app_settings.format_price(car_data["price"]) if car_data["price"] else "PRICE ON REQUEST"
        self.add_field("Price", price_text, self.price_label)
        self.add_field("Brand", car_data["brand"])
        self.add_field("Model", car_data["model"])
        self.add_field("Year", str(car_data["year"]))
        self.add_field("Transmission", car_data["transmission"])
        self.add_field("Mileage", car_data["mileage"])
        self.add_field("Condition", car_data["condition"])
        self.add_field("Fuel Type", car_data.get("fuel_type", "Not specified"))
        self.add_field("Location", car_data["location"])

        # View Listing Button
        view_button = QPushButton("View Listing")
        view_button.setCursor(Qt.PointingHandCursor)
        view_button.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #10b981;
            }
        """)
        view_button.clicked.connect(lambda: self.open_listing(car_data["link"]))
        self.details_layout.addWidget(view_button, alignment=Qt.AlignLeft)

        # Add both panels to layout
        content_layout.addWidget(image_frame, 2)
        content_layout.addWidget(details_frame, 3)

        main_layout.addLayout(content_layout)
        app_settings.settingsChanged.connect(self.refresh_price_display)

    
    def refresh_price_display(self):
        price = self.car_data["price"]
        if price:
            self.price_label.setText(app_settings.format_price(price))
        else:
            self.price_label.setText("PRICE ON REQUEST")

    def add_field(self, label_text, value_text, label_ref=None):
            row = QHBoxLayout()
            label = QLabel(f"{label_text}:")
            value = QLabel(value_text)
            label.setFixedWidth(110)
            row.addWidget(label)
            row.addWidget(value)
            row.addStretch()
            self.details_layout.addLayout(row)

            if label_ref is not None:
                label_ref.setText(value_text)  
                label_ref.setObjectName(label_text.lower() + "_label")

    def open_listing(self, url):

        webbrowser.open(url)
