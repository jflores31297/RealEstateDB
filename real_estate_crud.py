import mysql.connector  # Import MySQL connector library to interact with MySQL database
from mysql.connector import Error  # Import Error class for exception handling










# Function to establish a connection to the MySQL database
def connect_db():
    try:
        # Attempt to connect to the database with specified credentials
        conn = mysql.connector.connect(
            host="localhost",  # Change this if the database is hosted elsewhere
            user="root",  # Replace with your MySQL username
            password="Macbook312",  # Replace with your MySQL password
            database="RealEstateDB"  # The name of the database
        )
        if conn.is_connected():
            print("Connected to the database!")  # Confirmation message
        return conn  # Return the database connection object
    except Error as e:
        print(f"Error: {e}")  # Print any connection errors
        return None  # Return None if connection fails











#  Property Table CRUD Functions
# Function to create a new property record
def create_property(cursor):
    # Collect user input for property details
    address = input("Enter address: ")
    city = input("Enter city: ")
    state = input("Enter state: ")
    zip_code = input("Enter zip code: ")
    property_type = input("Enter property type (Single Family, Apartment, Commercial, Condo): ")
    square_feet = input("Enter square feet: ")
    year_built = input("Enter year built: ")
    purchase_date = input("Enter purchase date (YYYY-MM-DD): ")
    purchase_price = input("Enter purchase price: ")

    # SQL query to insert the collected data into the Property table
    query = """
    INSERT INTO Property (address, city, state, zip_code, property_type, square_feet, year_built, purchase_date, purchase_price)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (address, city, state, zip_code, property_type, square_feet, year_built, purchase_date, purchase_price)

    # Execute the query with provided values
    cursor.execute(query, values)


# Function to read and display all properties from the database
def read_properties(cursor):
    cursor.execute("SELECT * FROM Property")  # Execute query to fetch all property records
    properties = cursor.fetchall()  # Fetch all results
    for prop in properties:
        print(prop)  # Print each property record


# Function to update multiple fields of a property record
def update_property(cursor):
    prop_id = input("Enter the Property ID to update: ")  # Get the property ID

    # Dictionary mapping option numbers to column names
    fields = {
        "1": "address",
        "2": "city",
        "3": "state",
        "4": "zip_code",
        "5": "property_type",
        "6": "square_feet",
        "7": "year_built",
        "8": "purchase_date",
        "9": "purchase_price"
    }

    updates = {}  # Dictionary to store fields and new values

    print("\nWhich fields would you like to update?")
    print(
        "1. Address\n2. City\n3. State\n4. Zip Code\n5. Property Type\n6. Square Feet\n7. Year Built\n8. Purchase Date\n9. Purchase Price")
    print("Enter multiple numbers separated by commas (e.g., 1,3,5) or 'all' to update everything.")

    choices = input("Enter your choices: ").strip()  # Get user input

    if choices.lower() == "all":
        selected_fields = fields.keys()  # Select all fields
    else:
        selected_fields = choices.split(",")  # Convert input into a list

    for choice in selected_fields:
        choice = choice.strip()  # Remove any spaces
        if choice in fields:
            new_value = input(f"Enter new value for {fields[choice]}: ")
            updates[fields[choice]] = new_value
        else:
            print(f"Invalid choice: {choice}. Skipping...")

    if not updates:
        print("No valid fields selected. Returning to menu.")
        return

    # Construct the SQL UPDATE query dynamically
    set_clause = ", ".join(f"{field} = %s" for field in updates.keys())  # SQL SET clause
    query = f"UPDATE Property SET {set_clause} WHERE property_id = %s"

    values = list(updates.values()) + [prop_id]  # Values for query execution
    cursor.execute(query, values)  # Execute query

    print("Property updated successfully!")


# Function to delete a property based on its ID
def delete_property(cursor):
    prop_id = input("Enter property ID to delete: ")  # Get property ID to delete
    query = "DELETE FROM Property WHERE property_id = %s"  # SQL delete query
    cursor.execute(query, (prop_id,))  # Execute delete query










# Owner Table CRUD Functions
# Create a new owner record
def create_owner(cursor):
    """Insert a new owner into the Owner table."""
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")
    mailing_address = input("Enter mailing address: ")

    query = """
    INSERT INTO Owner (first_name, last_name, email, phone, mailing_address)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (first_name, last_name, email, phone, mailing_address)

    try:
        cursor.execute(query, values)
        print("Owner added successfully!")
    except Error as e:
        print(f"Error: {e}")


