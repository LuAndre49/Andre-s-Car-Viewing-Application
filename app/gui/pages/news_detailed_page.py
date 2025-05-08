from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QFrame, QSizePolicy
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os
import webbrowser
from app.settings.app_settings import app_settings
import requests
from bs4 import BeautifulSoup

class NewsDetailsPage(QWidget):
    def __init__(self, news_data):
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
            QLabel#snippet {
                padding-right: 10px;
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
                background-color: #334155;
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

        title = QLabel(news_data["title"])
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
    

        if news_data.get("local_image_path") and os.path.exists(news_data["local_image_path"]):
            pixmap = QPixmap(news_data["local_image_path"]).scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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


        self.add_field("Author", news_data["author"])
        self.add_field("Date", news_data["date"])
        snippet = self.get_snippet(news_data["link"])
        self.add_snippet_field("Snippet of Article", snippet)

        # View Full Article Button
        view_button = QPushButton("View Full Article")
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
        view_button.clicked.connect(lambda: self.open_full_article(news_data["link"]))
        self.details_layout.addWidget(view_button, alignment=Qt.AlignLeft)

        # Add both panels to layout
        content_layout.addWidget(image_frame, 2)
        content_layout.addWidget(details_frame, 3)

        main_layout.addLayout(content_layout)

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

    def get_snippet(self, link):
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraph_container = soup.select_one('div.padleft20.padright20.padbottom20')
            if paragraph_container:
                paragraphs = paragraph_container.find_all('p')
                if paragraphs:
                    # Get the first three paragraphs as a snippet
                    snippet = ' '.join([para.get_text() for para in paragraphs[:3]])
                    return snippet
                else:
                    return "No snippet available."
            else:
                return "No snippet available."
        else:
            return "Unable to fetch snippet."

    def add_snippet_field(self, label_text, value_text):
        # Create a row for the label and value
        row = QHBoxLayout()
        
        # Label part
        label = QLabel(f"{label_text}:")
        label.setFixedWidth(130)
        label.setAlignment(Qt.AlignTop)  # Align to top when text wraps
        row.addWidget(label)
        
        # Value part with word wrap enabled
        value = QLabel(value_text)
        value.setObjectName("snippet")
        value.setWordWrap(True)  # Enable word wrap
        value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Add to row
        row.addWidget(value, 1)  # Give the value label more space
        
        # Add the row to the details layout
        self.details_layout.addLayout(row)

    def open_full_article(self, url):

        webbrowser.open(url)
