from PySide6.QtCore import QObject, Signal

class AppSettings(QObject):
    settingsChanged = Signal()

    def __init__(self):
        super().__init__()
        self.selected_currency = 'PHP'
        self.currency_symbol = '₱'
        self.distance_unit = 'km'

        self.currency_conversion_rates = {
            "PHP": 1,
            "USD": 0.02,
            "CNY": 0.16,
        }

        self.currency_symbols = {
            "PHP": '₱',
            "USD": '$',
            "CNY": '¥',
        }

    def format_price(self, value):
        if not isinstance(value, (int, float)):
            return "PRICE ON REQUEST"  # handles None, strings, etc.

        rate = self.currency_conversion_rates.get(self.selected_currency, 1)
        symbol = self.currency_symbols.get(self.selected_currency, '')
        converted_value = value * rate
        return f"{symbol}{converted_value:,.0f}"

    def format_distance(self, value: int | None) -> str:
        if value is None:
            return "N/A"
        return f"{value:,} {self.distance_unit}"

    def set_currency(self, currency):
        if currency in self.currency_symbols:
            self.selected_currency = currency
            self.currency_symbol = self.currency_symbols[currency]
            self.settingsChanged.emit()

# Create a global instance
app_settings = AppSettings()