# View all Owners
def read_owners(cursor):
    """Retrieve and display all owners from the Owner table."""
    query = "SELECT * FROM Owner"

    cursor.execute(query)
    owners = cursor.fetchall()

    if not owners:
        print("No owners found.")
        return

    print("\nOwner Records:")
    print("-" * 50)
    for owner in owners:
        print(f"ID: {owner[0]}, Name: {owner[1]} {owner[2]}, Email: {owner[3]}, Phone: {owner[4]}, Address: {owner[5]}")


# Update an owner record
def update_owner(cursor):
    """Update an owner's information based on their ID."""
    owner_id = input("Enter the Owner ID to update: ")

    fields = {
        "1": "first_name",
        "2": "last_name",
        "3": "email",
        "4": "phone",
        "5": "mailing_address"
    }

    print("\nWhich field would you like to update?")
    print("1. First Name\n2. Last Name\n3. Email\n4. Phone\n5. Mailing Address")
    print("Enter multiple numbers separated by commas (e.g., 1,3) or 'all' to update everything.")

    choices = input("Enter your choices: ").strip()

    if choices.lower() == "all":
        selected_fields = fields.keys()
    else:
        selected_fields = choices.split(",")

    updates = {}
    for choice in selected_fields:
        choice = choice.strip()
        if choice in fields:
            new_value = input(f"Enter new value for {fields[choice]}: ")
            updates[fields[choice]] = new_value
        else:
            print(f"Invalid choice: {choice}. Skipping...")

    if not updates:
        print("No valid fields selected. Returning to menu.")
        return

    set_clause = ", ".join(f"{field} = %s" for field in updates.keys())
    query = f"UPDATE Owner SET {set_clause} WHERE owner_id = %s"
    values = list(updates.values()) + [owner_id]

    try:
        cursor.execute(query, values)
        print("Owner updated successfully!")
    except Error as e:
        print(f"Error: {e}")


# Delete an Owner Record
def delete_owner(cursor):
    """Delete an owner record by ID."""
    owner_id = input("Enter Owner ID to delete: ")

    confirm = input("Are you sure you want to delete this owner? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion canceled.")
        return

    query = "DELETE FROM Owner WHERE owner_id = %s"

    try:
        cursor.execute(query, (owner_id,))
        print("Owner deleted successfully!")
    except Error as e:
        print(f"Error: {e}")











