import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import hashlib

# Establish database connection
conn = sqlite3.connect('techtalk_computer_services.db')
c = conn.cursor()

# Create tables for businesses, clients, services, and technicians
c.execute('''CREATE TABLE IF NOT EXISTS businesses (
                BusinessID INTEGER PRIMARY KEY,
                TechnicianID INTEGER NOT NULL REFERENCES technician(TechnicianID),
                BusinessName TEXT NOT NULL,
                ContactNo TEXT NOT NULL,
                Address TEXT NOT NULL,
                Status TEXT NOT NULL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS clients (
                ClientID INTEGER PRIMARY KEY,
                TechnicianID INTEGER NOT NULL REFERENCES technician(TechnicianID),
                ClientName TEXT NOT NULL,
                ContactNo TEXT NOT NULL,
                Address TEXT NOT NULL,
                Status TEXT NOT NULL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS services (
                ServiceID INTEGER PRIMARY KEY,
                TechnicianID INTEGER NOT NULL REFERENCES technician(TechnicianID),
                ClientID INTEGER REFERENCES clients(ClientID),
                BusinessID INTEGER REFERENCES businesses(BusinessID),
                ServiceType TEXT NOT NULL,
                DeviceType TEXT NOT NULL,
                IssueDescription TEXT NOT NULL,
                Cost INTEGER NOT NULL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS technician (
                TechnicianID INTEGER PRIMARY KEY
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS AdminLogin (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )''')

# Check if the admin account exists, if not, create a default one
c.execute('''SELECT * FROM AdminLogin''')
admin_account = c.fetchone()
if admin_account is None:
    # Hashing the default password "admin"
    hashed_password = hashlib.sha256("admin".encode()).hexdigest()
    c.execute('''INSERT INTO AdminLogin (username, password) VALUES (?, ?)''', ("admin", hashed_password))
    conn.commit()
