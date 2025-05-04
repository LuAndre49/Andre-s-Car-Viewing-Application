class AppSettings:
    selected_currency = 'PHP'
    currency_symbol = '₱'
    distance_unit = 'km'

    currency_conversion_rates = {
        "PHP": 1,
        "USD": 0.02,
        "CNY": 0.16,
    }

    currency_symbols = {
        "PHP": '₱',
        "USD": '$',
        "CNY": '¥',
    }

    @classmethod
    def format_price(cls, value):
        if isinstance(value, (int, float)):
            rate = cls.currency_conversion_rates.get(cls.selected_currency)
            symbol = cls.currency_symbols.get(cls.selected_currency)
            converted_value = value * rate
            print(f"[DEBUG] Formatting price for {value} in {cls.selected_currency}")

            return f"{symbol}{converted_value:,}"
        elif isinstance(value, str):
            return value 
        else:
            return "N/A"

    @classmethod
    def format_distance(cls, value: int | None) -> str:
        if value is None:
            return "N/A"
        return f"{value:,} {cls.distance_unit}"
