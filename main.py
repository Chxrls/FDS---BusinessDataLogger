import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import ttk

# Establish database connection
conn = sqlite3.connect('client_data.db')
c = conn.cursor()

# Create table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                client_type TEXT NOT NULL,
                service TEXT NOT NULL,
                cost TEXT NOT NULL,
                status TEXT NOT NULL
            )''')
conn.commit()

# Function to add client information to the database
def add_client():
    name = name_entry.get()
    service = service_var.get()
    cost = cost_entry.get()
    status = status_combobox.get()  # Fetching status from the Combobox
    client_type = client_type_var.get()

    c.execute('''INSERT INTO clients (name, client_type, service, cost, status) 
                 VALUES (?, ?, ?, ?, ?)''', (name, client_type, service, cost, status))
    conn.commit()
    messagebox.showinfo("Success", "Client information added successfully")
    clear_entries()

# Function to delete client information from the database
def delete_client():
    selected_client = client_list.get(client_list.curselection())
    c.execute('''DELETE FROM clients WHERE name = ?''', (selected_client,))
    conn.commit()
    messagebox.showinfo("Success", "Client information deleted successfully")
    clear_entries()

# Function to update technician status in the database
def update_status():
    name = name_entry.get()
    status = status_combobox.get()  # Fetching status from the Combobox
    c.execute('''UPDATE clients SET status = ? WHERE name = ?''', (status, name))
    conn.commit()
    messagebox.showinfo("Success", "Status updated successfully")
    clear_entries()

# Function to display all client information from the database
def display_clients():
    client_list.delete(0, tk.END)
    c.execute('''SELECT name FROM clients''')
    clients = c.fetchall()
    for client in clients:
        client_list.insert(tk.END, client[0])

# Function to display selected client's details from the database
def show_client_details(event):
    selected_client = client_list.get(client_list.curselection())
    c.execute('''SELECT * FROM clients WHERE name = ?''', (selected_client,))
    details = c.fetchone()
    client_info_label.config(text=f"Type: {details[2]}\nService: {details[3]}\nCost: {details[4]}\nStatus: {details[5]}")

# Function to clear entry fields
def clear_entries():
    name_entry.delete(0, tk.END)
    cost_entry.delete(0, tk.END)
    status_combobox.set('')  # Clear Combobox selection

# GUI Setup
root = tk.Tk()
root.title("Repair Management System")

# Define colors
bg_color = "#add8e6"  # Light blue background color
button_color = "#ff7f50"  # Coral color for complementing buttons

# Apply colors to frames
technician_frame = tk.Frame(root, bg=bg_color)
admin_frame = tk.Frame(root, bg=bg_color)

# Technician Page
name_label = tk.Label(technician_frame, text="Full Name or Business:", bg=bg_color)
name_entry = tk.Entry(technician_frame)
service_label = tk.Label(technician_frame, text="Service Type:", bg=bg_color)
service_options = ["Select a service type:", "Computer Formatting", "Computer Upgrades", "Hardware troubleshooting", "GPU Repair"]
service_var = tk.StringVar()
service_var.set(service_options[0])
service_dropdown = tk.OptionMenu(technician_frame, service_var, *service_options)
cost_label = tk.Label(technician_frame, text="Quoted Cost:", bg=bg_color)
cost_entry = tk.Entry(technician_frame)
client_type_label = tk.Label(technician_frame, text="Client Type:", bg=bg_color)
client_type_var = tk.StringVar()
client_type_client = tk.Radiobutton(technician_frame, text="Client", variable=client_type_var, value="Client", bg=bg_color)
client_type_business = tk.Radiobutton(technician_frame, text="Business", variable=client_type_var, value="Business", bg=bg_color)
add_button = tk.Button(technician_frame, text="Add Client", command=add_client)
status_label = tk.Label(technician_frame, text="Update Status:", bg=bg_color)
status_values = ["Not Started", "Ongoing", "Almost finished", "Done"]
status_var = tk.StringVar()
status_var.set(status_values[0])  # Set default status
status_combobox = ttk.Combobox(technician_frame, textvariable=status_var, values=status_values, state='readonly')
update_status_button = tk.Button(technician_frame, text="Update Status", command=update_status)

name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry.grid(row=0, column=1, padx=5, pady=5)
service_label.grid(row=1, column=0, padx=5, pady=5)
service_dropdown.grid(row=1, column=1, padx=5, pady=5)
cost_label.grid(row=2, column=0, padx=5, pady=5)
cost_entry.grid(row=2, column=1, padx=5, pady=5)
client_type_label.grid(row=3, column=0, padx=5, pady=5)
client_type_client.grid(row=3, column=1, padx=5, pady=5)
client_type_business.grid(row=3, column=2, padx=5, pady=5)
add_button.grid(row=4, columnspan=3, padx=5, pady=5)
status_label.grid(row=5, column=0, padx=5, pady=5)
status_combobox.grid(row=5, column=1, padx=5, pady=5)
update_status_button.grid(row=6, columnspan=3, padx=5, pady=5)

# Admin Page
client_list = tk.Listbox(admin_frame, width=40)
client_list.bind('<<ListboxSelect>>', show_client_details)
client_info_label = tk.Label(admin_frame, text="", justify="left")
display_button = tk.Button(admin_frame, text="Display Clients", command=display_clients)
delete_button = tk.Button(admin_frame, text="Delete Client", command=delete_client)
update_status_button_admin = tk.Button(admin_frame, text="Update Status", command=update_status)

client_list.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
client_info_label.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
display_button.pack(side=tk.TOP, padx=10, pady=10)
delete_button.pack(side=tk.TOP, padx=10, pady=10)
update_status_button_admin.pack(side=tk.TOP, padx=10, pady=10)

# Function to switch between pages
def show_technician_page():
    admin_frame.pack_forget()
    technician_frame.pack()

def show_admin_page():
    technician_frame.pack_forget()
    admin_frame.pack()

# Default page
show_technician_page()

# Menu
menu = tk.Menu(root)
root.config(menu=menu)
submenu = tk.Menu(menu)
menu.add_cascade(label="Pages", menu=submenu)
submenu.add_command(label="Technician", command=show_technician_page)
submenu.add_command(label="Admin", command=show_admin_page)

# Close the connection on program exit
root.protocol("WM_DELETE_WINDOW", lambda: (conn.close(), root.destroy()))

root.mainloop()