# Tenant Table CRUD Functions
# Create a new Tenant record
def create_tenant(cursor):
    """Insert a new tenant into the Tenant table."""
    tenant_id = input("Enter Tenant ID: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")
    employer = input("Enter employer: ")
    emergency_contact = input("Enter emergency contact number: ")

    query = """
    INSERT INTO Tenant (tenant_id, first_name, last_name, email, phone, employer, emergency_contact)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (tenant_id, first_name, last_name, email, phone, employer, emergency_contact)

    try:
        cursor.execute(query, values)
        print("Tenant added successfully!")
    except Error as e:
        print(f"Error: {e}")


# Read and Display all Tenants
def read_tenants(cursor):
    """Retrieve and display all tenants from the Tenant table."""
    query = "SELECT * FROM Tenant"

    cursor.execute(query)
    tenants = cursor.fetchall()

    if not tenants:
        print("No tenants found.")
        return

    print("\nTenant Records:")
    print("-" * 80)
    for tenant in tenants:
        print(
            f"ID: {tenant[0]}, Name: {tenant[1]} {tenant[2]}, Email: {tenant[3]}, Phone: {tenant[4]}, Employer: {tenant[5]}, Emergency Contact: {tenant[6]}")


# Update a Tenant's information
def update_tenant(cursor):
    """Update a tenant's information based on their ID."""
    tenant_id = input("Enter the Tenant ID to update: ")

    fields = {
        "1": "first_name",
        "2": "last_name",
        "3": "email",
        "4": "phone",
        "5": "employer",
        "6": "emergency_contact"
    }

    print("\nWhich field would you like to update?")
    print("1. First Name\n2. Last Name\n3. Email\n4. Phone\n5. Employer\n6. Emergency Contact")
    print("Enter multiple numbers separated by commas (e.g., 1,3) or 'all' to update everything.")

    choices = input("Enter your choices: ").strip()

    if choices.lower() == "all":
        selected_fields = fields.keys()
    else:
        selected_fields = choices.split(",")

    updates = {}
    for choice in selected_fields:
        choice = choice.strip()
        if choice in fields:
            new_value = input(f"Enter new value for {fields[choice]}: ")
            updates[fields[choice]] = new_value
        else:
            print(f"Invalid choice: {choice}. Skipping...")

    if not updates:
        print("No valid fields selected. Returning to menu.")
        return

    set_clause = ", ".join(f"{field} = %s" for field in updates.keys())
    query = f"UPDATE Tenant SET {set_clause} WHERE tenant_id = %s"
    values = list(updates.values()) + [tenant_id]

    try:
        cursor.execute(query, values)
        print("Tenant updated successfully!")
    except Error as e:
        print(f"Error: {e}")

    # Delete a Tenant record


def delete_tenant(cursor):
    """Delete a tenant record by ID."""
    tenant_id = input("Enter Tenant ID to delete: ")

    confirm = input("Are you sure you want to delete this tenant? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion canceled.")
        return

    query = "DELETE FROM Tenant WHERE tenant_id = %s"

    try:
        cursor.execute(query, (tenant_id,))
        print("Tenant deleted successfully!")
    except Error as e:
        print(f"Error: {e}")










