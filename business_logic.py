

# 1. En business_logic.py (Base compartida y creación de hotel):

# =====================================================================
# PART 1 - Shared base: hotel list, integer conversion, hotel lookup
# =====================================================================

hotels = []

# Indexes of the occupancy levels (same order as the report shows them)
CRITICAL, LOW, MEDIUM, HIGH = 0, 1, 2, 3


def to_integer(text):
    """Return the integer written in text, or None if it is not an integer."""
    text = text.strip()
    if "_" in text:  # int("1_0") would give 10, and that is not valid here
        return None
    try:
        return int(text)
    except ValueError:
        return None


def find_hotel(name):
    """Return the hotel with that exact name (ignoring outer spaces) or None."""
    name = name.strip()
    for hotel in hotels:
        if hotel.name == name:
            return hotel
    return None


# =====================================================================
# PART 3 - Create a hotel (requirement 1)
# =====================================================================

def validate_new_hotel(name, rooms_text, year_text, month_text, day_text):
    """Check the four conditions in order.
    Return (error_message, None) at the first one that fails, or
    (None, (name, enabled_rooms, start_date)) when everything is valid."""
    name = name.strip()
    if name == "":
        return "El nombre no puede estar vacío.", None
    if find_hotel(name) is not None:
        return "Ya existe un hotel con ese nombre.", None

    enabled_rooms = to_integer(rooms_text)
    if enabled_rooms is None:
        return "Las habitaciones habilitadas deben ser un número entero.", None
    if enabled_rooms < 1:
        return "El hotel debe tener al menos una habitación habilitada.", None

    year = to_integer(year_text)
    month = to_integer(month_text)
    day = to_integer(day_text)
    start_date = None
    if year is not None and month is not None and day is not None:
        try:
            start_date = date(year, month, day)
        except (ValueError, OverflowError):
            start_date = None
    if start_date is None:
        return "La fecha no es válida.", None

    return None, (name, enabled_rooms, start_date)


def create_hotel(name, rooms_text, year_text, month_text, day_text):
    """Create the hotel if valid. Return None, or the error message."""
    error, values = validate_new_hotel(name, rooms_text, year_text,
                                       month_text, day_text)
    if error is not None:
        return error
    hotels.append(Hotel(*values))
    return None


