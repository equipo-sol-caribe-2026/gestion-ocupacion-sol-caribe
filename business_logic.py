from datetime import date, timedelta
import math
import random



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



"""Aporte Integrante 2: Clase Hotel (Parte 1) - Fechas, Registro, Simulación y Estadísticas (Req. 2, 3, 4 y 5)"""

# 1. (Primera mitad de la clase Hotel y parseos de entrada):

class Hotel:
    def __init__(self, name, enabled_rooms, start_date):
        self.name = name
        self.enabled_rooms = enabled_rooms
        self.start_date = start_date
        self.occupied_rooms = []  # one number per recorded day

    # --- 2A. Days and dates (requirement 2) ---------------------------

    def days_recorded(self):
        return len(self.occupied_rooms)

    def date_of_day(self, index):
        """Date of the day at that position of the record (0 = first day)."""
        return self.start_date + timedelta(days=index)

    def next_date(self):
        """Date of the day that follows in the record."""
        return self.date_of_day(self.days_recorded())

    def add_day(self, rooms):
        self.occupied_rooms.append(rooms)

    # --- 2B. Simulation (requirement 3) -------------------------------

    def simulate(self, days, minimum, maximum):
        for _ in range(days):
            self.add_day(random.randint(minimum, maximum))

    # --- 2C. Statistics (requirements 4 and 5) -------------------------
    # They return unrounded numbers; the interface rounds when it shows them.
    # Call them only when days_recorded() > 0.

    def nights_sold(self):
        return sum(self.occupied_rooms)

    def average(self):
        return self.nights_sold() / self.days_recorded()

    def percentage(self):
        return self.average() / self.enabled_rooms * 100

    def standard_deviation(self):
        average = self.average()
        squares = sum((rooms - average) ** 2 for rooms in self.occupied_rooms)
        return math.sqrt(squares / self.days_recorded())


# =====================================================================
# PART 4 - Parsing of occupied rooms and days (requirements 2 and 3)
# =====================================================================

def parse_occupied_rooms(text, hotel):
    """Return (value, None) if text is an integer from 0 to the enabled
    rooms of the hotel, otherwise (None, error_message)."""
    rooms = to_integer(text)
    if rooms is None:
        return None, "Las habitaciones ocupadas deben ser un número entero."
    if rooms < 0 or rooms > hotel.enabled_rooms:
        return None, (f"Las habitaciones ocupadas van de 0 a "
                      f"{hotel.enabled_rooms}.")
    return rooms, None


def parse_days_count(text):
    """Return (value, None) if text is an integer of at least 1,
    otherwise (None, error_message)."""
    days = to_integer(text)
    if days is None:
        return None, "El número de días debe ser un número entero."
    if days < 1:
        return None, "Se debe simular al menos un día."
    return days, None


def validate_min_max(minimum, maximum):
    """Return None if minimum <= maximum, otherwise the error message."""
    if minimum > maximum:
        return "El mínimo no puede ser mayor que el máximo."
    return None
