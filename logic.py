"""Aporte Integrante 3: Clase Hotel (Parte 2) - Extremos, Niveles, Racha Crítica y Comparativa (Req. 6 al 9 y 11)"""

# 1. En business_logic.py (Segunda mitad de la clase Hotel y comparativa entre hoteles):
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


# 2. En user_interface.py (Opciones 4 y 5: informe completo y extremos de la cadena):
# =====================================================================
# PART 5 - Option 4: hotel report (requirements 4 to 9)
# =====================================================================

def option_report():
    hotel = ask_for_hotel()
    if hotel is None:
        return

    # Requirement 4: header and basic numbers
    print(f"Hotel: {hotel.name}")
    print(f"Habitaciones habilitadas: {hotel.enabled_rooms}")
    if hotel.days_recorded() == 0:
        print("El hotel no tiene días registrados.")
        return
    print(f"Días registrados: {hotel.days_recorded()}")
    print(f"Noches vendidas: {hotel.nights_sold()}")
    print(f"Promedio de habitaciones ocupadas por día: "
          f"{round(hotel.average(), 2)}")
    print(f"Porcentaje de ocupación: {round(hotel.percentage(), 2)} %")

    # Requirement 5: standard deviation
    print(f"Desviación estándar: {round(hotel.standard_deviation(), 2)}")

    # Requirement 6: highest and lowest day
    print(f"Día con más habitaciones ocupadas: "
          f"{hotel.highest_day_date().isoformat()}")
    print(f"Día con menos habitaciones ocupadas: "
          f"{hotel.lowest_day_date().isoformat()}")

    # Requirement 7: days in each level (always the four, even with 0)
    level_names = ["crítica", "baja", "media", "alta"]
    counts = hotel.count_levels()
    for level_name, count in zip(level_names, counts):
        print(f"Días en ocupación {level_name}: {count}")

    # Requirement 8: longest critical streak
    streak = hotel.longest_critical_streak()
    if streak is None:
        print("El hotel no tuvo ningún día en ocupación crítica.")
    else:
        length, start_date = streak
        print(f"Racha más larga en ocupación crítica: {length} días, "
              f"desde el {start_date.isoformat()}")

    # Requirement 9: days not recorded yet
    print(f"Último día registrado: {hotel.last_recorded_date().isoformat()}")
    missing = hotel.missing_days(date.today())
    if missing == 0:
        print("El registro está al día.")
    else:
        print(f"Faltan por registrar {missing} días.")


# =====================================================================
# PART 6 - Option 5: highest and lowest percentage (requirement 11)
# =====================================================================

def option_extremes():
    highest = bl.hotel_with_highest_percentage()
    if highest is None:
        print("Ningún hotel tiene días registrados.")
        return
    lowest = bl.hotel_with_lowest_percentage()
    print(f"Mayor porcentaje de ocupación: {highest.name}, "
          f"{round(highest.percentage(), 2)} %")
    print(f"Menor porcentaje de ocupación: {lowest.name}, "
          f"{round(lowest.percentage(), 2)} %")

