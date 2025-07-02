import customtkinter as ctk
from PIL import Image
from CTkToolTip import CTkToolTip

# TODO
# Add ability to generate a PDF report

def show_error_popup(title, message):
    popup = ctk.CTkToplevel()
    popup.title(title)
    popup.geometry("300x150")
    label = ctk.CTkLabel(popup, text=message, wraplength=280)
    label.pack(pady=20)
    button = ctk.CTkButton(popup, text="OK", command=popup.destroy)
    button.pack(pady=10)

def show_settings_popup():
    popup = ctk.CTkToplevel()
    popup.title("Settings")
    popup.geometry("400x400")

    # Load the image
    bg_image = ctk.CTkImage(Image.open("src/img/hexagons.png"), size=(600, 600))

    # Create a label with the image
    bg_label = ctk.CTkLabel(popup, image=bg_image, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    settingsLabel = ctk.CTkLabel(popup, text="Settings", font=("poppins", 20))
    settingsLabel.place(relx=0.5, rely=0.1, anchor="center")

    defaultFilamentCostInput = ctk.CTkEntry(popup, placeholder_text="Default Filament Cost per kg (dollars)", width=300)
    defaultFilamentCostInput.place(relx=0.5, rely=0.2, anchor="center")

    defaultElectricityCostInput = ctk.CTkEntry(popup, placeholder_text="Default Electricity Cost per kWh (cents)", width=300)
    defaultElectricityCostInput.place(relx=0.5, rely=0.4, anchor="center")

    defaultPrinterPowerInput = ctk.CTkEntry(popup, placeholder_text="Default Printer Power Rating (watts)", width=300)
    defaultPrinterPowerInput.place(relx=0.5, rely=0.6, anchor="center")

    button = ctk.CTkButton(popup, text="OK", command=lambda: close_and_save_settings(popup, defaultFilamentCostInput.get(), defaultElectricityCostInput.get(), defaultPrinterPowerInput.get()))
    button.place(relx=0.5, rely=0.8, anchor="center")

def close_and_save_settings(popup, defaultFilamentCost, defaultElectricityCost, defaultPrinterPower):
    popup.destroy()
    # Ensure the data directory exists
    import os
    os.makedirs("src/data", exist_ok=True)
    
    # Write new settings, completely overwriting the file
    with open("src/data/settings.csv", "w") as settings_file:
        settings_file.write("default_filament_cost,default_electricity_cost,default_printer_power\n")
        settings_file.write(f"{defaultFilamentCost},{defaultElectricityCost},{defaultPrinterPower}\n")
    
    show_error_popup("Settings Saved", "Your settings have been saved successfully.")

def read_default_value(value):
    try:
        with open("src/data/settings.csv", "r") as settings_file:
            lines = settings_file.readlines()
            if len(lines) > 1:
                default_values = lines[1].strip().split(",")
                if value == "filament_cost":
                    return str(round(float(default_values[0]), 2))
                elif value == "electricity_cost":
                    return str(round(float(default_values[1]), 2))
                elif value == "printer_power":
                    return str(round(float(default_values[2]), 2))
    except FileNotFoundError:
        show_error_popup("Settings Error", "Settings file not found. Please set your defaults in the settings menu.")
    return ""

def load_default_value(entry_widget, value_type):
    """Load default value into entry widget, clearing existing content first"""
    default_value = read_default_value(value_type)
    if default_value:
        entry_widget.delete(0, 'end')  # Clear existing content
        entry_widget.insert(0, default_value)  # Insert default value


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
        printer_power_rating = float(printer_power_rating) / 1000  # convert watts to kW
        electricity_cost_per_kwh_dollars = float(electricity_cost_per_kwh) / 100  # convert cents to dollars

        # calculate the cost
        filament_cost = float(filament_cost_per_kg) * print_weight
        electricity_cost = electricity_cost_per_kwh_dollars * printer_power_rating * float(estimated_print_time)

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

# Load the image
bg_image = ctk.CTkImage(Image.open("src/img/hexagons.png"), size=(600, 600))

# Create a label with the image
bg_label = ctk.CTkLabel(root, image=bg_image, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

title = ctk.CTkLabel(root, text="PlasticTax", font=("poppins", 40), bg_color="transparent")
title.place(relx=0.5, rely=0.1, anchor="center")

# input fields
filament_cost_per_kg = ctk.CTkEntry(root, placeholder_text="Filament Cost per kg (dollars)", width=300)
filament_cost_per_kg.place(relx=0.4, rely=0.2, anchor="center")

filament_help_btn = ctk.CTkButton(root, text="?", width=25, height=25, 
                                 font=("Arial", 12, "bold"), command=lambda: None)
filament_help_btn.place(relx=0.7, rely=0.2, anchor="center")

CTkToolTip(filament_help_btn, message="Enter the cost of your filament per kilogram in dollars (e.g., 25.00)")
filament_load_defaults_btn = ctk.CTkButton(root, text="Load Defaults", command=lambda: load_default_value(filament_cost_per_kg, "filament_cost"))

filament_load_defaults_btn.place(relx=0.85, rely=0.2, anchor="center")
CTkToolTip(filament_load_defaults_btn, message="Load default filament cost from settings")

# -------------------------------------------------------------------

print_weight = ctk.CTkEntry(root, placeholder_text="Weight of Print (grams)", width=300)
print_weight.place(relx=0.4, rely=0.3, anchor="center")

weight_help_btn = ctk.CTkButton(root, text="?", width=25, height=25, 
                               font=("Arial", 12, "bold"), command=lambda: None)
weight_help_btn.place(relx=0.7, rely=0.3, anchor="center")
CTkToolTip(weight_help_btn, message="Enter the weight of your 3D print in grams (usually shown in your slicer)")

# -------------------------------------------------------------------

estimated_print_time = ctk.CTkEntry(root, placeholder_text="Estimated Print Time (hours)", width=300)
estimated_print_time.place(relx=0.4, rely=0.4, anchor="center")

time_help_btn = ctk.CTkButton(root, text="?", width=25, height=25, 
                             font=("Arial", 12, "bold"), command=lambda: None)
time_help_btn.place(relx=0.7, rely=0.4, anchor="center")
CTkToolTip(time_help_btn, message="Enter the estimated print time in hours (e.g., 2.5 for 2 hours 30 minutes)")

# -------------------------------------------------------------------

electricity_cost_per_kwh = ctk.CTkEntry(root, placeholder_text="Electricity Cost per kWh (cents)", width=300)
electricity_cost_per_kwh.place(relx=0.4, rely=0.5, anchor="center")

electricity_help_btn = ctk.CTkButton(root, text="?", width=25, height=25, 
                                   font=("Arial", 12, "bold"), command=lambda: None)
electricity_help_btn.place(relx=0.7, rely=0.5, anchor="center")
CTkToolTip(electricity_help_btn, message="Enter your electricity cost per kWh in cents (check your electricity bill!)")

electricity_load_defaults_btn = ctk.CTkButton(root, text="Load Defaults", command=lambda: load_default_value(electricity_cost_per_kwh, "electricity_cost"))
electricity_load_defaults_btn.place(relx=0.85, rely=0.5, anchor="center")
CTkToolTip(electricity_load_defaults_btn, message="Load default electricity cost from settings")

# -------------------------------------------------------------------

printer_power_rating = ctk.CTkEntry(root, placeholder_text="Printer Power Rating (watts)", width=300)
printer_power_rating.place(relx=0.4, rely=0.6, anchor="center")

power_help_btn = ctk.CTkButton(root, text="?", width=25, height=25, 
                              font=("Arial", 12, "bold"), command=lambda: None)
power_help_btn.place(relx=0.7, rely=0.6, anchor="center")
CTkToolTip(power_help_btn, message="Enter your 3D printer's power consumption in watts (check your printer's specifications or manual)")

power_load_defaults_btn = ctk.CTkButton(root, text="Load Defaults", command=lambda: load_default_value(printer_power_rating, "printer_power"))
power_load_defaults_btn.place(relx=0.85, rely=0.6, anchor="center")
CTkToolTip(power_load_defaults_btn, message="Load default printer power rating from settings")

# -------------------------------------------------------------------

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

settings_button = ctk.CTkButton(root, text="Settings", command=lambda: show_settings_popup())
settings_button.place(relx=0.05, rely=0.05, anchor="nw")

root.mainloop()