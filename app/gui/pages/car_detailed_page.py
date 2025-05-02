from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class CarDetailsPage(QWidget):
    def __init__(self, car_data):
        super().__init__()

        layout = QVBoxLayout()

        # Show detailed information
        layout.addWidget(QLabel(f"Title: {car_data['title']}"))
        layout.addWidget(QLabel(f"Price: {car_data['price']}"))
        layout.addWidget(QLabel(f"Location: {car_data['location']}"))
        layout.addWidget(QLabel(f"Transmission: {car_data['transmission']}"))
        layout.addWidget(QLabel(f"Year: {car_data['year']}"))
        layout.addWidget(QLabel(f"Mileage: {car_data['mileage']}"))
        layout.addWidget(QLabel(f"Status: {car_data['status']}"))
        layout.addWidget(QLabel(f"Link: {car_data['link']}"))

        self.setLayout(layout)
