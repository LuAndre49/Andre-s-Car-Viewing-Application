from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import QRunnable, QThreadPool, Signal, QObject, Slot, Qt, QTimer
from PySide6.QtGui import QPixmap
import requests
import time
import weakref


class NewsBox(QWidget):
    def __init__(self, news_data, on_click, image_cache=None, index=0):
        super().__init__()

        self.news_data = news_data
        self.on_click = on_click
        self.image_cache = image_cache or {}
        self.threadpool = QThreadPool.globalInstance()
        self.current_loader = None  # Track the current loader

        # Layout setup
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Image
        self.image_label = QLabel("Loading image...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(150)  # Ensure minimum height for image area
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

        # Load image with short delay to avoid threading issues
        self.loading_timer = QTimer(self)
        self.loading_timer.setSingleShot(True)
        self.loading_timer.timeout.connect(self.load_image_async)
        self.loading_timer.start(index * 30)  # delay increases per NewsBox index

        
        # Set up timeout for loading
        self.loading_timer = QTimer(self)
        self.loading_timer.setSingleShot(True)
        self.loading_timer.timeout.connect(self.handle_loading_timeout)

    def load_image_async(self):
        image_url = self.news_data['image_url']

        if image_url in self.image_cache:
            pixmap = self.image_cache[image_url]
            if not pixmap.isNull():
                self.set_image(pixmap)
            else:
                self.set_no_image()
            return

        if self.current_loader and (loader := self.current_loader()):
            loader.cancel()

        loader = ImageLoader(image_url)
        loader.signals.finished.connect(self.set_image_with_check)
        loader.signals.failed.connect(self.set_no_image)
        loader.signals.finished.connect(lambda _: self._clear_loader())
        self.current_loader = weakref.ref(loader)
        self.threadpool.start(loader)


    def set_image_with_check(self, pixmap):
        if pixmap and not pixmap.isNull():
            self.set_image(pixmap)
        else:
            self.set_no_image()

    def set_no_image(self):
        self.image_label.setText("No Image")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("color: gray; font-style: italic;")

    def handle_loading_timeout(self):
        # If hit the timeout, show error
        self.set_image_failed()

    def handle_image_loaded(self, image_url, pixmap):
        # Stop the timeout timer
        if self.loading_timer.isActive():
            self.loading_timer.stop()
            
        if pixmap and not pixmap.isNull():
            self.image_cache[image_url] = pixmap
            self.set_image(pixmap)
        else:
            self.set_image_failed()

    def set_image(self, pixmap):
        if pixmap is None or pixmap.isNull() or pixmap.width() <= 0 or pixmap.height() <= 0:
            self.set_image_failed()
            return
            
        scaled_pixmap = pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        if not scaled_pixmap.isNull():
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setText("")
        else:
            self.set_image_failed()

    def set_image_failed(self):
        self.image_label.setText("Image not available")
        
    def deleteLater(self):
        if self.loading_timer.isActive():
            self.loading_timer.stop()
        if self.current_loader and (loader := self.current_loader()):
            loader.cancel()
        super().deleteLater()

    def _clear_loader(self):
        self.current_loader = None


class ImageLoader(QRunnable):
    class Signals(QObject):
        finished = Signal(QPixmap)
        failed = Signal()

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.signals = self.Signals()
        self.cancelled = False

    @Slot()
    def run(self):
        try:
            if self.cancelled:
                return
                
            pixmap = QPixmap()
            
            # Add a small delay to avoid thread contention
            time.sleep(0.05)
            
            if self.image_path.startswith("http"):
                try:
                    response = requests.get(self.image_path, timeout=8)
                    if self.cancelled:
                        return
                        
                    response.raise_for_status()
                    
                    # Check if content is valid image data
                    if not pixmap.loadFromData(response.content):
                        raise ValueError("Invalid image data received")
                    
                    if self.cancelled:
                        return
                        
                    # Check if image has valid dimensions
                    if pixmap.isNull() or pixmap.width() <= 0 or pixmap.height() <= 0:
                        raise ValueError("Loaded image has invalid dimensions")
                        
                except requests.exceptions.Timeout:
                    print(f"[ImageLoader] Timeout loading: {self.image_path}")
                    raise ValueError("Request timed out")
                except requests.exceptions.RequestException as e:
                    print(f"[ImageLoader] Request failed: {self.image_path} - {e}")
                    raise ValueError(f"Request failed: {str(e)}")
            else:
                if not pixmap.load(self.image_path):
                    raise ValueError("Failed to load local image.")
                    
                if self.cancelled:
                    return
                    
                # Check if image has valid dimensions
                if pixmap.isNull() or pixmap.width() <= 0 or pixmap.height() <= 0:
                    raise ValueError("Loaded image has invalid dimensions")
            
            if not self.cancelled:
                self.signals.finished.emit(pixmap)
                
        except Exception as e:
            print(f"[ImageLoader] Failed to load: {self.image_path} - {e}")
            if not self.cancelled:
                self.signals.failed.emit()
                
    def cancel(self):
        self.cancelled = True