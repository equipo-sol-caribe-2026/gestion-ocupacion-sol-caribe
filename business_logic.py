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

# index() returns the FIRST position, which solves ties as required.

    def highest_day_date(self):
        index = self.occupied_rooms.index(max(self.occupied_rooms))
        return self.date_of_day(index)

    def lowest_day_date(self):
        index = self.occupied_rooms.index(min(self.occupied_rooms))
        return self.date_of_day(index)

    # --- 2E. Occupancy levels (requirement 7) --------------------------
    # Integer comparisons (rooms * 100 < 40 * enabled) avoid decimal errors.

    def level_of_day(self, index):
        rooms = self.occupied_rooms[index] * 100
        if rooms < 40 * self.enabled_rooms:
            return CRITICAL
        if rooms < 60 * self.enabled_rooms:
            return LOW
        if rooms < 80 * self.enabled_rooms:
            return MEDIUM
        return HIGH

    def count_levels(self):
        """Return [critical, low, medium, high] day counts."""
        counts = [0, 0, 0, 0]
        for index in range(self.days_recorded()):
            counts[self.level_of_day(index)] += 1
        return counts

    # --- 2F. Longest critical streak (requirement 8) -------------------

    def longest_critical_streak(self):
        """Return (length, start_date) of the longest critical streak,
        or None if the hotel never had a critical day.
        A strictly greater length is needed to replace the best streak,
        so on a tie the one that started first is kept."""
        best_length = 0
        best_start = 0
        current_length = 0
        current_start = 0
        for index in range(self.days_recorded()):
            if self.level_of_day(index) == CRITICAL:
                if current_length == 0:
                    current_start = index
                current_length += 1
                if current_length > best_length:
                    best_length = current_length
                    best_start = current_start
            else:
                current_length = 0
        if best_length == 0:
            return None
        return best_length, self.date_of_day(best_start)

    # --- 2G. Days not recorded yet (requirement 9) ---------------------

    def last_recorded_date(self):
        return self.date_of_day(self.days_recorded() - 1)

    def missing_days(self, today):
        """Days from the one after the last recorded day up to the day before
        today. 0 means the record is up to date. today is a parameter so it
        can be tested with any date."""
        missing = (today - timedelta(days=1) - self.last_recorded_date()).days
        return max(missing, 0)

# =====================================================================
# PART 5 - Highest and lowest occupancy percentage (requirement 11)
# =====================================================================
# Only hotels with recorded days count. Strict comparisons keep the first
# hotel created or loaded when there is a tie.

def hotel_with_highest_percentage():
    best = None
    for hotel in hotels:
        if hotel.days_recorded() == 0:
            continue
        if best is None or hotel.percentage() > best.percentage():
            best = hotel
    return best


def hotel_with_lowest_percentage():
    best = None
    for hotel in hotels:
        if hotel.days_recorded() == 0:
            continue
        if best is None or hotel.percentage() < best.percentage():
            best = hotel
    return best
    
# PART 6 - Load from files (requirements 12 and 13)
# ====================================================================
# Both loaders let FileNotFoundError go up so the interface can report it.
# They return (loaded_count, discarded) where discarded is a list of
# (line_number, cause).

def can_load_from_files():
    """Loading is only allowed when the program has no hotels yet."""
    return len(hotels) == 0


def read_data_lines(path):
    """Return [(line_number, line)] without the header (line 1) and
    without the blank lines. Line numbers are the real ones in the file."""
    with open(path, encoding="utf-8") as file:
        lines = file.read().splitlines()
    return [(number, line)
            for number, line in enumerate(lines, start=1)
            if number > 1 and line.strip() != ""]


def split_fields(line):
    return [field.strip() for field in line.split(";")]


def load_hotels_from_file(path):
    loaded = 0
    discarded = []
    for number, line in read_data_lines(path):
        fields = split_fields(line)
        if len(fields) != 5:
            discarded.append((number, "La línea no tiene cinco campos."))
            continue
        error = create_hotel(*fields)
        if error is not None:
            discarded.append((number, error))
        else:
            loaded += 1
    return loaded, discarded


def load_occupancy_from_file(path):
    loaded = 0
    discarded = []
    for number, line in read_data_lines(path):
        fields = split_fields(line)
        if len(fields) != 2:
            discarded.append((number, "La línea no tiene dos campos."))
            continue
        hotel = find_hotel(fields[0])
        if hotel is None:
            discarded.append((number, "No hay un hotel con ese nombre."))
            continue
        rooms, error = parse_occupied_rooms(fields[1], hotel)
        if error is not None:
            discarded.append((number, error))
            continue
        hotel.add_day(rooms)
        loaded += 1
    return loaded, discarded
