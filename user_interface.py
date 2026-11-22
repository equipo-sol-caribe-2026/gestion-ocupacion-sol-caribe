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
