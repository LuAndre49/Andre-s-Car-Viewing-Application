class AppSettings:
    currency = '₱'
    distance_unit = 'km'

    @classmethod
    def format_price(cls, value):
        if isinstance(value, (int, float)):
            return f"{cls.currency}{value:,}"
        elif isinstance(value, str):
            return value 
        else:
            return "N/A"

    @classmethod
    def format_distance(cls, value: int | None) -> str:
        if value is None:
            return "N/A"
        return f"{value:,} {cls.distance_unit}"
