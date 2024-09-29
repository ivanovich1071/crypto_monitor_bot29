def format_currency(value):
    try:
        return f"{float(value):,.2f}"
    except ValueError:
        return value
