# starting off with a console version


# everything the user needs to input
print("Welcome to PlasticTax!")

filament_cost_per_kg = input("Enter the cost of filament per kg (dollars): ")
print_weight = input("Enter the weight of the print in grams: ")
estimated_print_time = input("Enter the estimated print time in hours: ")
electricity_cost_per_kwh = input("Enter the cost of electricity per kWh (cents): ")
printer_power_rating = input("Enter the printer power rating in watts: ")

# ensure inputs are valid
try:
    float(filament_cost_per_kg)
    float(print_weight)
    float(estimated_print_time)
    float(electricity_cost_per_kwh)
    float(printer_power_rating)
except ValueError:
    print("Invalid input. Please enter numeric values.")
    exit(1)

# convert inputs to appropriate types
print_weight = float(print_weight) / 1000  # convert grams to kg
printer_power_rating = float(printer_power_rating) / 1000  # convert watts to kW

# calculate costs
filament_cost = float(filament_cost_per_kg) * print_weight
electricity_cost = float(electricity_cost_per_kwh) * printer_power_rating * float(estimated_print_time)

total_cost = filament_cost + electricity_cost

# display the results
print("\nCost Breakdown:")

print(f"Filament Cost: ${filament_cost}")
print(f"Electricity Cost: ${electricity_cost}")

print("-----------------------------------------------")
print(f"Total Cost: ${total_cost}")

