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

