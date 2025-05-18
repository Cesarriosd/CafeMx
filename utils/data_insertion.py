import pandas as pd
import inquirer

# Define the catalogs for dropdown menus
variedad_catalog = ["Sarchimor", "Ana café", "Typica", "Bourbon", "Geisha"]
perfil_catalog = ["Frutal", "Cítrico", "Chocolate", "Floral", "Nuez", "Especiado", "Caramelo", "Balanced"]
localidad_catalog = ["Ixhuacán de los Reyes", "Santa María Yucuhiti", "Mexico City", "Oaxaca", "Chiapas"]

def get_user_input_with_validation(prompt, catalog):
    """Gets user input with optional catalog dropdown and 'Other' option."""
    choices = catalog + ["Other"]
    questions = [
        inquirer.List('selection',
                      message=prompt,
                      choices=choices)
    ]
    answer = inquirer.prompt(questions)
    selected_value = answer['selection']

    if selected_value == "Other":
        new_value = input(f"Ingrese el nuevo valor para '{prompt}': ").strip()
        return new_value
    else:
        return selected_value

def get_numeric_input(prompt, data_type=float):
    """Gets numeric input from the user with type validation."""
    while True:
        try:
            value = data_type(input(f"{prompt}: "))
            return value
        except ValueError:
            print(f"Por favor, ingrese un valor numérico válido.")

def collect_coffee_data(variedad_catalog, perfil_catalog, localidad_catalog):
    """Collects coffee data from the user."""
    print("Por favor, ingrese la información del café:")

    localidad = get_user_input_with_validation("Localidad", localidad_catalog)
    finca = input("Finca: ").strip()
    latitude = get_numeric_input("Latitud")
    longitude = get_numeric_input("Longitud")
    variedad = get_user_input_with_validation("Variedad", variedad_catalog)
    productor = input("Productor: ").strip()
    perfil = get_user_input_with_validation("Perfil", perfil_catalog)
    variedad_details = input("URL de detalles de la variedad (opcional): ").strip()

    return {
        "Localidad": localidad,
        "Finca": finca,
        "Latitude": latitude,
        "Longitude": longitude,
        "Variedad": variedad,
        "Productor": productor,
        "Perfil": perfil,
        "Variedad_details": variedad_details if variedad_details else None
    }

def save_to_csv(data, filename="coffee_data.csv"):
    """Saves the collected data to a CSV file."""
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        df = pd.DataFrame(columns=data.keys())

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(f'..//data//{filename}', index=False)
    print(f"\nDatos guardados exitosamente en '{filename}'.")

if __name__ == "__main__":
    current_variedad_catalog = variedad_catalog[:]  # Create copies to allow modification
    current_perfil_catalog = perfil_catalog[:]
    current_localidad_catalog = localidad_catalog[:]

    while True:
        coffee_data = collect_coffee_data(current_variedad_catalog, current_perfil_catalog, current_localidad_catalog)
        save_to_csv(coffee_data)

        # Update catalogs with the newly entered value (if "Other" was selected)
        if coffee_data['Variedad'] not in variedad_catalog and coffee_data['Variedad'] not in current_variedad_catalog:
            current_variedad_catalog.append(coffee_data['Variedad'])
        if coffee_data['Perfil'] not in perfil_catalog and coffee_data['Perfil'] not in current_perfil_catalog:
            current_perfil_catalog.append(coffee_data['Perfil'])
        if coffee_data['Localidad'] not in localidad_catalog and coffee_data['Localidad'] not in current_localidad_catalog:
            current_localidad_catalog.append(coffee_data['Localidad'])

        another = input("¿Desea agregar información de otro café? (s/n): ").lower()
        if another != 's':
            break

    print("¡Gracias por ingresar la información!")