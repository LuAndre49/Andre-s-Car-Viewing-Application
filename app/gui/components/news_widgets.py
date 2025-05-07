from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import QRunnable, QThreadPool, Signal, QObject, Slot, Qt
from PySide6.QtGui import QPixmap
import requests


class NewsBox(QWidget):
    def __init__(self, news_data, on_click, image_cache=None):
        super().__init__()

        self.news_data = news_data
        self.on_click = on_click
        self.image_cache = image_cache or {}
        self.threadpool = QThreadPool.globalInstance()

        # Layout setup
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Image
        self.image_label = QLabel("Loading image...")
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # Title
        title = QLabel(news_data.get("title", "Untitled"))
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #ffffff;
        """)
        layout.addWidget(title)

        
        date_str = news_data.get("date")
        if date_str:
            date_label = QLabel(date_str)
            date_label.setAlignment(Qt.AlignCenter)
            date_label.setStyleSheet("""
                font-size: 13px;
                color: #cbd5e1;
            """)
            layout.addWidget(date_label)

        # Read more button
        button = QPushButton("Read More")
        button.clicked.connect(lambda _, d=news_data: self.on_click(d))
        button.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #3b82f6;
            }
        """)
        layout.addWidget(button)

        # Widget setup
        self.setLayout(layout)
        self.setObjectName("NewsBox")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #NewsBox {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 10px;
            }
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMaximumWidth(500)

        # Load image
        self.load_image_async()

    def load_image_async(self):
        image_url = self.news_data.get("image_url")
        if not image_url:
            self.image_label.setText("No image")
            return

        if image_url in self.image_cache:
            self.set_image(self.image_cache[image_url])
        else:
            loader = ImageLoader(image_url)
            loader.signals.finished.connect(lambda pixmap: self.handle_image_loaded(image_url, pixmap))
            loader.signals.failed.connect(self.set_image_failed)
            self.threadpool.start(loader)

    def handle_image_loaded(self, image_url, pixmap):
        self.image_cache[image_url] = pixmap
        self.set_image(pixmap)

    def set_image(self, pixmap):
        self.image_label.setPixmap(pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setText("")

    def set_image_failed(self):
        self.image_label.setText("Image not available")


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