# Lease Table CRUD Functions
# Create a new Lease record
def create_lease(cursor):
    """Insert a new lease into the Lease table."""
    lease_id = input("Enter Lease ID: ")
    property_id = input("Enter Property ID: ")
    tenant_id = input("Enter Tenant ID: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    monthly_rent = input("Enter monthly rent amount: ")
    security_deposit = input("Enter security deposit amount (or leave blank for none): ")
    lease_status = input("Enter lease status (Active, Expired, Terminated): ")

    if security_deposit == "":
        security_deposit = None

    query = """
    INSERT INTO Lease (lease_id, property_id, tenant_id, start_date, end_date, monthly_rent, security_deposit, lease_status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (lease_id, property_id, tenant_id, start_date, end_date, monthly_rent, security_deposit, lease_status)

    try:
        cursor.execute(query, values)
        print("Lease added successfully!")
    except Error as e:
        print(f"Error: {e}")


# Read and Display all Lease records
def read_leases(cursor):
    """Retrieve and display all leases from the Lease table."""
    query = "SELECT * FROM Lease"

    cursor.execute(query)
    leases = cursor.fetchall()

    if not leases:
        print("No leases found.")
        return

    print("\nLease Records:")
    print("-" * 100)
    for lease in leases:
        print(
            f"Lease ID: {lease[0]}, Property ID: {lease[1]}, Tenant ID: {lease[2]}, Start: {lease[3]}, End: {lease[4]}, Rent: ${lease[5]}, Deposit: ${lease[6]}, Status: {lease[7]}")


# Update a Lease record
def update_lease(cursor):
    """Update a lease record based on lease ID."""
    lease_id = input("Enter Lease ID to update: ")

    fields = {
        "1": "property_id",
        "2": "tenant_id",
        "3": "start_date",
        "4": "end_date",
        "5": "monthly_rent",
        "6": "security_deposit",
        "7": "lease_status"
    }

    print("\nWhich field would you like to update?")
    print(
        "1. Property ID\n2. Tenant ID\n3. Start Date\n4. End Date\n5. Monthly Rent\n6. Security Deposit\n7. Lease Status")
    print("Enter multiple numbers separated by commas (e.g., 1,3) or 'all' to update everything.")

    choices = input("Enter your choices: ").strip()

    if choices.lower() == "all":
        selected_fields = fields.keys()
    else:
        selected_fields = choices.split(",")

    updates = {}
    for choice in selected_fields:
        choice = choice.strip()
        if choice in fields:
            new_value = input(f"Enter new value for {fields[choice]}: ")
            updates[fields[choice]] = new_value
        else:
            print(f"Invalid choice: {choice}. Skipping...")

    if not updates:
        print("No valid fields selected. Returning to menu.")
        return

    set_clause = ", ".join(f"{field} = %s" for field in updates.keys())
    query = f"UPDATE Lease SET {set_clause} WHERE lease_id = %s"
    values = list(updates.values()) + [lease_id]

    try:
        cursor.execute(query, values)
        print("Lease updated successfully!")
    except Error as e:
        print(f"Error: {e}")


# Delete a Lease record
def delete_lease(cursor):
    """Delete a lease record by ID."""
    lease_id = input("Enter Lease ID to delete: ")

    confirm = input("Are you sure you want to delete this lease? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion canceled.")
        return

    query = "DELETE FROM Lease WHERE lease_id = %s"

    try:
        cursor.execute(query, (lease_id,))
        print("Lease deleted successfully!")
    except Error as e:
        print(f"Error: {e}")














# MaintenanceRequest Table CRUD Functions
# Create a new Maintenance Request
def create_maintenance_request(cursor):
    """Insert a new maintenance request into the MaintenanceRequest table."""
    request_id = input("Enter Request ID: ")
    property_id = input("Enter Property ID: ")
    tenant_id = input("Enter Tenant ID: ")
    employee_id = input("Enter Employee ID (or leave blank if unassigned): ")
    description = input("Enter maintenance request description: ")
    request_date = input("Enter request date (YYYY-MM-DD) or press Enter for today: ")
    completion_date = input("Enter completion date (YYYY-MM-DD) or leave blank if not completed: ")
    status = input("Enter request status (Open, In Progress, Completed): ")

    if employee_id == "":
        employee_id = None
    if request_date == "":
        request_date = None  # Default to CURRENT_DATE in SQL
    if completion_date == "":
        completion_date = None

    query = """
    INSERT INTO MaintenanceRequest (request_id, property_id, tenant_id, employee_id, description, request_date, completion_date, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (request_id, property_id, tenant_id, employee_id, description, request_date, completion_date, status)

    try:
        cursor.execute(query, values)
        print("Maintenance request added successfully!")
    except Error as e:
        print(f"Error: {e}")


# Read and Display all maintenance requests
def read_maintenance_requests(cursor):
    """Retrieve and display all maintenance requests from the database."""
    query = "SELECT * FROM MaintenanceRequest"

    cursor.execute(query)
    requests = cursor.fetchall()

    if not requests:
        print("No maintenance requests found.")
        return

    print("\nMaintenance Requests:")
    print("-" * 120)
    for req in requests:
        print(
            f"Request ID: {req[0]}, Property ID: {req[1]}, Tenant ID: {req[2]}, Employee ID: {req[3] or 'Unassigned'},")
        print(
            f"Description: {req[4]}, Request Date: {req[5]}, Completion Date: {req[6] or 'Pending'}, Status: {req[7]}\n")


# Update a maintenance request
def update_maintenance_request(cursor):
    """Update a maintenance request based on request ID."""
    request_id = input("Enter Request ID to update: ")

    fields = {
        "1": "property_id",
        "2": "tenant_id",
        "3": "employee_id",
        "4": "description",
        "5": "request_date",
        "6": "completion_date",
        "7": "status"
    }

    print("\nWhich field would you like to update?")
    print(
        "1. Property ID\n2. Tenant ID\n3. Employee ID\n4. Description\n5. Request Date\n6. Completion Date\n7. Status")
    print("Enter multiple numbers separated by commas (e.g., 1,3) or 'all' to update everything.")

    choices = input("Enter your choices: ").strip()

    if choices.lower() == "all":
        selected_fields = fields.keys()
    else:
        selected_fields = choices.split(",")

    updates = {}
    for choice in selected_fields:
        choice = choice.strip()
        if choice in fields:
            new_value = input(f"Enter new value for {fields[choice]}: ")
            if new_value == "":
                new_value = None
            updates[fields[choice]] = new_value
        else:
            print(f"Invalid choice: {choice}. Skipping...")

    if not updates:
        print("No valid fields selected. Returning to menu.")
        return

    set_clause = ", ".join(f"{field} = %s" for field in updates.keys())
    query = f"UPDATE MaintenanceRequest SET {set_clause} WHERE request_id = %s"
    values = list(updates.values()) + [request_id]

    try:
        cursor.execute(query, values)
        print("Maintenance request updated successfully!")
    except Error as e:
        print(f"Error: {e}")


# Delete a Maintenance Request
def delete_maintenance_request(cursor):
    """Delete a maintenance request by ID."""
    request_id = input("Enter Request ID to delete: ")

    confirm = input("Are you sure you want to delete this request? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion canceled.")
        return

    query = "DELETE FROM MaintenanceRequest WHERE request_id = %s"

    try:
        cursor.execute(query, (request_id,))
        print("Maintenance request deleted successfully!")
    except Error as e:
        print(f"Error: {e}")











# Payment Table CRUD Functions
# Create a new Payment
def create_payment(cursor):
    """Insert a new payment into the Payment table."""
    payment_id = input("Enter Payment ID: ")
    lease_id = input("Enter Lease ID: ")
    tenant_id = input("Enter Tenant ID: ")
    amount = input("Enter Payment Amount: ")
    payment_date = input("Enter Payment Date (YYYY-MM-DD): ")
    print("Available Payment Methods: Credit Card, Check, Bank Transfer, Cash")
    payment_method = input("Enter Payment Method: ")
    received_by = input("Enter Employee ID who received the payment (or leave blank if unknown): ")

    if received_by == "":
        received_by = None

    query = """
    INSERT INTO Payment (payment_id, lease_id, tenant_id, amount, payment_date, payment_method, received_by)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (payment_id, lease_id, tenant_id, amount, payment_date, payment_method, received_by)

    try:
        cursor.execute(query, values)
        print("Payment record added successfully!")
    except Error as e:
        print(f"Error: {e}")


# Read and Display all payments
def read_payments(cursor):
    """Retrieve and display all payments from the database."""
    query = "SELECT * FROM Payment"

    cursor.execute(query)
    payments = cursor.fetchall()

    if not payments:
        print("No payments found.")
        return

    print("\nPayments:")
    print("-" * 100)
    for pay in payments:
        print(f"Payment ID: {pay[0]}, Lease ID: {pay[1]}, Tenant ID: {pay[2]}, Amount: ${pay[3]:.2f},")
        print(f"Payment Date: {pay[4]}, Method: {pay[5]}, Received By: {pay[6] or 'Unknown'}\n")


# Update a Payment record
def update_payment(cursor):
    """Update payment details based on payment ID."""
    payment_id = input("Enter Payment ID to update: ")

    fields = {
        "1": "lease_id",
        "2": "tenant_id",
        "3": "amount",
        "4": "payment_date",
        "5": "payment_method",
        "6": "received_by"
    }

    print("\nWhich field(s) would you like to update?")
    print("1. Lease ID\n2. Tenant ID\n3. Amount\n4. Payment Date\n5. Payment Method\n6. Received By")
    print("Enter multiple numbers separated by commas (e.g., 1,3) or 'all' to update everything.")

    choices = input("Enter your choices: ").strip()

    if choices.lower() == "all":
        selected_fields = fields.keys()
    else:
        selected_fields = choices.split(",")

    updates = {}
    for choice in selected_fields:
        choice = choice.strip()
        if choice in fields:
            new_value = input(f"Enter new value for {fields[choice]}: ")
            if new_value == "":
                new_value = None
            updates[fields[choice]] = new_value
        else:
            print(f"Invalid choice: {choice}. Skipping...")

    if not updates:
        print("No valid fields selected. Returning to menu.")
        return

    set_clause = ", ".join(f"{field} = %s" for field in updates.keys())
    query = f"UPDATE Payment SET {set_clause} WHERE payment_id = %s"
    values = list(updates.values()) + [payment_id]

    try:
        cursor.execute(query, values)
        print("Payment record updated successfully!")
    except Error as e:
        print(f"Error: {e}")


# Delete a Payment record
def delete_payment(cursor):
    """Delete a payment record by ID."""
    payment_id = input("Enter Payment ID to delete: ")

    confirm = input("Are you sure you want to delete this payment record? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion canceled.")
        return

    query = "DELETE FROM Payment WHERE payment_id = %s"

    try:
        cursor.execute(query, (payment_id,))
        print("Payment record deleted successfully!")
    except Error as e:
        print(f"Error: {e}")









# Employee Table CRUD Functions
# Create a new employee record
def create_employee(cursor):
    """Insert a new employee into the Employee table."""
    employee_id = input("Enter Employee ID: ")
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone Number: ")
    print("Available Roles: Property Manager, Maintenance Staff, Accountant, Leasing Agent")
    role = input("Enter Role: ")
    hire_date = input("Enter Hire Date (YYYY-MM-DD): ")

    query = """
    INSERT INTO Employee (employee_id, first_name, last_name, email, phone, role, hire_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (employee_id, first_name, last_name, email, phone, role, hire_date)

    try:
        cursor.execute(query, values)
        print("Employee record added successfully!")
    except Error as e:
        print(f"Error: {e}")


# Read and Display all Employee records
def read_employees(cursor):
    """Retrieve and display all employees from the database."""
    query = "SELECT * FROM Employee"

    cursor.execute(query)
    employees = cursor.fetchall()

    if not employees:
        print("No employees found.")
        return

    print("\nEmployees:")
    print("-" * 100)
    for emp in employees:
        print(f"Employee ID: {emp[0]}, Name: {emp[1]} {emp[2]}, Email: {emp[3]}")
        print(f"Phone: {emp[4]}, Role: {emp[5]}, Hire Date: {emp[6]}\n")


# Update an Employee record
def update_employee(cursor):
    """Update employee details based on employee ID."""
    employee_id = input("Enter Employee ID to update: ")

    fields = {
        "1": "first_name",
        "2": "last_name",
        "3": "email",
        "4": "phone",
        "5": "role",
        "6": "hire_date"
    }

    print("\nWhich field(s) would you like to update?")
    print("1. First Name\n2. Last Name\n3. Email\n4. Phone\n5. Role\n6. Hire Date")
    print("Enter multiple numbers separated by commas (e.g., 1,3) or 'all' to update everything.")

    choices = input("Enter your choices: ").strip()

    if choices.lower() == "all":
        selected_fields = fields.keys()
    else:
        selected_fields = choices.split(",")

    updates = {}
    for choice in selected_fields:
        choice = choice.strip()
        if choice in fields:
            new_value = input(f"Enter new value for {fields[choice]}: ")
            if new_value == "":
                new_value = None
            updates[fields[choice]] = new_value
        else:
            print(f"Invalid choice: {choice}. Skipping...")

    if not updates:
        print("No valid fields selected. Returning to menu.")
        return

    set_clause = ", ".join(f"{field} = %s" for field in updates.keys())
    query = f"UPDATE Employee SET {set_clause} WHERE employee_id = %s"
    values = list(updates.values()) + [employee_id]

    try:
        cursor.execute(query, values)
        print("Employee record updated successfully!")
    except Error as e:
        print(f"Error: {e}")


# Delete an Employee record
def delete_employee(cursor):
    """Delete an employee record by ID."""
    employee_id = input("Enter Employee ID to delete: ")

    confirm = input("Are you sure you want to delete this employee record? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion canceled.")
        return

    query = "DELETE FROM Employee WHERE employee_id = %s"

    try:
        cursor.execute(query, (employee_id,))
        print("Employee record deleted successfully!")
    except Error as e:
        print(f"Error: {e}")

# PropertyOwner Table CRUD Functions
# Create a new Property/Owner record
def create_property_owner(cursor):
    """Insert a new record into the PropertyOwner table."""
    property_id = input("Enter Property ID: ")
    owner_id = input("Enter Owner ID: ")
    ownership_percentage = input("Enter Ownership Percentage: ")

    query = """
    INSERT INTO PropertyOwner (property_id, owner_id, ownership_percentage)
    VALUES (%s, %s, %s)
    """
    values = (property_id, owner_id, ownership_percentage)

    try:
        cursor.execute(query, values)
        print("PropertyOwner record added successfully!")
    except Error as e:
        print(f"Error: {e}")


# Read and Display all PropertyOwner records
def read_property_owners(cursor):
    """Retrieve and display all PropertyOwner records."""
    query = "SELECT * FROM PropertyOwner"

    cursor.execute(query)
    records = cursor.fetchall()

    if not records:
        print("No PropertyOwner records found.")
        return

    print("\nProperty Owners:")
    print("-" * 100)
    for record in records:
        print(f"Property ID: {record[0]}, Owner ID: {record[1]}, Ownership Percentage: {record[2]}%")


# Udate an ownership percentage
def update_property_owner(cursor):
    """Update the ownership percentage for a property-owner relationship."""
    property_id = input("Enter Property ID: ")
    owner_id = input("Enter Owner ID: ")
    new_percentage = input("Enter new Ownership Percentage: ")

    query = """
    UPDATE PropertyOwner
    SET ownership_percentage = %s
    WHERE property_id = %s AND owner_id = %s
    """
    values = (new_percentage, property_id, owner_id)

    try:
        cursor.execute(query, values)
        print("Ownership percentage updated successfully!")
    except Error as e:
        print(f"Error: {e}")


# Delete a Property/Owner record
def delete_property_owner(cursor):
    """Delete a property-owner relationship by property and owner ID."""
    property_id = input("Enter Property ID: ")
    owner_id = input("Enter Owner ID: ")

    confirm = input("Are you sure you want to remove this property-owner relationship? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion canceled.")
        return

    query = "DELETE FROM PropertyOwner WHERE property_id = %s AND owner_id = %s"

    try:
        cursor.execute(query, (property_id, owner_id))
        print("Property-owner record deleted successfully!")
    except Error as e:
        print(f"Error: {e}")








# Function to manage CRUD operations for different tables dynamically
def manage_table(table_name):
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()

    while True:
        print(f"\nManaging {table_name}")
        print("1. Create New Record\n2. Display All Records\n3. Update a Record\n4. Delete a Record\n5. Back to main menu")
        choice = input("Choose an option: ")

        if table_name == "Property":
            if choice == "1":
                create_property(cursor)
            elif choice == "2":
                read_properties(cursor)
            elif choice == "3":
                update_property(cursor)
            elif choice == "4":
                delete_property(cursor)
            elif choice == "5":
                break
            else:
                print("Invalid choice!")

        elif table_name == "Owner":
            if choice == "1":
                create_owner(cursor)
            elif choice == "2":
                read_owners(cursor)
            elif choice == "3":
                update_owner(cursor)
            elif choice == "4":
                delete_owner(cursor)
            elif choice == "5":
                break
            else:
                print("Invalid choice!")

        elif table_name == "PropertyOwner":
            if choice == "1":
                create_property_owner(cursor)
            elif choice == "2":
                read_property_owners(cursor)
            elif choice == "3":
                update_property_owner(cursor)
            elif choice == "4":
                delete_property_owner(cursor)
            elif choice == "5":
                break
            else:
                print("Invalid choice!")

        elif table_name == "Tenant":
            if choice == "1":
                create_tenant(cursor)
            elif choice == "2":
                read_tenants(cursor)
            elif choice == "3":
                update_tenant(cursor)
            elif choice == "4":
                delete_tenant(cursor)
            elif choice == "5":
                break
            else:
                print("Invalid choice!")

        elif table_name == "Lease":
            if choice == "1":
                create_lease(cursor)
            elif choice == "2":
                read_leases(cursor)
            elif choice == "3":
                update_lease(cursor)
            elif choice == "4":
                delete_lease(cursor)
            elif choice == "5":
                break
            else:
                print("Invalid choice!")

        elif table_name == "MaintenanceRequest":
            if choice == "1":
                create_maintenance_request(cursor)
            elif choice == "2":
                read_maintenance_requests(cursor)
            elif choice == "3":
                update_maintenance_request(cursor)
            elif choice == "4":
                delete_maintenance_request(cursor)
            elif choice == "5":
                break
            else:
                print("Invalid choice!")

        elif table_name == "Payment":
            if choice == "1":
                create_payment(cursor)
            elif choice == "2":
                read_payments(cursor)
            elif choice == "3":
                update_payment(cursor)
            elif choice == "4":
                delete_payment(cursor)
            elif choice == "5":
                break
            else:
                print("Invalid choice!")

        elif table_name == "Employee":
            if choice == "1":
                create_employee(cursor)
            elif choice == "2":
                read_employees(cursor)
            elif choice == "3":
                update_employee(cursor)
            elif choice == "4":
                delete_employee(cursor)
            elif choice == "5":
                break
            else:
                print("Invalid choice!")

        else:
            print("Invalid table name!")

        conn.commit()

    cursor.close()
    conn.close()














# Main function that provides a menu for managing different database tables
def main():
    while True:
        print("\nReal Estate Property Management CLI")  # Title
        print("1. Manage Properties")
        print("2. Manage Owners")
        print("3. Manage Tenants")
        print("4. Manage Leases")
        print("5. Manage Maintenance Requests")
        print("6. Manage Payments")
        print("7. Exit")

        choice = input("Select an option: ")  # Get user input

        if choice == "1":
            manage_table("Property")  # Call function to manage Property table
        elif choice == "2":
            manage_table("Owner")  # Call function to manage Owner table (not yet implemented)
        elif choice == "3":
            manage_table("Tenant")  # Call function to manage Tenant table (not yet implemented)
        elif choice == "4":
            manage_table("Lease")  # Call function to manage Lease table (not yet implemented)
        elif choice == "5":
            manage_table("MaintenanceRequest")  # Call function to manage MaintenanceRequest table (not yet implemented)
        elif choice == "6":
            manage_table("Payment")  # Call function to manage Payment table (not yet implemented)
        elif choice == "7":
            print("Exiting...")  # Exit message
            break  # Exit the loop and terminate the program
        else:
            print("Invalid choice! Please select a valid option.")  # Handle invalid input

# Entry point of the script - Runs the main function when the script is executed
if __name__ == "__main__":
    main()