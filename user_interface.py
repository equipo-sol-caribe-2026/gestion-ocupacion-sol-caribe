# =====================================================================
# PART 1 - Shared helpers
# =====================================================================

def ask_for_hotel():
    """Read a hotel name. Return the hotel, or None after warning the user."""
    name = input("Nombre del hotel: ")
    hotel = bl.find_hotel(name)
    if hotel is None:
        print("No hay un hotel con ese nombre.")
    return hotel


def show_discarded(discarded):
    for line_number, cause in discarded:
        print(f"Línea {line_number} descartada: {cause}")


# =====================================================================
# PART 2 - Option 1: create a hotel (requirement 1)
# =====================================================================

def option_create_hotel():
    name = input("Nombre del hotel: ")
    rooms_text = input("Habitaciones habilitadas: ")
    year_text = input("Año de la fecha de inicio: ")
    month_text = input("Mes de la fecha de inicio: ")
    day_text = input("Día de la fecha de inicio: ")
    error = bl.create_hotel(name, rooms_text, year_text, month_text, day_text)
    if error is not None:
        print(error)
    else:
        print("Hotel creado.")


# =====================================================================
# PART 8 - Menu and program start (requirement 14)
# =====================================================================

def show_menu():
    print()
    print("===== Hoteles Sol Caribe =====")
    print("1. Crear un hotel")
    print("2. Registrar las habitaciones ocupadas del día siguiente")
    print("3. Simular días")
    print("4. Ver el informe de un hotel")
    print("5. Ver el hotel con mayor y menor porcentaje de ocupación")
    print("6. Cargar los hoteles y la ocupación desde archivos")
    print("7. Salir")


def main():
    actions = {
        "1": option_create_hotel,
        "2": option_register_day,
        "3": option_simulate_days,
        "4": option_report,
        "5": option_extremes,
        "6": option_load_files,
    }
    while True:
        show_menu()
        choice = input("Elija una opción: ").strip()
        if choice == "7":
            break
        action = actions.get(choice)
        if action is None:
            print("La opción no es válida.")
        else:
            action()


if __name__ == "__main__":
    main()

# PART 3 - Option 2: register the next day (requirement 2)
# =====================================================================

def option_register_day():
    hotel = ask_for_hotel()
    if hotel is None:
        return
    print(f"Día a registrar: {hotel.next_date().isoformat()}")
    while True:
        text = input("Habitaciones ocupadas: ")
        rooms, error = bl.parse_occupied_rooms(text, hotel)
        if error is None:
            break
        print(error)
    hotel.add_day(rooms)
    print("Día registrado.")


# =====================================================================
# PART 4 - Option 3: simulate days (requirement 3)
# =====================================================================
# Each value is checked right after reading it. If one fails, the message
# is shown and we go back to the menu without reading the rest.

def option_simulate_days():
    hotel = ask_for_hotel()
    if hotel is None:
        return

    days, error = bl.parse_days_count(input("Número de días a simular: "))
    if error is not None:
        print(error)
        return

    minimum, error = bl.parse_occupied_rooms(
        input("Habitaciones ocupadas mínimas: "), hotel)
    if error is not None:
        print(error)
        return

    maximum, error = bl.parse_occupied_rooms(
        input("Habitaciones ocupadas máximas: "), hotel)
    if error is not None:
        print(error)
        return

    error = bl.validate_min_max(minimum, maximum)
    if error is not None:
        print(error)
        return

    hotel.simulate(days, minimum, maximum)
    print(f"Se simularon {days} días.")

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
