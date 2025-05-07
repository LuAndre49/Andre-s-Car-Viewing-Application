from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget
from app.gui.pages.news_page import NewsPage
#from app.gui.pages.news_detailed_page import NewsDetailsPage

def show_news_details(news_data, ui):
    details_page = NewsDetailsPage(news_data)
    ui.mainPages.addWidget(details_page)
    ui.mainPages.setCurrentWidget(details_page)

def setup_news_page(ui, news_data):
    news_page_layout = QVBoxLayout(ui.newsPage)

    # Search bar setup
    search_layout = QHBoxLayout()
    search_bar = QLineEdit()
    search_bar.setPlaceholderText("Search for news")
    search_bar.setFixedHeight(35)
    search_bar.setStyleSheet("""
        QLineEdit {
            padding: 8px;
            border-radius: 6px;
            border: 1px solid #4B5563;
            background-color: #1f2937;
            color: white;
        }
    """)
    search_button = QPushButton("Search")
    search_layout.addWidget(search_bar)
    search_layout.addWidget(search_button)

    search_widget = QWidget()
    search_widget.setLayout(search_layout)
    news_page_layout.addWidget(search_widget)

    # News content
    image_cache = {}
    news = NewsPage(news_data, lambda n: show_news_details(n, ui), image_cache)
    news_page_layout.addWidget(news)

    def perform_search():
        news.search_news(search_bar.text())

    search_button.clicked.connect(perform_search)
    search_bar.returnPressed.connect(perform_search)

    return news
