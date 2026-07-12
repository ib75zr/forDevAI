def calculate_discount(price, percentage):
    if price < 0:
        raise ValueError("price must be non-negative")
    if not (0 <= percentage <= 100):
        raise ValueError("percentage must be between 0 and 100")
    return price - (price * percentage / 100)
