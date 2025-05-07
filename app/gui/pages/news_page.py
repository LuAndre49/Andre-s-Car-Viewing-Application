from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QGridLayout
from app.gui.components.news_widgets import NewsBox

class NewsPage(QWidget):
    def __init__(self, news_data, on_news_click, image_cache):
        super().__init__()
        self.news_data_all = news_data
        self.on_news_click = on_news_click
        self.image_cache = image_cache
        self.max_news_per_row = 2  # Adjust for layout clarity

        self.page_layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.container = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(15)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)

        self.container.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.container)
        self.page_layout.addWidget(self.scroll_area)
        self.setLayout(self.page_layout)

        self.display_news(self.news_data_all)

    def display_news(self, data):
        while self.grid_layout.count() > 0:
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.news_boxes = []
        for index, news in enumerate(data):
            row = index // self.max_news_per_row
            col = index % self.max_news_per_row
            box = NewsBox(news, self.on_news_click, self.image_cache)
            self.news_boxes.append(box)
            self.grid_layout.addWidget(box, row, col)

    def search_news(self, query):
        terms = query.lower().split()
        filtered = [
            news for news in self.news_data_all
            if all(term in news["title"].lower() for term in terms)
        ]
        self.display_news(filtered)