# Function to add client information to the database
# Function to add client information to the database
# Function to add client information to the database
def add_client():
    name = name_entry.get()
    service_type = service_var.get()
    address = address_entry.get()
    contact = contact_entry.get()
    device_type = device_entry.get()
    issue = issue_entry.get()
    status = status_combobox.get()  # Fetching status from the Combobox
    client_type = client_type_var.get()

    # Check if any required field is empty
    if not name or not service_type or not status or not client_type or service_type == "Select a service type:":
        messagebox.showerror("Error", "Please fill in all fields and select a service type.")
        return

    # Insert data based on client type
    if client_type == "Client":
        c.execute('''INSERT INTO clients (TechnicianID, ClientName, ContactNo, Address, Status)
                     VALUES (?, ?, ?, ?, ?)''', (1, name, contact, address, status))
        client_id = c.lastrowid
    elif client_type == "Business":
        c.execute('''INSERT INTO businesses (TechnicianID, BusinessName, ContactNo, Address, Status)
                     VALUES (?, ?, ?, ?, ?)''', (1, name, contact, address, status))
        client_id = c.lastrowid

    # Insert data into services table
    c.execute('''INSERT INTO services (TechnicianID, ClientID, BusinessID, ServiceType, DeviceType, IssueDescription, Cost)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', (1, client_id if client_type == "Client" else None,
                                                 client_id if client_type == "Business" else None,
                                                 service_type, device_type, issue, cost_entry.get()))

    conn.commit()
    messagebox.showinfo("Success", f"{client_type} information added successfully")
    clear_entries()
    display_clients()


    conn.commit()
    messagebox.showinfo("Success", f"{client_type} information added successfully")
    clear_entries()
    display_clients()


# Function to delete client information from the database
def delete_client():
    selected_index = client_list.curselection()

    if not selected_index:
        return  # No item selected

    selected_client = client_list.get(selected_index)
    selected_client_name = selected_client.split(". ")[1].split(" (")[0]

    c.execute('''DELETE FROM clients WHERE ClientName = ?''', (selected_client_name,))
    c.execute('''DELETE FROM businesses WHERE BusinessName = ?''', (selected_client_name,))
    conn.commit()

    messagebox.showinfo("Success", "Client information deleted successfully")
    clear_entries()
    display_clients()


# Function to edit client information
def edit_client():
    selected_index = client_list.curselection()

    if not selected_index:
        return  # No item selected

    selected_client = client_list.get(selected_index)
    selected_client_name = selected_client.split(". ")[1].split(" (")[0]

    # Retrieve existing client details
    if "(Client)" in selected_client:
        c.execute('''SELECT * FROM clients WHERE ClientName = ?''', (selected_client_name,))
        current_details = c.fetchone()
    elif "(Business)" in selected_client:
        c.execute('''SELECT * FROM businesses WHERE BusinessName = ?''', (selected_client_name,))
        current_details = c.fetchone()
    else:
        current_details = None

    # Check if details are found
    if current_details is None:
        messagebox.showerror("Error", "No details found for the selected client/business")
        return

    # Open a new window or dialog for editing
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Client Information")
    edit_window.resizable(False, False)

    # Create labels and entry fields for editing
    edit_name_label = tk.Label(edit_window, text="Full Name or Business:")
    edit_name_entry = tk.Entry(edit_window)
    edit_name_entry.insert(0, current_details[2] if current_details and len(current_details) > 2 else "Name")  # Set the client/business name as the placeholder

    edit_service_label = tk.Label(edit_window, text="Service Type:")
    edit_service_var = tk.StringVar()
   # edit_service_var.set(current_details[3] if current_details and len(current_details) > 3 else "Select a service type")  # Populate with current service
    edit_service_dropdown = ttk.Combobox(edit_window, textvariable=edit_service_var, values=service_options, state='readonly')

    edit_cost_label = tk.Label(edit_window, text="Quoted Cost:")
    edit_cost_entry = tk.Entry(edit_window, validate="key",
                               validatecommand=(root.register(lambda char: char.isdigit() or char == ""), "%S"))
   # edit_cost_entry.insert(0, current_details[4] if current_details and len(current_details) > 4 else "Cost")  # Populate with current cost

    edit_client_type_label = tk.Label(edit_window, text="Client Type:")
    edit_client_type_var = tk.StringVar()
   # edit_client_type_var.set(current_details[2] if current_details and len(current_details) > 2 else "")  # Populate with current client type
    edit_client_type_client = tk.Radiobutton(edit_window, text="Client", variable=edit_client_type_var, value="Client")
    edit_client_type_business = tk.Radiobutton(edit_window, text="Business", variable=edit_client_type_var, value="Business")

    edit_status_label = tk.Label(edit_window, text="Update Status:")
    edit_status_values = ["Not Started", "Ongoing", "Almost finished", "Done"]
    edit_status_var = tk.StringVar()
   # edit_status_var.set(current_details[5] if current_details and len(current_details) > 5 else "Select a status")  # Populate with current status
    edit_status_combobox = ttk.Combobox(edit_window, textvariable=edit_status_var, values=edit_status_values, state='readonly')

    # Additional fields for address and contact number
    edit_address_label = tk.Label(edit_window, text="Address:")
    edit_address_entry = tk.Entry(edit_window)
   # edit_address_entry.insert(0, current_details[6] if current_details and len(current_details) > 6 else "Address")  # Populate with current address

    edit_contact_label = tk.Label(edit_window, text="Contact Number:")
    edit_contact_entry = tk.Entry(edit_window, validate="key",
                                  validatecommand=(root.register(lambda char: char.isdigit() or char == ""), "%S"))

    # edit_contact_entry.insert(0, current_details[7] if current_details and len(current_details) > 7 else "Contact Number")  # Populate with current contact number

    # Create a function to save changes
    def save_changes():
        new_name = edit_name_entry.get()
        new_service = edit_service_var.get()
        new_cost = edit_cost_entry.get()
        new_client_type = edit_client_type_var.get()
        new_status = edit_status_var.get()
        new_address = edit_address_entry.get()
        new_contact = edit_contact_entry.get()

        # Check for empty fields
        if not new_name or not new_service or not new_cost or not new_client_type or not new_status or not new_address or not new_contact:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if "(Client)" in selected_client:
            # Update the client in the clients table
            c.execute('''UPDATE clients SET ClientName = ?, client_type = ?, service = ?, cost = ?, status = ?, address = ?, contact_number = ? WHERE ClientName = ?''',
                      (new_name, new_client_type, new_service, new_cost, new_status, new_address, new_contact, selected_client_name))
        elif "(Business)" in selected_client:
            # Update the business in the businesses table
            c.execute('''UPDATE businesses SET BusinessName = ?, technicianID = ?, ContactNo = ? WHERE BusinessName = ?''',
                      (new_name, 1, new_contact, selected_client_name))

        conn.commit()
        messagebox.showinfo("Success", "Client/business information updated successfully")
        edit_window.destroy()  # Close the edit window
        display_clients()  # Refresh the displayed client list

    # Create a button to save changes
    save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)

    # Grid layout for the edit window
    edit_name_label.grid(row=0, column=0, padx=5, pady=5)
    edit_name_entry.grid(row=0, column=1, padx=5, pady=5)
    edit_service_label.grid(row=1, column=0, padx=5, pady=5)
    edit_service_dropdown.grid(row=1, column=1, padx=5, pady=5)
    edit_cost_label.grid(row=2, column=0, padx=5, pady=5)
    edit_cost_entry.grid(row=2, column=1, padx=5, pady=5)
    edit_client_type_label.grid(row=3, column=0, padx=5, pady=5)
    edit_client_type_client.grid(row=3, column=1, padx=5, pady=5)
    edit_client_type_business.grid(row=3, column=2, padx=5, pady=5)
    edit_status_label.grid(row=4, column=0, padx=5, pady=5)
    edit_status_combobox.grid(row=4, column=1, padx=5, pady=5)
    edit_address_label.grid(row=5, column=0, padx=5, pady=5)
    edit_address_entry.grid(row=5, column=1, padx=5, pady=5)
    edit_contact_label.grid(row=6, column=0, padx=5, pady=5)
    edit_contact_entry.grid(row=6, column=1, padx=5, pady=5)
    save_button.grid(row=7, columnspan=2, padx=5, pady=5)


# Function to display all client information from the database
def display_clients():
    c.execute('''SELECT clients.ClientName, clients.ClientID, clients.ContactNo, clients.Address, clients.Status,
                 services.ServiceType, services.DeviceType, services.IssueDescription, services.Cost
                 FROM clients LEFT JOIN services ON clients.ClientID = services.ClientID''')
    client_data = c.fetchall()

    c.execute('''SELECT businesses.BusinessName, businesses.BusinessID, businesses.ContactNo, businesses.Address, businesses.Status,
                 services.ServiceType, services.DeviceType, services.IssueDescription, services.Cost
                 FROM businesses LEFT JOIN services ON businesses.BusinessID = services.BusinessID''')
    business_data = c.fetchall()

    num_clients = 0
    client_list.delete(0, tk.END)

    # Display client data
    for items in client_data:
        num_clients += 1
        client_list.insert(tk.END, f"{num_clients}. {items[0]} (Client)")

    # Display business data
    for items in business_data:
        num_clients += 1
        client_list.insert(tk.END, f"{num_clients}. {items[0]} (Business)")


def show_client_details(event):
    selected_index = client_list.curselection()

    if not selected_index:
        return  # No item selected

    selected_client = client_list.get(selected_index)
    selected_client_name = selected_client.split(". ")[1].split(" (")[0]

    # Determine if the selected entry corresponds to a client or business
    client_type = "Client" if "(Client)" in selected_client else "Business"

    # Retrieve and update details on the UI
    if client_type == "Client":
        c.execute('''SELECT clients.ClientName, clients.ClientID, clients.ContactNo, clients.Address, clients.Status,
                     services.ServiceType, services.DeviceType, services.IssueDescription, services.Cost
                     FROM clients LEFT JOIN services ON clients.ClientID = services.ClientID
                     WHERE clients.ClientName = ?''', (selected_client_name,))
        client_details = c.fetchone()
    elif client_type == "Business":
        c.execute('''SELECT businesses.BusinessName, businesses.BusinessID, businesses.ContactNo, businesses.Address, businesses.Status,
                     services.ServiceType, services.DeviceType, services.IssueDescription, services.Cost
                     FROM businesses LEFT JOIN services ON businesses.BusinessID = services.BusinessID
                     WHERE businesses.BusinessName = ?''', (selected_client_name,))
        client_details = c.fetchone()

    if client_details:
        details_text = f"Details for {client_type}: {selected_client_name}\n"
        details_text += "===================================\n"
        #details_text += f"ID: {client_details[1]}\n"
        details_text += f"Contact No: {client_details[2]}\n"
        if client_type == "Client":
            details_text += f"Address: {client_details[3]}\n"

        # Additional details for services
        details_text += f"Service Type: {client_details[5]}\n"
        details_text += f"Device Type: {client_details[6]}\n"
        details_text += f"Issue Description: {client_details[7]}\n"
        details_text += f"Quoted Cost: {client_details[8]}\n"

        details_text += "===================================\n"
        client_info_label.config(text=details_text)
    else:
        client_info_label.config(text=f"No details found for {client_type}: {selected_client_name}")


# Function to clear entry fields
def clear_entries():
    name_entry.delete(0, tk.END)
    cost_entry.delete(0, tk.END)
    status_combobox.set('')  # Clear Combobox selection

def validate_name(char):
    return char.isalpha() or char.isspace()

# GUI Setup
root = tk.Tk()
root.geometry("700x500")
root.resizable(False, False)
root.title("Repair Management System")

# Define colors
bg_color = "#add8e6"  # Light blue background color
button_color = "#ff7f50"  # Coral color for complementing buttons

# Apply background color to the whole window
root.configure(bg=bg_color)

# Apply colors to frames
technician_frame = tk.Frame(root, bg=bg_color)
admin_frame = tk.Frame(root, bg=bg_color)

# Technician Page
name_label = tk.Label(technician_frame, text="Full Name or Business:", bg=bg_color)
name_entry = tk.Entry(technician_frame, validate="key", validatecommand=(root.register(validate_name), "%S"))
service_label = tk.Label(technician_frame, text="Service Type:", bg=bg_color)
service_options = ["Select a service type:", "Computer Formatting", "Computer Upgrades", "Hardware troubleshooting", "GPU Repair"]
service_var = tk.StringVar()
service_var.set(service_options[0])
service_dropdown = ttk.Combobox(technician_frame, textvariable=service_var, values=service_options, state='readonly')
cost_label = tk.Label(technician_frame, text="Quoted Cost:", bg=bg_color)
cost_entry = tk.Entry(technician_frame, validate="key", validatecommand=(root.register(lambda char: char.isdigit() or char == ""), "%S"))
client_type_label = tk.Label(technician_frame, text="Client Type:", bg=bg_color)
client_type_var = tk.StringVar()
client_type_client = tk.Radiobutton(technician_frame, text="Client", variable=client_type_var, value="Client", bg=bg_color)
client_type_business = tk.Radiobutton(technician_frame, text="Business", variable=client_type_var, value="Business", bg=bg_color)

# Add new entry boxes for address, contact number, device type, and issue description
address_label = tk.Label(technician_frame, text="Address:", bg=bg_color)
address_entry = tk.Entry(technician_frame)

contact_label = tk.Label(technician_frame, text="Contact Number:", bg=bg_color)
contact_entry = tk.Entry(technician_frame, validate="key", validatecommand=(root.register(lambda char: char.isdigit() or char == ""), "%S"))

device_label = tk.Label(technician_frame, text="Device Type:", bg=bg_color)
device_entry = tk.Entry(technician_frame)

issue_label = tk.Label(technician_frame, text="Issue Description:", bg=bg_color)
issue_entry = tk.Entry(technician_frame)

add_button = tk.Button(technician_frame, text="Add Client", command=add_client)
status_label = tk.Label(technician_frame, text="Update Status:", bg=bg_color)
status_values = ["Not Started", "Ongoing", "Almost finished", "Done"]
status_var = tk.StringVar()
status_var.set(status_values[0])  # Set default status
status_combobox = ttk.Combobox(technician_frame, textvariable=status_var, values=status_values, state='readonly')
#update_status_button = tk.Button(technician_frame, text="Update Status", command=update_status)

# Grid layout for the technician frame
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry.grid(row=0, column=1, padx=5, pady=5)
service_label.grid(row=1, column=0, padx=5, pady=5)
service_dropdown.grid(row=1, column=1, padx=5, pady=5)
cost_label.grid(row=2, column=0, padx=5, pady=5)
cost_entry.grid(row=2, column=1, padx=5, pady=5)
client_type_label.grid(row=3, column=0, padx=5, pady=5)
client_type_client.grid(row=3, column=1, padx=5, pady=5)
client_type_business.grid(row=3, column=2, padx=5, pady=5)

# New components grid layout
address_label.grid(row=4, column=0, padx=5, pady=5)
address_entry.grid(row=4, column=1, padx=5, pady=5)
contact_label.grid(row=5, column=0, padx=5, pady=5)
contact_entry.grid(row=5, column=1, padx=5, pady=5)
device_label.grid(row=6, column=0, padx=5, pady=5)
device_entry.grid(row=6, column=1, padx=5, pady=5)
issue_label.grid(row=7, column=0, padx=5, pady=5)
issue_entry.grid(row=7, column=1, padx=5, pady=5)

add_button.grid(row=8, columnspan=3, padx=5, pady=5)
status_label.grid(row=9, column=0, padx=5, pady=5)
status_combobox.grid(row=9, column=1, padx=5, pady=5)
#update_status_button.grid(row=10, columnspan=3, padx=5, pady=5)

# Admin Page
client_list = tk.Listbox(admin_frame, width=30, height=85)
client_list.bind('<<ListboxSelect>>', show_client_details)
client_info_label = tk.Label(admin_frame, text="", justify="left", width=40)
display_button = tk.Button(admin_frame, text="Display Clients", command=display_clients)
delete_button = tk.Button(admin_frame, text="Delete Client", command=delete_client)
Edit_Item = tk.Button(admin_frame, text="Edit Item", command=edit_client)

client_list.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
client_info_label.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=10)
display_button.pack(side=tk.TOP, padx=10, pady=10)
delete_button.pack(side=tk.TOP, padx=10, pady=10)
Edit_Item.pack(side=tk.TOP, padx=10, pady=10)

# Function to switch between pages
def show_technician_page():
    admin_frame.pack_forget()
    technician_frame.pack()


def show_admin_page():
    # Create a separate login window
    admin_login_window = tk.Toplevel(root)
    admin_login_window.title("Admin Login")
    admin_login_window.geometry("300x200")
    admin_login_window.resizable(False, False)

    # Function to check credentials
    def check_credentials():
        entered_username = username_entry.get()
        entered_password = password_entry.get()

        # Hash the entered password for comparison
        hashed_entered_password = hashlib.sha256(entered_password.encode()).hexdigest()

        # Retrieve the hashed password from the database
        c.execute('''SELECT password FROM AdminLogin WHERE username = ?''', (entered_username,))
        stored_password = c.fetchone()

        if stored_password is not None and stored_password[0] == hashed_entered_password:
            admin_login_window.destroy()
            technician_frame.pack_forget()
            admin_frame.pack()
        else:
            messagebox.showerror("Authentication Failed", "Invalid credentials. Access denied.")

    # Function to handle "Forgot Password" functionality
    def forgot_password():
        # Create a separate window for password reset
        reset_password_window = tk.Toplevel(admin_login_window)
        reset_password_window.title("Reset Password")
        reset_password_window.geometry("300x175")
        reset_password_window.resizable(False, False)

        # Function to update the password in the database
        def update_password():
            entered_username = username_entry.get()
            entered_new_password = new_password_entry.get()

            # Hash the new password for storage
            hashed_new_password = hashlib.sha256(entered_new_password.encode()).hexdigest()

            # Update the password in the database
            c.execute('''UPDATE AdminLogin SET password = ? WHERE username = ?''', (hashed_new_password, entered_username))
            conn.commit()

            messagebox.showinfo("Password Reset", "Password reset successful. You can now log in with the new password.")
            reset_password_window.destroy()

        # GUI components for the password reset window
        new_password_info = tk.Label(reset_password_window, text="Enter The Correct Username First\n"
                                                                 "On The Login Window Before You\n"
                                                                 "Before You Can Change The Password")
        new_password_label = tk.Label(reset_password_window, text="Enter New Password")
        new_password_entry = tk.Entry(reset_password_window, show='*')
        update_button = tk.Button(reset_password_window, text="Update Password", command=update_password)

        new_password_info.pack(pady=7)
        new_password_label.pack(pady=3)
        new_password_entry.pack(pady=10)
        update_button.pack(pady=10)

    # GUI components for the login window
    username_label = tk.Label(admin_login_window, text="Enter Username:")
    username_entry = tk.Entry(admin_login_window)
    password_label = tk.Label(admin_login_window, text="Enter Password:")
    password_entry = tk.Entry(admin_login_window, show='*')

    login_button = tk.Button(admin_login_window, text="Login", command=check_credentials)
    forgot_password_button = tk.Button(admin_login_window, text="Forgot Password", command=forgot_password)

    username_label.pack(pady=5)
    username_entry.pack(pady=5)
    password_label.pack(pady=5)
    password_entry.pack(pady=5)
    login_button.pack(pady=5)
    forgot_password_button.pack(pady=5)


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
