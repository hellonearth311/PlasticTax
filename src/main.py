import customtkinter as ctk

def show_error_popup(title, message):
    popup = ctk.CTkToplevel()
    popup.title(title)
    popup.geometry("300x150")
    label = ctk.CTkLabel(popup, text=message, wraplength=280)
    label.pack(pady=20)
    button = ctk.CTkButton(popup, text="OK", command=popup.destroy)
    button.pack(pady=10)


def calculate_cost(filament_cost_per_kg, print_weight, estimated_print_time, electricity_cost_per_kwh, printer_power_rating):
    # ensure inputs are valid
    try:
        # input validation
        float(filament_cost_per_kg)
        float(print_weight)
        float(estimated_print_time)
        float(electricity_cost_per_kwh)
        float(printer_power_rating)

        # convert inputs
        print_weight = float(print_weight) / 1000  # convert grams to kg
        printer_power_rating = float(printer_power_rating) / 1000  # convert watts

        # calculate the cost
        filament_cost = float(filament_cost_per_kg) * print_weight
        electricity_cost = float(electricity_cost_per_kwh) * printer_power_rating * float(estimated_print_time)

        total_cost = filament_cost + electricity_cost

        # update the labels with results
        filament_cost_label.configure(text=f"Filament Cost: ${filament_cost:.2f}")
        electricity_cost_label.configure(text=f"Electricity Cost: ${electricity_cost:.2f}")
        total_cost_label.configure(text=f"Total Cost: ${total_cost:.2f}")

    except ValueError:
        show_error_popup("Invalid Input", "Please enter valid numeric values.")
        return None, None, None

root = ctk.CTk()
root.title("PlasticTax")
root.geometry("600x600")

title = ctk.CTkLabel(root, text="PlasticTax", font=("poppins", 40))
title.place(relx=0.5, rely=0.1, anchor="center")

# input fields
filament_cost_per_kg = ctk.CTkEntry(root, placeholder_text="Filament Cost per kg (dollars)", width=300)
filament_cost_per_kg.place(relx=0.5, rely=0.2, anchor="center")

print_weight = ctk.CTkEntry(root, placeholder_text="Weight of Print (grams)", width=300)
print_weight.place(relx=0.5, rely=0.3, anchor="center")

estimated_print_time = ctk.CTkEntry(root, placeholder_text="Estimated Print Time (hours)", width=300)
estimated_print_time.place(relx=0.5, rely=0.4, anchor="center")

electricity_cost_per_kwh = ctk.CTkEntry(root, placeholder_text="Electricity Cost per kWh (cents)", width=300)
electricity_cost_per_kwh.place(relx=0.5, rely=0.5, anchor="center")

printer_power_rating = ctk.CTkEntry(root, placeholder_text="Printer Power Rating (watts)", width=300)
printer_power_rating.place(relx=0.5, rely=0.6, anchor="center")

# calculate button
calculateButton = ctk.CTkButton(root, text="Calculate", command=lambda: calculate_cost(
    filament_cost_per_kg.get(),
    print_weight.get(),
    estimated_print_time.get(),
    electricity_cost_per_kwh.get(),
    printer_power_rating.get()
))
calculateButton.place(relx=0.5, rely=0.7, anchor="center")

# result labels
filament_cost_label = ctk.CTkLabel(root, text="Filament Cost: hit calculate to see result!", font=("poppins", 14))
filament_cost_label.place(relx=0.5, rely=0.8, anchor="center")

electricity_cost_label = ctk.CTkLabel(root, text="Electricity Cost: hit calculate to see result!", font=("poppins", 14))
electricity_cost_label.place(relx=0.5, rely=0.85, anchor="center")

total_cost_label = ctk.CTkLabel(root, text="Total Cost: hit calculate to see result!", font=("poppins", 14))
total_cost_label.place(relx=0.5, rely=0.9, anchor="center")

root.mainloop()