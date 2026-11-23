"""Aporte Integrante 3: Clase Hotel (Parte 2) - Extremos, Niveles, Racha Crítica y Comparativa (Req. 6 al 9 y 11)"""



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
