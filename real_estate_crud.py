import mysql.connector  # MySQL connector for database interaction
from mysql.connector import Error  # Generic error handling for MySQL-related exceptions
import logging  # For logging errors and issues
import os  # To fetch environment variables for database credentials
from time import sleep  # To introduce delays between retry attempts
import re  # Regular expressions (though not used in this snippet)
from tabulate import tabulate  # For formatting table outputs (requires `pip install tabulate`)
from datetime import datetime  # To manage timestamps in logs

# Configure logging to store error messages in a log file
logging.basicConfig(
    filename='database.log',  # Log file name
    level=logging.ERROR,  # Log only errors
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format includes timestamp, level, and message
)


def connect_db(retries=3, delay=5):
    """
    Attempts to establish a connection to a MySQL database with a retry mechanism.

    :param retries: Number of retry attempts before giving up (default: 3)
    :param delay: Time in seconds to wait between retries (default: 5)
    :return: MySQL connection object if successful, otherwise None
    """
    for attempt in range(retries):  # Loop through the specified number of retries
        try:
            # Fetch database credentials from environment variables with defaults
            db_config = {
                'host': os.getenv('DB_HOST', 'localhost'),  # Default to localhost if not set
                'user': os.getenv('DB_USER', 'root'),  # Default username is 'root'
                'password': os.getenv('DB_PASSWORD', 'Macbook312'),  # Default password
                'database': os.getenv('DB_NAME', 'RealEstateDB'),  # Default database name
                'connect_timeout': 10  # Timeout if connection takes more than 10 seconds
            }

            # Attempt to establish a connection
            conn = mysql.connector.connect(**db_config)

            if conn.is_connected():  # Check if the connection was successful
                print("Connected to the database!")  # Print confirmation
                return conn  # Return the database connection object

        # Handle connection failure due to network issues or incorrect host
        except mysql.connector.errors.InterfaceError as e:
            logging.error(f"Connection attempt {attempt + 1} failed: {e}")  # Log the error
            print(f"Connection attempt {attempt + 1} failed: {e}")  # Display the error message
            if attempt < retries - 1:  # If more retries are available
                sleep(delay)  # Wait before retrying
            else:  # If no more retries left
                print("Max retries reached. Please check your database server.")
                return None  # Return None as connection failed

        # Handle incorrect credentials or SQL syntax errors
        except mysql.connector.errors.ProgrammingError as e:
            logging.error(f"Database error: {e}")  # Log the error
            print(f"Database error: {e}")  # Display the error
            return None  # Return None as connection failed

        # Handle database-related errors, like incorrect database name or access denial
        except mysql.connector.errors.DatabaseError as e:
            logging.error(f"Database not found or access denied: {e}")  # Log the error
            print(f"Database not found or access denied: {e}")  # Display the error
            return None  # Return None as connection failed

        # Catch-all for unexpected MySQL errors
        except Error as e:
            logging.error(f"Unexpected error: {e}")  # Log the error
            print(f"Unexpected error: {e}")  # Display the error
            return None  # Return None as connection failed

    return None  # If all retries fail, return None


# Property Table CRUD Functions

def validate_date(date_str):
    """
    Validate that the provided date string is in YYYY-MM-DD format.

    :param date_str: Date string input from the user.
    :return: The validated date string if correct.
    :raises ValueError: If the format is incorrect.
    """
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):  # Regex pattern for YYYY-MM-DD format
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")  # Raise error if invalid
    return date_str  # Return the validated date


def validate_zip_code(zip_code):
    """
    Validate that the provided zip code follows the US zip code format (5-digit or 9-digit with hyphen).

    :param zip_code: Zip code input from the user.
    :return: The validated zip code if correct.
    :raises ValueError: If the format is incorrect.
    """
    if not re.match(r'^\d{5}(-\d{4})?$', zip_code):  # Regex pattern for US zip codes
        raise ValueError("Invalid zip code format. Please use a valid US zip code.")  # Raise error if invalid
    return zip_code  # Return the validated zip code


def validate_property_type(property_type):
    """
    Validate that the property type is one of the predefined allowed values.

    :param property_type: Property type input from the user.
    :return: The validated property type if correct.
    :raises ValueError: If the type is not allowed.
    """
    allowed_types = ['Single Family', 'Apartment', 'Commercial', 'Condo']  # List of valid property types
    if property_type not in allowed_types:  # Check if the input is in the allowed list
        raise ValueError(
            f"Invalid property type. Allowed values are: {', '.join(allowed_types)}")  # Raise error if invalid
    return property_type  # Return the validated property type


def create_property(cursor):
    """
    Collect user input for a new property and insert it into the Property table.

    :param cursor: MySQL database cursor to execute the SQL query.
    """
    try:
        # Collect required property details from user input
        address = input("Enter address: ").strip()  # Remove extra spaces
        city = input("Enter city: ").strip()
        state = input("Enter state: ").strip()
        zip_code = validate_zip_code(input("Enter zip code: ").strip())  # Validate zip code format
        property_type = validate_property_type(
            input(
                "Enter property type (Single Family, Apartment, Commercial, Condo): ").strip())  # Validate property type

        # Collect optional property details with validation
        square_feet = input("Enter square feet (optional): ").strip()
        square_feet = int(square_feet) if square_feet else None  # Convert input to integer if provided

        year_built = input("Enter year built (optional): ").strip()
        year_built = int(year_built) if year_built else None  # Convert input to integer if provided

        purchase_date = input("Enter purchase date (YYYY-MM-DD, optional): ").strip()
        purchase_date = validate_date(purchase_date) if purchase_date else None  # Validate date if provided

        purchase_price = input("Enter purchase price (optional): ").strip()
        purchase_price = float(purchase_price) if purchase_price else None  # Convert input to float if provided

        # SQL query to insert the collected data into the Property table
        query = """INSERT INTO Property (address, city, state, zip_code, property_type, square_feet, year_built, 
        purchase_date, purchase_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (address, city, state, zip_code, property_type, square_feet, year_built, purchase_date, purchase_price)

        # Execute the query with provided values
        cursor.execute(query, values)
        print("Property record added successfully!")  # Confirm successful addition

    except ValueError as ve:  # Handle validation errors
        print(f"Input validation error: {ve}")
    except Error as e:  # Handle MySQL database errors
        print(f"Database error: {e}")
    except Exception as e:  # Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")


# Function to read and display all properties from the database
def read_properties(cursor):
    """
    Retrieve and display all properties from the database in a formatted table with error handling.

    :param cursor: MySQL database cursor used to execute queries.
    """
    try:
        # Execute SQL query to select relevant property details, ordered by property_id for consistency
        cursor.execute("""
            SELECT 
                property_id, address, city, state, zip_code,
                property_type, square_feet, year_built,
                purchase_date, purchase_price
            FROM Property
            ORDER BY property_id
        """)

        # Fetch all records from the query result
        properties = cursor.fetchall()

        # Check if the database returned any properties
        if not properties:
            print("\nNo properties found in the database.")  # Inform the user if no records exist
            return  # Exit the function if no properties are found

        # Initialize an empty list to store formatted property data
        formatted_properties = []

        # Loop through each property record and format the data for better readability
        for prop in properties:
            formatted_prop = {
                "ID": prop[0],  # Property ID
                "Address": prop[1],  # Street address
                "City": prop[2],  # City name
                "State": prop[3],  # State abbreviation
                "ZIP": prop[4],  # ZIP code
                "Type": prop[5],  # Property type (e.g., Single Family, Condo)
                "Sq Ft": f"{prop[6]:,}" if prop[6] else "N/A",  # Format square feet with commas, or show "N/A" if None
                "Year Built": prop[7] or "N/A",  # Display year built, or "N/A" if not available
                "Purchase Date": prop[8].strftime("%Y-%m-%d") if prop[8] else "N/A",  # Format date or show "N/A"
                "Price": f"${prop[9]:,.2f}" if prop[9] else "N/A"  # Format purchase price with thousands separator
            }
            formatted_properties.append(formatted_prop)  # Add formatted dictionary to the list

        # Print property listings in a tabular format using the tabulate library
        print("\nProperty Listings")  # Section header
        print(tabulate(formatted_properties, headers="keys", tablefmt="grid", stralign="left"))  # Generate a grid table
        print(f"\nTotal properties: {len(properties)}")  # Display total number of properties retrieved

    # Handle MySQL database errors
    except Error as e:
        print(f"\nDatabase error: {e}")  # Print database-related errors

    # Handle any unexpected errors
    except Exception as e:
        print(f"\nUnexpected error: {e}")  # Print general errors for debugging


# Function to update multiple fields of a property record
def update_property(cursor):
    """
    Update multiple fields of a property record with validation and error handling.

    :param cursor: MySQL database cursor used to execute queries.
    """
    try:
        # Prompt user to enter the Property ID they want to update
        prop_id = input("Enter the Property ID to update: ").strip()

        # Check if the property exists in the database
        cursor.execute("SELECT * FROM Property WHERE property_id = %s", (prop_id,))
        property_data = cursor.fetchone()  # Fetch the property record

        if not property_data:  # If no property is found, inform the user and exit
            print(f"Property with ID {prop_id} not found.")
            return

        # Display the current details of the property to the user
        print("\nCurrent Property Details:")
        print(f"1. Address: {property_data[1]}")
        print(f"2. City: {property_data[2]}")
        print(f"3. State: {property_data[3]}")
        print(f"4. Zip Code: {property_data[4]}")
        print(f"5. Property Type: {property_data[5]}")
        print(f"6. Square Feet: {property_data[6]}")
        print(f"7. Year Built: {property_data[7]}")
        print(f"8. Purchase Date: {property_data[8]}")
        print(f"9. Purchase Price: {property_data[9]}")

        # Dictionary mapping user input options to database column names
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

        updates = {}  # Dictionary to store fields to be updated and their new values

        # Display available update options
        print("\nWhich fields would you like to update?")
        print(
            "1. Address\n2. City\n3. State\n4. Zip Code\n5. Property Type\n6. Square Feet\n7. Year Built\n8. Purchase Date\n9. Purchase Price")
        print("Enter multiple numbers separated by commas (e.g., 1,3,5) or 'all' to update everything.")

        choices = input("Enter your choices: ").strip()  # Get user input for fields to update

        if choices.lower() == "all":
            selected_fields = fields.keys()  # Select all fields if user enters 'all'
        else:
            selected_fields = choices.split(",")  # Convert input into a list of selected options

        for choice in selected_fields:
            choice = choice.strip()  # Remove extra spaces from input
            if choice in fields:  # Check if the selected option is valid
                # Prompt user to enter a new value for the selected field
                new_value = input(f"Enter new value for {fields[choice]} (press Enter to skip): ").strip()

                if new_value:  # If user enters a value (not just pressing Enter)
                    # Validate and convert input based on field type
                    if fields[choice] == "zip_code":
                        new_value = validate_zip_code(new_value)  # Validate ZIP code format
                    elif fields[choice] == "property_type":
                        new_value = validate_property_type(new_value)  # Validate property type
                    elif fields[choice] == "purchase_date":
                        new_value = validate_date(new_value)  # Validate date format
                    elif fields[choice] in ["square_feet", "year_built"]:
                        new_value = int(new_value)  # Convert numeric input to an integer
                    elif fields[choice] == "purchase_price":
                        new_value = float(new_value)  # Convert numeric input to a float

                    updates[fields[choice]] = new_value  # Store validated new value in updates dictionary
            else:
                print(f"Invalid choice: {choice}. Skipping...")  # Warn about invalid input and continue

        if not updates:  # If no valid fields were selected for updating
            print("No valid fields selected. Returning to menu.")
            return

        # Display the changes to be made and confirm with the user
        print("\nChanges to be made:")
        for field, value in updates.items():
            print(f"{field}: {value}")

        confirm = input("\nAre you sure you want to update this property? (yes/no): ").strip().lower()
        if confirm != "yes":  # If user does not confirm, cancel the update
            print("Update canceled.")
            return

        # Construct the SQL UPDATE query dynamically
        set_clause = ", ".join(f"{field} = %s" for field in updates.keys())  # Create SQL SET clause
        query = f"UPDATE Property SET {set_clause} WHERE property_id = %s"

        values = list(updates.values()) + [prop_id]  # Prepare values for query execution
        cursor.execute(query, values)  # Execute the query to update the database

        print("Property updated successfully!")  # Inform user of successful update

    except ValueError as ve:  # Handle validation errors
        print(f"Input validation error: {ve}")
    except Error as e:  # Handle database errors
        print(f"Database error: {e}")
    except Exception as e:  # Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")


# Function to delete a property based on its ID
def delete_property(cursor):
    """
    Delete a property record based on its ID with validation and error handling.

    :param cursor: MySQL database cursor used to execute queries.
    """
    try:
        # Prompt user to enter the property ID they want to delete
        prop_id = input("Enter property ID to delete: ").strip()

        # Validate that the entered property ID is a numeric value
        if not prop_id.isdigit():
            print("Invalid property ID. Please enter a numeric value.")
            return  # Exit function if input is invalid

        # Check if the property exists in the database
        cursor.execute("SELECT * FROM Property WHERE property_id = %s", (prop_id,))
        property_data = cursor.fetchone()  # Fetch the property record

        if not property_data:  # If no property is found, inform the user and exit
            print(f"Property with ID {prop_id} not found.")
            return

        # Display property details for confirmation before deletion
        print("\nProperty Details:")
        print(f"ID: {property_data[0]}")
        print(f"Address: {property_data[1]}")
        print(f"City: {property_data[2]}")
        print(f"State: {property_data[3]}")
        print(f"Zip Code: {property_data[4]}")
        print(f"Type: {property_data[5]}")
        print(f"Square Feet: {property_data[6]}")
        print(f"Year Built: {property_data[7]}")
        print(f"Purchase Date: {property_data[8]}")
        print(f"Purchase Price: {property_data[9]}")

        # Ask the user for final confirmation before deleting the record
        confirm = input("\nAre you sure you want to delete this property? (yes/no): ").strip().lower()
        if confirm != "yes":  # If user does not confirm, cancel the deletion
            print("Deletion canceled.")
            return

        # Execute the SQL DELETE query to remove the property from the database
        query = "DELETE FROM Property WHERE property_id = %s"
        cursor.execute(query, (prop_id,))

        # Check if the deletion was successful by verifying affected rows
        if cursor.rowcount > 0:
            print(f"Property with ID {prop_id} deleted successfully!")  # Success message
        else:
            print(f"No property found with ID {prop_id}.")  # Edge case: Record not deleted

    except Error as e:  # Handle database-related errors
        print(f"Database error: {e}")
    except Exception as e:  # Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")


def validate_email(email):
    """
    Validate that the given email follows a standard format.

    :param email: The email address to validate.
    :return: The email address if it is valid.
    :raises ValueError: If the email format is invalid.
    """
    # Regular expression pattern to match a valid email format
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Check if the email matches the expected pattern
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format. Please enter a valid email address.")

    return email  # Return the email if it is valid


def validate_phone(phone):
    """
    Validate that the given phone number follows a valid US format.

    :param phone: The phone number to validate.
    :return: The phone number if it is valid.
    :raises ValueError: If the phone number format is invalid.
    """
    # Regular expression pattern to match various US phone number formats
    phone_pattern = r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'

    # Check if the phone number matches the expected pattern
    if not re.match(phone_pattern, phone):
        raise ValueError("Invalid phone number format. Please use (123) 456-7890 or 123-456-7890.")

    return phone  # Return the phone number if it is valid


# Owner Table CRUD Functions
# Function to create a new owner record
def create_owner(cursor):
    """
    Insert a new owner into the Owner table with validation and error handling.

    :param cursor: MySQL database cursor used to execute queries.
    """
    try:
        # Collect user input for owner's first name
        first_name = input("Enter first name: ").strip()
        if not first_name:  # Ensure first name is not empty
            raise ValueError("First name is required.")

        # Collect user input for owner's last name
        last_name = input("Enter last name: ").strip()
        if not last_name:  # Ensure last name is not empty
            raise ValueError("Last name is required.")

        # Collect and validate email input
        email = validate_email(input("Enter email: ").strip())
        if not email:  # Ensure email is not empty
            raise ValueError("Email is required.")

        # Collect phone number input (optional)
        phone = input("Enter phone number (optional): ").strip()
        if phone:  # If phone is provided, validate its format
            phone = validate_phone(phone)

        # Collect mailing address input (optional)
        mailing_address = input("Enter mailing address (optional): ").strip()
        if not mailing_address:  # Convert empty input to None for database compatibility
            mailing_address = None

        # SQL query to insert the collected data into the Owner table
        query = """
        INSERT INTO Owner (first_name, last_name, email, phone, mailing_address)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (first_name, last_name, email, phone, mailing_address)  # Tuple of values for query execution

        # Execute the SQL query with provided values
        cursor.execute(query, values)

        # Confirmation message upon successful insertion
        print("Owner added successfully!")

    except ValueError as ve:  # Handle validation errors
        print(f"Input validation error: {ve}")
    except Error as e:  # Handle database-related errors
        print(f"Database error: {e}")
    except Exception as e:  # Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")


# Function to view all owners with pagination
def read_owners(cursor, page_size=10):
    """
    Retrieve and display all owners in a formatted table with pagination and error handling.

    :param cursor: MySQL database cursor used to execute queries.
    :param page_size: Number of records to display per page (default: 10).
    """
    try:
        # Execute SQL query to fetch all owner records, ordered by owner_id
        cursor.execute("SELECT * FROM Owner ORDER BY owner_id")
        owners = cursor.fetchall()  # Fetch all records from the query result

        # Check if the Owner table has any records
        if not owners:
            print("\nNo owners found.")
            return  # Exit the function if no records exist

        # Convert fetched records into a formatted list of dictionaries for better readability
        formatted_owners = []
        for owner in owners:
            formatted_owner = {
                "ID": owner[0],  # Owner ID
                "First Name": owner[1],  # Owner's first name
                "Last Name": owner[2],  # Owner's last name
                "Email": owner[3],  # Email address
                "Phone": owner[4] or "N/A",  # Handle NULL values by replacing with "N/A"
                "Address": owner[5] or "N/A"  # Handle NULL values by replacing with "N/A"
            }
            formatted_owners.append(formatted_owner)

        # Initialize pagination variables
        total_owners = len(formatted_owners)  # Total number of owner records
        start_index = 0  # Start index for displaying records

        # Paginate through the results
        while start_index < total_owners:
            # Display a subset of owners as per the page size
            print("\nOwner Records:")
            print(tabulate(formatted_owners[start_index:start_index + page_size], headers="keys", tablefmt="grid", stralign="left"))
            print(f"\nDisplaying {start_index + 1} to {min(start_index + page_size, total_owners)} of {total_owners} owners.")

            # Check if there are more records to display
            if start_index + page_size < total_owners:
                # Prompt user to continue or quit pagination
                next_page = input("\nPress Enter to view the next page or 'q' to quit: ").strip().lower()
                if next_page == 'q':  # If user enters 'q', exit pagination loop
                    break
            start_index += page_size  # Move to the next page

    except Error as e:  # Handle database-related errors
        print(f"\nDatabase error: {e}")
    except Exception as e:  # Handle any unexpected errors
        print(f"\nAn unexpected error occurred: {e}")


# Function to update an owner record
def update_owner(cursor):
    """
    Update an owner's information based on their ID with validation and error handling.

    :param cursor: Database cursor used to execute SQL queries.
    """
    try:
        # Prompt user to enter the Owner ID they want to update
        owner_id = input("Enter the Owner ID to update: ").strip()

        # Check if the owner exists in the database
        cursor.execute("SELECT * FROM Owner WHERE owner_id = %s", (owner_id,))
        owner_data = cursor.fetchone()

        # If no matching owner is found, exit the function
        if not owner_data:
            print(f"Owner with ID {owner_id} not found.")
            return

        # Display the current owner details for reference
        print("\nCurrent Owner Details:")
        print(f"1. First Name: {owner_data[1]}")
        print(f"2. Last Name: {owner_data[2]}")
        print(f"3. Email: {owner_data[3]}")
        print(f"4. Phone: {owner_data[4] or 'N/A'}")  # Show 'N/A' if phone is NULL
        print(f"5. Mailing Address: {owner_data[5] or 'N/A'}")  # Show 'N/A' if address is NULL

        # Dictionary mapping input choices to database column names
        fields = {
            "1": "first_name",
            "2": "last_name",
            "3": "email",
            "4": "phone",
            "5": "mailing_address"
        }

        updates = {}  # Dictionary to store fields and new values

        # Prompt the user to select fields to update
        print("\nWhich fields would you like to update?")
        print("1. First Name\n2. Last Name\n3. Email\n4. Phone\n5. Mailing Address")
        print("Enter multiple numbers separated by commas (e.g., 1,3) or 'all' to update everything.")

        # Get user's field selection
        choices = input("Enter your choices: ").strip()

        # If user chooses "all", update all fields; otherwise, split input into a list
        if choices.lower() == "all":
            selected_fields = fields.keys()  # Select all available fields
        else:
            selected_fields = choices.split(",")  # Convert input string into a list

        # Loop through selected fields and prompt for new values
        for choice in selected_fields:
            choice = choice.strip()  # Remove any extra spaces
            if choice in fields:  # Ensure choice is valid
                new_value = input(f"Enter new value for {fields[choice]} (press Enter to skip): ").strip()

                if new_value:  # Only update if user provides input
                    # Validate and convert input based on field type
                    if fields[choice] == "email":
                        new_value = validate_email(new_value)  # Ensure email format is valid
                    elif fields[choice] == "phone":
                        new_value = validate_phone(new_value)  # Ensure phone format is valid
                    elif fields[choice] in ["first_name", "last_name"] and not new_value:
                        # Prevent empty first or last name
                        raise ValueError(f"{fields[choice]} cannot be empty.")

                    # Store the field and its new value for updating
                    updates[fields[choice]] = new_value
            else:
                print(f"Invalid choice: {choice}. Skipping...")

        # If no valid fields were selected, exit function
        if not updates:
            print("No valid fields selected. Returning to menu.")
            return

        # Confirm the updates with the user before making changes
        print("\nChanges to be made:")
        for field, value in updates.items():
            print(f"{field}: {value}")

        confirm = input("\nAre you sure you want to update this owner? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Update canceled.")
            return

        # Construct the SQL UPDATE query dynamically
        set_clause = ", ".join(f"{field} = %s" for field in updates.keys())  # Generate SET clause
        query = f"UPDATE Owner SET {set_clause} WHERE owner_id = %s"

        values = list(updates.values()) + [owner_id]  # List of values to execute query
        cursor.execute(query, values)  # Execute the update query

        print("Owner updated successfully!")

    # Handle input validation errors
    except ValueError as ve:
        print(f"Input validation error: {ve}")

    # Handle database-related errors
    except Error as e:
        print(f"Database error: {e}")

    # Handle any unexpected errors
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Function to delete an owner record
def delete_owner(cursor):
    """
    Delete an owner record by ID with validation, error handling, and user confirmation.

    :param cursor: Database cursor used to execute SQL queries.
    """
    try:
        # Prompt user to enter the Owner ID they want to delete
        owner_id = input("Enter Owner ID to delete: ").strip()

        # Validate that the input is a numeric value (to prevent SQL errors)
        if not owner_id.isdigit():
            print("Invalid owner ID. Please enter a numeric value.")
            return  # Exit the function if the input is invalid

        # Check if the owner exists in the database
        cursor.execute("SELECT * FROM Owner WHERE owner_id = %s", (owner_id,))
        owner_data = cursor.fetchone()

        # If no matching owner is found, exit the function
        if not owner_data:
            print(f"Owner with ID {owner_id} not found.")
            return

        # Display owner details for confirmation before deletion
        print("\nOwner Details:")
        print(f"ID: {owner_data[0]}")
        print(f"First Name: {owner_data[1]}")
        print(f"Last Name: {owner_data[2]}")
        print(f"Email: {owner_data[3]}")
        print(f"Phone: {owner_data[4] or 'N/A'}")  # Show 'N/A' if phone is NULL
        print(f"Mailing Address: {owner_data[5] or 'N/A'}")  # Show 'N/A' if address is NULL

        # Check if the owner has related records in the PropertyOwner table (e.g., associated properties)
        cursor.execute("SELECT COUNT(*) FROM PropertyOwner WHERE owner_id = %s", (owner_id,))
        property_count = cursor.fetchone()[0]

        # Warn the user if the owner has related property ownership records
        if property_count > 0:
            print(
                f"\nWARNING: Deleting this owner will also remove {property_count} associated property ownership record(s)."
            )

        # Ask the user to confirm deletion
        confirm = input("\nAre you sure you want to delete this owner? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Deletion canceled.")
            return  # Exit function if user does not confirm deletion

        # Execute the SQL DELETE query to remove the owner from the database
        query = "DELETE FROM Owner WHERE owner_id = %s"
        cursor.execute(query, (owner_id,))

        # Verify if the deletion was successful
        if cursor.rowcount > 0:
            print(f"Owner with ID {owner_id} deleted successfully!")
        else:
            print(f"No owner found with ID {owner_id}.")  # Shouldn't happen due to earlier validation

    # Handle database-related errors
    except Error as e:
        print(f"Database error: {e}")

    # Handle any unexpected errors
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Tenant Table CRUD Functions

# Function to create a new tenant record in the Tenant table
def create_tenant(cursor):
    """
    Insert a new tenant into the Tenant table with validation and error handling.

    :param cursor: Database cursor used to execute SQL queries.
    """
    try:
        # Prompt user to enter Tenant ID and validate that it is not empty
        tenant_id = input("Enter Tenant ID: ").strip()
        if not tenant_id:
            raise ValueError("Tenant ID is required.")  # Raise error if Tenant ID is empty

        # Prompt user to enter first name and validate that it is not empty
        first_name = input("Enter first name: ").strip()
        if not first_name:
            raise ValueError("First name is required.")  # Raise error if first name is empty

        # Prompt user to enter last name and validate that it is not empty
        last_name = input("Enter last name: ").strip()
        if not last_name:
            raise ValueError("Last name is required.")  # Raise error if last name is empty

        # Prompt user to enter email and validate it using the validate_email function
        email = validate_email(input("Enter email: ").strip())
        if not email:
            raise ValueError("Email is required.")  # Raise error if email is empty or invalid

        # Prompt user to enter phone number (optional) and validate it using the validate_phone function
        phone = input("Enter phone number (optional): ").strip()
        if phone:
            phone = validate_phone(phone)  # Validate phone number if provided

        # Prompt user to enter employer information (optional), allow for empty input
        employer = input("Enter employer (optional): ").strip()
        if not employer:
            employer = None  # Set employer to None if not provided

        # Prompt user to enter emergency contact number (optional) and validate it if provided
        emergency_contact = input("Enter emergency contact number (optional): ").strip()
        if emergency_contact:
            emergency_contact = validate_phone(emergency_contact)  # Validate emergency contact number if provided

        # SQL query to insert the collected data into the Tenant table
        query = """
        INSERT INTO Tenant (tenant_id, first_name, last_name, email, phone, employer, emergency_contact)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (tenant_id, first_name, last_name, email, phone, employer, emergency_contact)  # Tuple of values to insert

        # Execute the SQL query with the provided values
        cursor.execute(query, values)
        print("Tenant added successfully!")  # Confirmation message upon successful insertion

    except ValueError as ve:
        # Handle input validation errors (e.g., missing required fields)
        print(f"Input validation error: {ve}")
    except Error as e:
        # Handle database-related errors (e.g., SQL syntax issues or connection errors)
        print(f"Database error: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")


# Function to read and display all tenants with pagination
def read_tenants(cursor, page_size=10):
    """
    Retrieve and display all tenants in a formatted table with pagination and error handling.

    :param cursor: Database cursor used to execute SQL queries.
    :param page_size: Number of records to display per page (default is 10).
    """
    try:
        # Execute SQL query to fetch all tenants from the Tenant table, ordered by tenant_id
        cursor.execute("SELECT * FROM Tenant ORDER BY tenant_id")
        tenants = cursor.fetchall()  # Fetch all records from the query result

        # Check if there are no tenants in the database
        if not tenants:
            print("\nNo tenants found.")
            return  # Exit if no tenants are found

        # Format tenant records for better display, converting them into a dictionary for each tenant
        formatted_tenants = []
        for tenant in tenants:
            formatted_tenant = {
                "ID": tenant[0],  # Tenant ID
                "First Name": tenant[1],  # Tenant's first name
                "Last Name": tenant[2],  # Tenant's last name
                "Email": tenant[3],  # Tenant's email address
                "Phone": tenant[4] or "N/A",  # Tenant's phone number or "N/A" if not provided
                "Employer": tenant[5] or "N/A",  # Tenant's employer or "N/A" if not provided
                "Emergency Contact": tenant[6] or "N/A"  # Tenant's emergency contact or "N/A" if not provided
            }
            formatted_tenants.append(formatted_tenant)  # Append formatted tenant record to the list

        # Calculate the total number of tenants
        total_tenants = len(formatted_tenants)
        start_index = 0  # Index to keep track of where to start displaying the next page of tenants

        # Pagination logic: display tenants in pages, each page containing 'page_size' tenants
        while start_index < total_tenants:
            print("\nTenant Records:")
            # Display the tenants for the current page using the tabulate library for table formatting
            print(tabulate(formatted_tenants[start_index:start_index + page_size], headers="keys", tablefmt="grid",
                           stralign="left"))
            # Display which range of tenants is being shown
            print(
                f"\nDisplaying {start_index + 1} to {min(start_index + page_size, total_tenants)} of {total_tenants} tenants.")

            # If there are more pages of tenants to display, ask the user if they want to continue
            if start_index + page_size < total_tenants:
                next_page = input("\nPress Enter to view the next page or 'q' to quit: ").strip().lower()
                if next_page == 'q':  # If the user inputs 'q', exit the loop
                    break
            start_index += page_size  # Move to the next page of tenants

    except Error as e:
        # Handle database errors (e.g., SQL errors)
        print(f"\nDatabase error: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"\nAn unexpected error occurred: {e}")


# Function to update a tenant's information based on their ID
def update_tenant(cursor):
    """
    Update a tenant's information based on their ID with validation and error handling.

    :param cursor: Database cursor used to execute SQL queries.
    """
    try:
        # Prompt the user to input the Tenant ID they want to update
        tenant_id = input("Enter the Tenant ID to update: ").strip()

        # Check if the tenant exists in the database
        cursor.execute("SELECT * FROM Tenant WHERE tenant_id = %s", (tenant_id,))
        tenant_data = cursor.fetchone()  # Fetch the tenant's current data

        if not tenant_data:
            print(f"Tenant with ID {tenant_id} not found.")
            return  # Exit if tenant does not exist

        # Display the current tenant details to the user
        print("\nCurrent Tenant Details:")
        print(f"1. First Name: {tenant_data[1]}")
        print(f"2. Last Name: {tenant_data[2]}")
        print(f"3. Email: {tenant_data[3]}")
        print(f"4. Phone: {tenant_data[4] or 'N/A'}")  # Handle null phone values
        print(f"5. Employer: {tenant_data[5] or 'N/A'}")  # Handle null employer values
        print(f"6. Emergency Contact: {tenant_data[6] or 'N/A'}")  # Handle null emergency contact values

        # Map user choices to database field names
        fields = {
            "1": "first_name",
            "2": "last_name",
            "3": "email",
            "4": "phone",
            "5": "employer",
            "6": "emergency_contact"
        }

        updates = {}  # Dictionary to store the fields and their updated values

        # Ask the user which fields they want to update
        print("\nWhich fields would you like to update?")
        print("1. First Name\n2. Last Name\n3. Email\n4. Phone\n5. Employer\n6. Emergency Contact")
        print("Enter multiple numbers separated by commas (e.g., 1,3) or 'all' to update everything.")

        # Get the user's input
        choices = input("Enter your choices: ").strip()

        # If the user chooses "all", select all fields for updating
        if choices.lower() == "all":
            selected_fields = fields.keys()  # Select all fields
        else:
            selected_fields = choices.split(",")  # Split the user's input into a list of choices

        # Iterate through the selected fields to update
        for choice in selected_fields:
            choice = choice.strip()  # Remove any extra spaces from the choice
            if choice in fields:
                # Ask the user to enter the new value for the chosen field
                new_value = input(f"Enter new value for {fields[choice]} (press Enter to skip): ").strip()
                if new_value:  # If the user enters a value (not just pressing Enter)
                    # Validate and convert input based on field type
                    if fields[choice] == "email":
                        new_value = validate_email(new_value)  # Validate email format
                    elif fields[choice] in ["phone", "emergency_contact"]:
                        new_value = validate_phone(new_value)  # Validate phone number format
                    elif fields[choice] in ["first_name", "last_name"] and not new_value:
                        raise ValueError(f"{fields[choice]} cannot be empty.")  # Validate non-empty names

                    updates[fields[choice]] = new_value  # Store the valid updated value
            else:
                print(f"Invalid choice: {choice}. Skipping...")  # Handle invalid choices

        # If no valid fields were selected, exit
        if not updates:
            print("No valid fields selected. Returning to menu.")
            return

        # Confirm the changes with the user before proceeding
        print("\nChanges to be made:")
        for field, value in updates.items():
            print(f"{field}: {value}")

        confirm = input("\nAre you sure you want to update this tenant? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Update canceled.")  # If the user cancels, exit the function
            return

        # Construct the SQL UPDATE query dynamically based on the selected fields
        set_clause = ", ".join(f"{field} = %s" for field in updates.keys())  # Create the SET clause
        query = f"UPDATE Tenant SET {set_clause} WHERE tenant_id = %s"  # Full SQL UPDATE query

        # Prepare the values to be used in the query (update values + tenant_id)
        values = list(updates.values()) + [tenant_id]
        cursor.execute(query, values)  # Execute the SQL UPDATE query

        print("Tenant updated successfully!")  # Notify the user of success

    except ValueError as ve:
        print(f"Input validation error: {ve}")  # Handle input validation errors (e.g., empty field or invalid format)
    except Error as e:
        print(f"Database error: {e}")  # Handle database errors (e.g., query errors)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  # Handle any other unexpected errors


# Function to delete a tenant record by their ID
def delete_tenant(cursor):
    """
    Delete a tenant record by ID with validation, error handling, and user confirmation.

    :param cursor: Database cursor used to execute SQL queries.
    """
    try:
        # Prompt the user to input the Tenant ID to delete
        tenant_id = input("Enter Tenant ID to delete: ").strip()

        # Validate that the tenant ID is a numeric value
        if not tenant_id.isdigit():
            print("Invalid tenant ID. Please enter a numeric value.")  # Notify if invalid
            return  # Exit the function if ID is not a valid integer

        # Check if the tenant exists in the database
        cursor.execute("SELECT * FROM Tenant WHERE tenant_id = %s", (tenant_id,))
        tenant_data = cursor.fetchone()  # Fetch tenant data

        # If tenant data is not found, inform the user and exit
        if not tenant_data:
            print(f"Tenant with ID {tenant_id} not found.")
            return  # Exit the function if tenant does not exist

        # Display the tenant's current details to the user for confirmation
        print("\nTenant Details:")
        print(f"ID: {tenant_data[0]}")
        print(f"First Name: {tenant_data[1]}")
        print(f"Last Name: {tenant_data[2]}")
        print(f"Email: {tenant_data[3]}")
        print(f"Phone: {tenant_data[4] or 'N/A'}")  # Handle missing phone number
        print(f"Employer: {tenant_data[5] or 'N/A'}")  # Handle missing employer
        print(f"Emergency Contact: {tenant_data[6] or 'N/A'}")  # Handle missing emergency contact

        # Check for any related records, like leases, before deletion
        cursor.execute("SELECT COUNT(*) FROM Lease WHERE tenant_id = %s", (tenant_id,))
        lease_count = cursor.fetchone()[0]  # Get the count of related leases

        # If there are related leases, warn the user about potential data loss
        if lease_count > 0:
            print(f"\nWARNING: Deleting this tenant will also remove {lease_count} associated lease record(s).")

        # Ask the user for confirmation before proceeding with the deletion
        confirm = input("\nAre you sure you want to delete this tenant? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Deletion canceled.")  # Exit if user cancels
            return

        # Execute the SQL query to delete the tenant record
        query = "DELETE FROM Tenant WHERE tenant_id = %s"
        cursor.execute(query, (tenant_id,))  # Perform the delete operation

        # Check if any rows were affected (i.e., a tenant was deleted)
        if cursor.rowcount > 0:
            print(f"Tenant with ID {tenant_id} deleted successfully!")  # Notify the user of success
        else:
            print(f"No tenant found with ID {tenant_id}.")  # Inform if no tenant matched the ID

    except Error as e:
        # Handle any database errors and print an error message
        print(f"Database error: {e}")
    except Exception as e:
        # Handle any unexpected errors that may occur
        print(f"An unexpected error occurred: {e}")


def validate_lease_status(status):
    """
    Validate that the lease status is one of the allowed values.

    :param status: The lease status to validate.
    :return: The original lease status if valid.
    :raises ValueError: If the status is not one of the allowed values.
    """
    # Define the allowed lease statuses
    allowed_statuses = ["Active", "Expired", "Terminated"]

    # Check if the provided status is in the allowed statuses list
    if status not in allowed_statuses:
        # If not, raise an error with a message indicating the valid options
        raise ValueError(f"Invalid lease status. Allowed values are: {', '.join(allowed_statuses)}")

    # Return the original status if it's valid
    return status


# Lease Table CRUD Functions

# Create a new Lease record
def create_lease(cursor):
    """
    Insert a new lease into the Lease table with validation and error handling.
    """
    try:
        # Collect user input for lease details
        lease_id = input("Enter Lease ID: ").strip()  # Get the lease ID from the user
        if not lease_id:
            raise ValueError("Lease ID is required.")  # Ensure lease ID is provided

        property_id = input("Enter Property ID: ").strip()  # Get the property ID
        if not property_id:
            raise ValueError("Property ID is required.")  # Ensure property ID is provided

        tenant_id = input("Enter Tenant ID: ").strip()  # Get the tenant ID
        if not tenant_id:
            raise ValueError("Tenant ID is required.")  # Ensure tenant ID is provided

        # Get and validate the start and end dates in YYYY-MM-DD format
        start_date = validate_date(input("Enter start date (YYYY-MM-DD): ").strip())
        end_date = validate_date(input("Enter end date (YYYY-MM-DD): ").strip())

        # Ensure the start date is before the end date
        if start_date >= end_date:
            raise ValueError("Start date must be before the end date.")

        # Get and validate the monthly rent amount, ensure it’s a valid number
        monthly_rent = input("Enter monthly rent amount: ").strip()
        if not monthly_rent.replace(".", "", 1).isdigit():  # Check if input is numeric, allowing one decimal point
            raise ValueError("Monthly rent must be a valid number.")
        monthly_rent = float(monthly_rent)  # Convert the rent to a float

        # Get and validate the security deposit amount (optional)
        security_deposit = input("Enter security deposit amount (or leave blank for none): ").strip()
        if security_deposit:  # If a deposit is provided, validate the value
            if not security_deposit.replace(".", "", 1).isdigit():
                raise ValueError("Security deposit must be a valid number.")
            security_deposit = float(security_deposit)  # Convert the deposit to a float
        else:
            security_deposit = None  # If no deposit is provided, set to None

        # Validate the lease status (Active, Expired, Terminated)
        lease_status = validate_lease_status(input("Enter lease status (Active, Expired, Terminated): ").strip())

        # SQL query to insert the collected data into the Lease table
        query = """
        INSERT INTO Lease (lease_id, property_id, tenant_id, start_date, end_date, monthly_rent, security_deposit, lease_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (lease_id, property_id, tenant_id, start_date, end_date, monthly_rent, security_deposit, lease_status)

        # Execute the query with provided values
        cursor.execute(query, values)  # Insert the new lease record into the database
        print("Lease added successfully!")  # Inform the user of successful insertion

    except ValueError as ve:
        # Handle input validation errors (e.g., incorrect date format, non-numeric rent)
        print(f"Input validation error: {ve}")
    except Error as e:
        # Handle database-related errors (e.g., issues with the query execution)
        print(f"Database error: {e}")
    except Exception as e:
        # Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")


# Read and Display all Lease records
def read_leases(cursor, page_size=10):
    """
    Retrieve and display all leases in a formatted table with pagination and error handling.
    """
    try:
        # Execute query to fetch all leases from the Lease table, ordered by lease_id
        cursor.execute("SELECT * FROM Lease ORDER BY lease_id")
        leases = cursor.fetchall()  # Fetch all lease records from the query

        # If no leases are found, print a message and return
        if not leases:
            print("\nNo leases found.")
            return

        # Format the lease results into a more user-friendly dictionary format for display
        formatted_leases = []
        for lease in leases:
            formatted_lease = {
                "Lease ID": lease[0],  # Lease ID (primary key)
                "Property ID": lease[1],  # Property ID (foreign key)
                "Tenant ID": lease[2],  # Tenant ID (foreign key)
                "Start Date": lease[3].strftime("%Y-%m-%d") if lease[3] else "N/A",  # Format start date if it exists
                "End Date": lease[4].strftime("%Y-%m-%d") if lease[4] else "N/A",  # Format end date if it exists
                "Monthly Rent": f"${lease[5]:,.2f}",  # Format the monthly rent as currency
                "Security Deposit": f"${lease[6]:,.2f}" if lease[6] else "N/A",  # Format the security deposit, if present
                "Status": lease[7]  # Lease status (e.g., Active, Expired, etc.)
            }
            formatted_leases.append(formatted_lease)  # Add the formatted lease data to the list

        # Calculate the total number of leases for pagination
        total_leases = len(formatted_leases)
        start_index = 0  # Initialize the starting index for pagination

        # Pagination: display the leases in chunks (page_size at a time)
        while start_index < total_leases:
            print("\nLease Records:")
            # Display a subset of leases as a table using tabulate
            print(tabulate(formatted_leases[start_index:start_index + page_size], headers="keys", tablefmt="grid", stralign="left"))
            # Display the range of leases being shown and the total number of leases
            print(f"\nDisplaying {start_index + 1} to {min(start_index + page_size, total_leases)} of {total_leases} leases.")

            # If there are more leases, prompt the user to press Enter to see the next page or 'q' to quit
            if start_index + page_size < total_leases:
                next_page = input("\nPress Enter to view the next page or 'q' to quit: ").strip().lower()
                if next_page == 'q':
                    break  # If the user chooses 'q', exit the loop and stop pagination
            start_index += page_size  # Increment the starting index to show the next page of leases

    except Error as e:
        # Handle database-specific errors (e.g., issues executing the query)
        print(f"\nDatabase error: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"\nAn unexpected error occurred: {e}")


# Update a Lease record
def update_lease(cursor):
    """
    Update a lease record based on lease ID with validation and error handling.
    """
    try:
        # Step 1: Get the lease ID to update from the user
        lease_id = input("Enter Lease ID to update: ").strip()

        # Step 2: Check if the lease exists in the database
        cursor.execute("SELECT * FROM Lease WHERE lease_id = %s", (lease_id,))
        lease_data = cursor.fetchone()

        if not lease_data:
            print(f"Lease with ID {lease_id} not found.")
            return

        # Step 3: Display current lease details for the user to review
        print("\nCurrent Lease Details:")
        print(f"1. Property ID: {lease_data[1]}")
        print(f"2. Tenant ID: {lease_data[2]}")
        print(f"3. Start Date: {lease_data[3].strftime('%Y-%m-%d')}")
        print(f"4. End Date: {lease_data[4].strftime('%Y-%m-%d')}")
        print(f"5. Monthly Rent: ${lease_data[5]:,.2f}")
        print(f"6. Security Deposit: ${lease_data[6]:,.2f}" if lease_data[6] else "6. Security Deposit: N/A")
        print(f"7. Lease Status: {lease_data[7]}")

        # Step 4: Create a dictionary to map field numbers to the corresponding column names
        fields = {
            "1": "property_id",
            "2": "tenant_id",
            "3": "start_date",
            "4": "end_date",
            "5": "monthly_rent",
            "6": "security_deposit",
            "7": "lease_status"
        }

        updates = {}  # Dictionary to store fields and new values that need to be updated

        # Step 5: Prompt the user for which fields they want to update
        print("\nWhich fields would you like to update?")
        print(
            "1. Property ID\n2. Tenant ID\n3. Start Date\n4. End Date\n5. Monthly Rent\n6. Security Deposit\n7. Lease Status")
        print("Enter multiple numbers separated by commas (e.g., 1,3) or 'all' to update everything.")

        # Step 6: Get user input for fields to update
        choices = input("Enter your choices: ").strip()

        # Step 7: If user selects 'all', select all fields, otherwise, split input into individual choices
        if choices.lower() == "all":
            selected_fields = fields.keys()  # Select all fields to update
        else:
            selected_fields = choices.split(",")  # Split input by commas to update selected fields

        # Step 8: Loop through the selected fields to get new values from the user
        for choice in selected_fields:
            choice = choice.strip()  # Remove any extra spaces around input
            if choice in fields:  # Ensure the choice is valid
                # Get the new value for the selected field
                new_value = input(f"Enter new value for {fields[choice]} (press Enter to skip): ").strip()
                if new_value:  # If the user enters a new value (skips if empty)
                    # Validate and process the input based on the field type
                    if fields[choice] in ["start_date", "end_date"]:
                        new_value = validate_date(new_value)  # Validate date format
                    elif fields[choice] in ["monthly_rent", "security_deposit"]:
                        # Ensure that rent or deposit is a valid number
                        if not new_value.replace(".", "", 1).isdigit():
                            raise ValueError(f"{fields[choice]} must be a valid number.")
                        new_value = float(new_value)  # Convert to a float
                    elif fields[choice] == "lease_status":
                        new_value = validate_lease_status(new_value)  # Validate lease status
                    elif fields[choice] in ["property_id", "tenant_id"] and not new_value:
                        # Ensure Property ID or Tenant ID is not empty
                        raise ValueError(f"{fields[choice]} cannot be empty.")

                    # Store the new value for the field in the updates dictionary
                    updates[fields[choice]] = new_value
            else:
                print(f"Invalid choice: {choice}. Skipping...")  # Handle invalid choices

        # Step 9: If no valid fields were selected, return to menu
        if not updates:
            print("No valid fields selected. Returning to menu.")
            return

        # Step 10: Confirm changes with the user before applying them
        print("\nChanges to be made:")
        for field, value in updates.items():
            print(f"{field}: {value}")

        confirm = input("\nAre you sure you want to update this lease? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Update canceled.")
            return

        # Step 11: Construct the SQL UPDATE query dynamically based on the selected fields
        set_clause = ", ".join(f"{field} = %s" for field in updates.keys())  # Create SET clause
        query = f"UPDATE Lease SET {set_clause} WHERE lease_id = %s"  # Complete SQL query

        values = list(updates.values()) + [lease_id]  # Prepare values for query execution (include lease_id)
        cursor.execute(query, values)  # Execute the SQL query to update the lease

        # Step 12: Notify the user that the lease was successfully updated
        print("Lease updated successfully!")

    except ValueError as ve:
        # Handle validation errors (e.g., invalid input)
        print(f"Input validation error: {ve}")
    except Error as e:
        # Handle database-related errors
        print(f"Database error: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")


# Delete a Lease record
def delete_lease(cursor):
    """
    Delete a lease record by ID with validation, error handling, and user confirmation.
    """
    try:
        # Step 1: Get the lease ID from the user
        lease_id = input("Enter Lease ID to delete: ").strip()

        # Step 2: Validate that the lease ID is a numeric value (i.e., an integer)
        if not lease_id.isdigit():
            print("Invalid lease ID. Please enter a numeric value.")
            return  # Exit the function if the input is invalid

        # Step 3: Check if the lease exists in the database by querying with the lease ID
        cursor.execute("SELECT * FROM Lease WHERE lease_id = %s", (lease_id,))
        lease_data = cursor.fetchone()  # Fetch the lease data (if exists)

        if not lease_data:
            print(f"Lease with ID {lease_id} not found.")  # Notify user if lease does not exist
            return

        # Step 4: Display the lease details for user confirmation before deletion
        print("\nLease Details:")
        print(f"ID: {lease_data[0]}")
        print(f"Property ID: {lease_data[1]}")
        print(f"Tenant ID: {lease_data[2]}")
        print(f"Start Date: {lease_data[3].strftime('%Y-%m-%d')}")
        print(f"End Date: {lease_data[4].strftime('%Y-%m-%d')}")
        print(f"Monthly Rent: ${lease_data[5]:,.2f}")
        print(f"Security Deposit: ${lease_data[6]:,.2f}" if lease_data[6] else "Security Deposit: N/A")
        print(f"Status: {lease_data[7]}")

        # Step 5: Check for any related records (e.g., payments) that might be affected by the deletion
        cursor.execute("SELECT COUNT(*) FROM Payment WHERE lease_id = %s", (lease_id,))
        payment_count = cursor.fetchone()[0]  # Get the number of related payment records

        if payment_count > 0:
            print(f"\nWARNING: Deleting this lease will also remove {payment_count} associated payment record(s).")

        # Step 6: Confirm deletion with the user
        confirm = input("\nAre you sure you want to delete this lease? (yes/no): ").strip().lower()
        if confirm != "yes":  # If user does not confirm, cancel the deletion
            print("Deletion canceled.")
            return

        # Step 7: Execute the DELETE SQL query to remove the lease record from the database
        query = "DELETE FROM Lease WHERE lease_id = %s"
        cursor.execute(query, (lease_id,))  # Execute the query with the lease ID

        # Step 8: Check if the deletion was successful (i.e., if any rows were affected)
        if cursor.rowcount > 0:
            print(f"Lease with ID {lease_id} deleted successfully!")  # Confirm deletion
        else:
            print(f"No lease found with ID {lease_id}.")  # If no rows were affected, notify the user

    except Error as e:
        # Step 9: Handle database-related errors (e.g., connection or query issues)
        print(f"Database error: {e}")
    except Exception as e:
        # Step 10: Handle any unexpected errors that occur during execution
        print(f"An unexpected error occurred: {e}")


# MaintenanceRequest Table CRUD Functions

# Function to validate the status of the maintenance request
def validate_status(status):
    """Validate that the status is one of the allowed values."""
    # Define allowed status options for the maintenance request
    allowed_statuses = ["Open", "In Progress", "Completed"]

    # If the provided status is not in the allowed list, raise an error
    if status not in allowed_statuses:
        raise ValueError(f"Invalid status. Allowed values are: {', '.join(allowed_statuses)}")

    # Return the valid status
    return status


# Function to create a new maintenance request record in the database
def create_maintenance_request(cursor):
    """
    Insert a new maintenance request into the MaintenanceRequest table with validation and error handling.
    """
    try:
        # Step 1: Collect user input for maintenance request details
        # Prompt user for the request ID and validate input
        request_id = input("Enter Request ID: ").strip()
        if not request_id:
            raise ValueError("Request ID is required.")

        # Prompt user for the property ID and validate input
        property_id = input("Enter Property ID: ").strip()
        if not property_id:
            raise ValueError("Property ID is required.")

        # Prompt user for the tenant ID and validate input
        tenant_id = input("Enter Tenant ID: ").strip()
        if not tenant_id:
            raise ValueError("Tenant ID is required.")

        # Prompt user for the employee ID (or allow for unassigned)
        employee_id = input("Enter Employee ID (or leave blank if unassigned): ").strip()
        if employee_id == "":
            employee_id = None  # If left blank, set employee_id to None (unassigned)

        # Prompt user for a description of the maintenance request
        description = input("Enter maintenance request description: ").strip()
        if not description:
            raise ValueError("Description is required.")

        # Step 2: Collect and validate request date
        # Prompt for request date or default to None (Current date will be used in the database if left blank)
        request_date = input("Enter request date (YYYY-MM-DD) or press Enter for today: ").strip()
        if request_date:
            request_date = validate_date(request_date)  # Validate date format if provided
        else:
            request_date = None  # Set to None (which will use CURRENT_DATE in SQL)

        # Step 3: Collect and validate completion date (if applicable)
        # Prompt for completion date if the request is completed, otherwise leave it blank
        completion_date = input("Enter completion date (YYYY-MM-DD) or leave blank if not completed: ").strip()
        if completion_date:
            completion_date = validate_date(completion_date)  # Validate completion date format
            if request_date and completion_date < request_date:
                # Ensure that the completion date is not earlier than the request date
                raise ValueError("Completion date must be on or after the request date.")
        else:
            completion_date = None  # If not completed, leave as None

        # Step 4: Collect and validate the status of the maintenance request
        status = validate_status(input("Enter request status (Open, In Progress, Completed): ").strip())

        # Step 5: Construct SQL query to insert the collected data into the MaintenanceRequest table
        query = """
        INSERT INTO MaintenanceRequest (request_id, property_id, tenant_id, employee_id, description, request_date, completion_date, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        # The values to be inserted into the SQL query (prepared statement)
        values = (request_id, property_id, tenant_id, employee_id, description, request_date, completion_date, status)

        # Step 6: Execute the SQL query with the provided values
        cursor.execute(query, values)

        # Step 7: Print a success message after the maintenance request has been added
        print("Maintenance request added successfully!")

    except ValueError as ve:
        # Handle input validation errors
        print(f"Input validation error: {ve}")
    except Error as e:
        # Handle any database-related errors (e.g., connection or query issues)
        print(f"Database error: {e}")
    except Exception as e:
        # Handle any unexpected errors during the execution of the function
        print(f"An unexpected error occurred: {e}")


# Read and Display all maintenance requests
def read_maintenance_requests(cursor, page_size=10):
    """
    Retrieve and display all maintenance requests in a formatted table with pagination and error handling.
    """
    try:
        # Step 1: Execute query to fetch all maintenance requests from the database
        cursor.execute("SELECT * FROM MaintenanceRequest ORDER BY request_id")
        requests = cursor.fetchall()

        # If no maintenance requests are found, print a message and return
        if not requests:
            print("\nNo maintenance requests found.")
            return

        # Step 2: Format the fetched data into dictionaries for better display
        formatted_requests = []
        for req in requests:
            # Format each request into a dictionary with clear keys for easy reading
            formatted_request = {
                "Request ID": req[0],
                "Property ID": req[1],
                "Tenant ID": req[2],
                "Employee ID": req[3] or "Unassigned",  # If employee_id is None, display "Unassigned"
                "Description": req[4],
                "Request Date": req[5].strftime("%Y-%m-%d") if req[5] else "N/A",  # Format date or show "N/A"
                "Completion Date": req[6].strftime("%Y-%m-%d") if req[6] else "Pending",  # Show "Pending" if no completion date
                "Status": req[7]
            }
            # Append the formatted request to the list
            formatted_requests.append(formatted_request)

        # Step 3: Paginate the results for better user experience
        total_requests = len(formatted_requests)  # Total number of requests retrieved
        start_index = 0  # Start with the first page of results

        # Display results with pagination
        while start_index < total_requests:
            print("\nMaintenance Requests:")
            # Print the current page of results in a formatted table
            print(tabulate(formatted_requests[start_index:start_index + page_size], headers="keys", tablefmt="grid", stralign="left"))
            print(f"\nDisplaying {start_index + 1} to {min(start_index + page_size, total_requests)} of {total_requests} requests.")

            # Check if there are more requests to display
            if start_index + page_size < total_requests:
                # Ask the user if they want to view the next page or quit
                next_page = input("\nPress Enter to view the next page or 'q' to quit: ").strip().lower()
                if next_page == 'q':
                    break  # Exit the loop if the user presses 'q'
            start_index += page_size  # Move to the next page of results

    except Error as e:
        # Handle any database-related errors (e.g., query issues or connection problems)
        print(f"\nDatabase error: {e}")
    except Exception as e:
        # Handle any unexpected errors
        print(f"\nAn unexpected error occurred: {e}")


# Update a maintenance request
def update_maintenance_request(cursor):
    """
    Update a maintenance request based on request ID with validation and error handling.
    """
    try:
        # Step 1: Get the request ID to update from the user
        request_id = input("Enter Request ID to update: ").strip()

        # Step 2: Check if the maintenance request exists in the database
        cursor.execute("SELECT * FROM MaintenanceRequest WHERE request_id = %s", (request_id,))
        request_data = cursor.fetchone()

        # If the request doesn't exist, notify the user and return
        if not request_data:
            print(f"Maintenance request with ID {request_id} not found.")
            return

        # Step 3: Display the current maintenance request details to the user
        print("\nCurrent Maintenance Request Details:")
        print(f"1. Property ID: {request_data[1]}")
        print(f"2. Tenant ID: {request_data[2]}")
        print(f"3. Employee ID: {request_data[3] or 'Unassigned'}")
        print(f"4. Description: {request_data[4]}")
        print(f"5. Request Date: {request_data[5].strftime('%Y-%m-%d') if request_data[5] else 'N/A'}")
        print(f"6. Completion Date: {request_data[6].strftime('%Y-%m-%d') if request_data[6] else 'Pending'}")
        print(f"7. Status: {request_data[7]}")

        # Step 4: Create a dictionary mapping option numbers to column names for easy reference
        fields = {
            "1": "property_id",
            "2": "tenant_id",
            "3": "employee_id",
            "4": "description",
            "5": "request_date",
            "6": "completion_date",
            "7": "status"
        }

        updates = {}  # Dictionary to store updated fields and their new values

        # Step 5: Ask the user which fields they would like to update
        print("\nWhich fields would you like to update?")
        print(
            "1. Property ID\n2. Tenant ID\n3. Employee ID\n4. Description\n5. Request Date\n6. Completion Date\n7. Status")
        print("Enter multiple numbers separated by commas (e.g., 1,3) or 'all' to update everything.")

        choices = input("Enter your choices: ").strip()  # Get user input for choices

        # Step 6: Determine which fields to update based on user input
        if choices.lower() == "all":
            selected_fields = fields.keys()  # Select all fields if "all" is entered
        else:
            selected_fields = choices.split(",")  # Convert input into a list of selected fields

        # Step 7: Loop through the selected fields and gather new values
        for choice in selected_fields:
            choice = choice.strip()  # Remove any spaces around the choice
            if choice in fields:
                # Prompt the user for a new value for the selected field
                new_value = input(f"Enter new value for {fields[choice]} (press Enter to skip): ").strip()
                if new_value:  # Only update if the user provided a new value
                    # Validate and convert the input based on the field type
                    if fields[choice] in ["request_date", "completion_date"]:
                        new_value = validate_date(new_value)  # Validate date fields
                        if fields[choice] == "completion_date" and "request_date" in updates:
                            # Ensure that the completion date is not before the request date
                            if new_value < updates["request_date"]:
                                raise ValueError("Completion date must be on or after the request date.")
                    elif fields[choice] == "status":
                        new_value = validate_status(new_value)  # Validate the status field
                    elif fields[choice] in ["property_id", "tenant_id", "employee_id"] and not new_value:
                        # Ensure that property_id, tenant_id, and employee_id are not empty
                        raise ValueError(f"{fields[choice]} cannot be empty.")

                    # Store the updated value in the updates dictionary
                    updates[fields[choice]] = new_value
            else:
                # If an invalid choice was made, print a message and skip it
                print(f"Invalid choice: {choice}. Skipping...")

        # Step 8: Check if any valid fields were selected for update
        if not updates:
            print("No valid fields selected. Returning to menu.")
            return

        # Step 9: Display the changes to be made and confirm with the user
        print("\nChanges to be made:")
        for field, value in updates.items():
            print(f"{field}: {value}")

        # Confirm if the user wants to proceed with the update
        confirm = input("\nAre you sure you want to update this maintenance request? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Update canceled.")
            return

        # Step 10: Construct the SQL UPDATE query dynamically
        # Create the SET clause for the SQL query
        set_clause = ", ".join(f"{field} = %s" for field in updates.keys())
        query = f"UPDATE MaintenanceRequest SET {set_clause} WHERE request_id = %s"

        # Prepare the values for query execution: values from updates and the request_id
        values = list(updates.values()) + [request_id]
        cursor.execute(query, values)  # Execute the update query

        # Step 11: Print a success message after the update
        print("Maintenance request updated successfully!")

    except ValueError as ve:
        # Handle validation errors (e.g., invalid date, empty fields)
        print(f"Input validation error: {ve}")
    except Error as e:
        # Handle database errors (e.g., query issues, connection problems)
        print(f"Database error: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")


# Delete a Maintenance Request
def delete_maintenance_request(cursor):
    """
    Delete a maintenance request by ID with validation, error handling, and user confirmation.
    """
    try:
        # Step 1: Get the request ID to delete from the user
        request_id = input("Enter Request ID to delete: ").strip()

        # Step 2: Validate that the request ID is a valid integer
        # If the ID is not numeric, print an error and return
        if not request_id.isdigit():
            print("Invalid request ID. Please enter a numeric value.")
            return

        # Step 3: Check if the maintenance request exists in the database
        cursor.execute("SELECT * FROM MaintenanceRequest WHERE request_id = %s", (request_id,))
        request_data = cursor.fetchone()

        # If the request doesn't exist, notify the user and exit
        if not request_data:
            print(f"Maintenance request with ID {request_id} not found.")
            return

        # Step 4: Display the details of the maintenance request for confirmation
        print("\nMaintenance Request Details:")
        print(f"ID: {request_data[0]}")
        print(f"Property ID: {request_data[1]}")
        print(f"Tenant ID: {request_data[2]}")
        print(f"Employee ID: {request_data[3] or 'Unassigned'}")
        print(f"Description: {request_data[4]}")
        print(f"Request Date: {request_data[5].strftime('%Y-%m-%d') if request_data[5] else 'N/A'}")
        print(f"Completion Date: {request_data[6].strftime('%Y-%m-%d') if request_data[6] else 'Pending'}")
        print(f"Status: {request_data[7]}")

        # Step 5: Ask for user confirmation to delete the maintenance request
        confirm = input("\nAre you sure you want to delete this maintenance request? (yes/no): ").strip().lower()

        # If the user does not confirm, cancel the deletion
        if confirm != "yes":
            print("Deletion canceled.")
            return

        # Step 6: Execute the DELETE SQL query to remove the request from the database
        query = "DELETE FROM MaintenanceRequest WHERE request_id = %s"
        cursor.execute(query, (request_id,))

        # Step 7: Check if the deletion was successful
        if cursor.rowcount > 0:
            # If a row was deleted, notify the user of success
            print(f"Maintenance request with ID {request_id} deleted successfully!")
        else:
            # If no rows were deleted, notify the user that the request was not found
            print(f"No maintenance request found with ID {request_id}.")

    except Error as e:
        # Step 8: Handle any database-related errors
        print(f"Database error: {e}")
    except Exception as e:
        # Step 9: Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")


# Payment Table CRUD Functions
def validate_payment_method(method):
    """
    Validate that the payment method is one of the allowed values.
    Ensures that the entered payment method is valid.
    """
    allowed_methods = ["Credit Card", "Check", "Bank Transfer", "Cash"]

    # Check if the provided method is in the allowed methods list
    if method not in allowed_methods:
        raise ValueError(f"Invalid payment method. Allowed values are: {', '.join(allowed_methods)}")

    # Return the validated method if it's valid
    return method


# Create a new Payment
def create_payment(cursor):
    """
    Insert a new payment into the Payment table with validation and error handling.
    This function collects payment details from the user and inserts them into the database.
    """
    try:
        # Step 1: Collect user input for payment details
        payment_id = input("Enter Payment ID: ").strip()
        # Ensure the Payment ID is provided
        if not payment_id:
            raise ValueError("Payment ID is required.")

        lease_id = input("Enter Lease ID: ").strip()
        # Ensure the Lease ID is provided
        if not lease_id:
            raise ValueError("Lease ID is required.")

        tenant_id = input("Enter Tenant ID: ").strip()
        # Ensure the Tenant ID is provided
        if not tenant_id:
            raise ValueError("Tenant ID is required.")

        # Step 2: Collect and validate the payment amount
        amount = input("Enter Payment Amount: ").strip()
        # Check if the amount is a valid number
        if not amount.replace(".", "", 1).isdigit():
            raise ValueError("Payment amount must be a valid number.")
        amount = float(amount)  # Convert the string to a float

        # Step 3: Collect and validate the payment date
        payment_date = validate_date(input("Enter Payment Date (YYYY-MM-DD): ").strip())

        # Step 4: Show available payment methods and validate input
        print("Available Payment Methods: Credit Card, Check, Bank Transfer, Cash")
        payment_method = validate_payment_method(input("Enter Payment Method: ").strip())

        # Step 5: Collect Employee ID who received the payment (optional)
        received_by = input("Enter Employee ID who received the payment (or leave blank if unknown): ").strip()
        if received_by == "":
            received_by = None  # If left blank, set as None (unknown)

        # Step 6: Prepare the SQL query to insert the collected data into the Payment table
        query = """
        INSERT INTO Payment (payment_id, lease_id, tenant_id, amount, payment_date, payment_method, received_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        # Values to insert in the SQL query
        values = (payment_id, lease_id, tenant_id, amount, payment_date, payment_method, received_by)

        # Step 7: Execute the SQL query with the provided values
        cursor.execute(query, values)

        # Step 8: Notify the user that the payment record was added successfully
        print("Payment record added successfully!")

    except ValueError as ve:
        # Handle specific input validation errors (e.g., invalid amount or missing fields)
        print(f"Input validation error: {ve}")
    except Error as e:
        # Handle database-related errors (e.g., query issues)
        print(f"Database error: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")


# Read and Display all payments
def read_payments(cursor, page_size=10):
    """
    Retrieve and display all payments in a formatted table with pagination and error handling.
    This function fetches all payments from the database, formats the results for display,
    and paginates the output for easy viewing.
    """
    try:
        # Step 1: Execute a query to fetch all payments from the database, ordered by payment ID
        cursor.execute("SELECT * FROM Payment ORDER BY payment_id")
        payments = cursor.fetchall()

        # Step 2: Check if any payments were returned
        if not payments:
            print("\nNo payments found.")  # Inform the user if no payments exist
            return

        # Step 3: Format the fetched results into dictionaries for better display
        formatted_payments = []
        for pay in payments:
            # Create a dictionary for each payment with more user-friendly field names
            formatted_payment = {
                "Payment ID": pay[0],  # Payment ID
                "Lease ID": pay[1],  # Lease ID associated with the payment
                "Tenant ID": pay[2],  # Tenant ID who made the payment
                "Amount": f"${pay[3]:.2f}",  # Format the amount as currency (2 decimal places)
                "Payment Date": pay[4].strftime("%Y-%m-%d") if pay[4] else "N/A",
                # Format date, or show 'N/A' if not available
                "Method": pay[5],  # Payment method (e.g., Credit Card, Cash, etc.)
                "Received By": pay[6] or "Unknown"  # If 'received_by' is None, display 'Unknown'
            }
            formatted_payments.append(formatted_payment)

        # Step 4: Paginate the display of payments for better usability
        total_payments = len(formatted_payments)  # Total number of payments
        start_index = 0  # Starting index for pagination

        # Step 5: Display payments in pages
        while start_index < total_payments:
            # Display the current page of payments in a table format
            print("\nPayments:")
            print(tabulate(formatted_payments[start_index:start_index + page_size], headers="keys", tablefmt="grid",
                           stralign="left"))

            # Display a summary of the current page (range of payments being shown and total count)
            print(
                f"\nDisplaying {start_index + 1} to {min(start_index + page_size, total_payments)} of {total_payments} payments.")

            # Step 6: Prompt the user to view the next page or quit
            if start_index + page_size < total_payments:
                next_page = input("\nPress Enter to view the next page or 'q' to quit: ").strip().lower()
                if next_page == 'q':
                    break  # If the user chooses to quit, break out of the loop
            start_index += page_size  # Move to the next page

    except Error as e:
        # Handle any database-related errors (e.g., SQL query issues)
        print(f"\nDatabase error: {e}")
    except Exception as e:
        # Handle any other unexpected errors that may arise
        print(f"\nAn unexpected error occurred: {e}")


# Update a Payment record
def update_payment(cursor):
    """
    Update payment details based on payment ID with validation and error handling.
    This function allows the user to update payment details by specifying the payment ID.
    It includes validation for user input and updates the database with the new values.
    """
    try:
        # Step 1: Get the payment ID to update from the user
        payment_id = input("Enter Payment ID to update: ").strip()

        # Step 2: Check if the payment with the given ID exists in the database
        cursor.execute("SELECT * FROM Payment WHERE payment_id = %s", (payment_id,))
        payment_data = cursor.fetchone()

        # If no matching payment is found, inform the user and return
        if not payment_data:
            print(f"Payment with ID {payment_id} not found.")
            return

        # Step 3: Display current payment details to the user for reference
        print("\nCurrent Payment Details:")
        print(f"1. Lease ID: {payment_data[1]}")
        print(f"2. Tenant ID: {payment_data[2]}")
        print(f"3. Amount: ${payment_data[3]:.2f}")
        print(f"4. Payment Date: {payment_data[4].strftime('%Y-%m-%d') if payment_data[4] else 'N/A'}")
        print(f"5. Payment Method: {payment_data[5]}")
        print(f"6. Received By: {payment_data[6] or 'Unknown'}")

        # Step 4: Define a dictionary to map user choices to actual column names in the database
        fields = {
            "1": "lease_id",
            "2": "tenant_id",
            "3": "amount",
            "4": "payment_date",
            "5": "payment_method",
            "6": "received_by"
        }

        updates = {}  # Dictionary to store the fields the user wants to update and their new values

        # Step 5: Ask the user which fields they would like to update
        print("\nWhich fields would you like to update?")
        print("1. Lease ID\n2. Tenant ID\n3. Amount\n4. Payment Date\n5. Payment Method\n6. Received By")
        print("Enter multiple numbers separated by commas (e.g., 1,3) or 'all' to update everything.")

        # Get the user's choices
        choices = input("Enter your choices: ").strip()

        # Step 6: Determine which fields the user wants to update
        if choices.lower() == "all":
            selected_fields = fields.keys()  # Select all fields if 'all' is entered
        else:
            selected_fields = choices.split(",")  # Split input into a list of selected fields

        # Step 7: For each selected field, get the new value from the user
        for choice in selected_fields:
            choice = choice.strip()  # Remove any surrounding spaces
            if choice in fields:
                # Ask the user for a new value for the selected field
                new_value = input(f"Enter new value for {fields[choice]} (press Enter to skip): ").strip()
                if new_value:  # Only proceed if the user provided a value (skipping if Enter is pressed)
                    # Step 8: Validate and convert input based on the type of the field
                    if fields[choice] == "payment_date":
                        new_value = validate_date(new_value)  # Validate date input
                    elif fields[choice] == "amount":
                        # Check if the amount is a valid number
                        if not new_value.replace(".", "", 1).isdigit():
                            raise ValueError("Amount must be a valid number.")
                        new_value = float(new_value)  # Convert to float
                    elif fields[choice] == "payment_method":
                        # Validate payment method
                        new_value = validate_payment_method(new_value)
                    elif fields[choice] in ["lease_id", "tenant_id"] and not new_value:
                        # Ensure lease_id and tenant_id are not empty
                        raise ValueError(f"{fields[choice]} cannot be empty.")

                    # Store the new value in the updates dictionary
                    updates[fields[choice]] = new_value
            else:
                # If the user entered an invalid choice, notify them
                print(f"Invalid choice: {choice}. Skipping...")

        # Step 9: If no valid fields were selected, inform the user and return
        if not updates:
            print("No valid fields selected. Returning to menu.")
            return

        # Step 10: Confirm the changes with the user
        print("\nChanges to be made:")
        for field, value in updates.items():
            print(f"{field}: {value}")

        # Ask the user to confirm the update
        confirm = input("\nAre you sure you want to update this payment record? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Update canceled.")
            return

        # Step 11: Construct the SQL UPDATE query dynamically based on the fields to be updated
        set_clause = ", ".join(f"{field} = %s" for field in updates.keys())  # Create the SET clause of the query
        query = f"UPDATE Payment SET {set_clause} WHERE payment_id = %s"  # Complete the query

        # Prepare the values for query execution
        values = list(updates.values()) + [payment_id]  # Add payment_id as the last value for WHERE clause
        cursor.execute(query, values)  # Execute the update query

        # Step 12: Inform the user that the update was successful
        print("Payment record updated successfully!")

    except ValueError as ve:
        # Handle input validation errors (e.g., invalid amount or date)
        print(f"Input validation error: {ve}")
    except Error as e:
        # Handle database-related errors (e.g., issues executing the query)
        print(f"Database error: {e}")
    except Exception as e:
        # Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")


# Delete a Payment record
def delete_payment(cursor):
    """
    Delete a payment record by ID with validation, error handling, and user confirmation.
    This function allows the user to delete a payment record based on its ID. It includes input validation,
    checks for the existence of the payment record, and prompts for user confirmation before performing the deletion.
    """
    try:
        # Step 1: Get the payment ID to delete from the user
        payment_id = input("Enter Payment ID to delete: ").strip()

        # Step 2: Validate that the payment ID entered is a valid integer
        if not payment_id.isdigit():
            print("Invalid payment ID. Please enter a numeric value.")
            return  # If the ID is invalid, exit the function

        # Step 3: Check if the payment record exists in the database
        cursor.execute("SELECT * FROM Payment WHERE payment_id = %s", (payment_id,))
        payment_data = cursor.fetchone()  # Fetch the payment record from the database

        # If the payment does not exist, inform the user and exit the function
        if not payment_data:
            print(f"Payment with ID {payment_id} not found.")
            return

        # Step 4: Display the payment details for confirmation
        print("\nPayment Details:")
        print(f"ID: {payment_data[0]}")
        print(f"Lease ID: {payment_data[1]}")
        print(f"Amount: ${payment_data[2]:.2f}")  # Format amount as currency
        print(f"Payment Date: {payment_data[3].strftime('%Y-%m-%d') if payment_data[3] else 'N/A'}")
        print(f"Payment Method: {payment_data[4]}")
        print(f"Received By: {payment_data[5] or 'Unknown'}")

        # Step 5: Ask for user confirmation before proceeding with the deletion
        confirm = input("\nAre you sure you want to delete this payment record? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Deletion canceled.")  # If the user doesn't confirm, exit the function
            return

        # Step 6: Execute the SQL DELETE query to remove the payment record from the database
        query = "DELETE FROM Payment WHERE payment_id = %s"
        cursor.execute(query, (payment_id,))

        # Step 7: Check if the deletion was successful
        if cursor.rowcount > 0:
            print(f"Payment with ID {payment_id} deleted successfully!")  # Notify user of successful deletion
        else:
            print(f"No payment found with ID {payment_id}.")  # If no record was deleted, inform the user

    except mysql.connector.Error as e:
        # Step 8: Handle MySQL database errors
        if e.errno == 1451:  # Specific error code for foreign key constraint violation
            print("Cannot delete payment record due to related records in other tables.")
        else:
            # For other database-related errors, print the error message
            print(f"Database error: {e}")
    except Exception as e:
        # Step 9: Handle unexpected errors (non-database related)
        print(f"An unexpected error occurred: {e}")


# Employee Table CRUD Functions
def validate_role(role):
    """Validate that the role is one of the allowed values."""
    # Define allowed roles for an employee
    allowed_roles = ["Property Manager", "Maintenance Staff", "Accountant", "Leasing Agent"]

    # Check if the provided role is valid
    if role not in allowed_roles:
        raise ValueError(f"Invalid role. Allowed values are: {', '.join(allowed_roles)}")

    return role  # Return the validated role


# Create a new employee record
def create_employee(cursor):
    """
    Insert a new employee into the Employee table with validation and error handling.
    This function collects details about an employee, validates the data, and inserts a new record into the Employee table.
    """
    try:
        # Step 1: Collect user input for employee details
        employee_id = input("Enter Employee ID: ").strip()

        # Validate that the employee ID is a numeric value
        if not employee_id.isdigit():
            raise ValueError("Employee ID must be a numeric value.")

        # Step 2: Check if the employee ID already exists in the database
        cursor.execute("SELECT * FROM Employee WHERE employee_id = %s", (employee_id,))
        if cursor.fetchone():
            raise ValueError(f"Employee with ID {employee_id} already exists.")  # If exists, raise error

        # Step 3: Collect and validate first name
        first_name = input("Enter First Name: ").strip()
        if not first_name:
            raise ValueError("First name is required.")  # First name cannot be empty

        # Step 4: Collect and validate last name
        last_name = input("Enter Last Name: ").strip()
        if not last_name:
            raise ValueError("Last name is required.")  # Last name cannot be empty

        # Step 5: Validate email format
        email = validate_email(input("Enter Email: ").strip())  # Use a function to validate email format

        # Step 6: Validate phone number format
        phone = validate_phone(input("Enter Phone Number: ").strip())  # Use a function to validate phone number format

        # Step 7: Collect and validate role
        print("Available Roles: Property Manager, Maintenance Staff, Accountant, Leasing Agent")
        role = validate_role(input("Enter Role: ").strip())  # Validate the role using the validate_role function

        # Step 8: Validate hire date format
        hire_date = validate_date(
            input("Enter Hire Date (YYYY-MM-DD): ").strip())  # Use a function to validate date format

        # Step 9: SQL query to insert the collected data into the Employee table
        query = """
        INSERT INTO Employee (employee_id, first_name, last_name, email, phone, role, hire_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        # Prepare the values to be inserted into the database
        values = (employee_id, first_name, last_name, email, phone, role, hire_date)

        # Step 10: Execute the SQL query with the provided values
        cursor.execute(query, values)

        # Success message upon successful insertion
        print("Employee record added successfully!")

    except ValueError as ve:
        # Handle validation errors (e.g., invalid input or already existing employee)
        print(f"Input validation error: {ve}")
    except mysql.connector.Error as e:
        # Handle database-related errors (e.g., duplicate entries)
        if e.errno == 1062:  # Error code for duplicate entry
            print(f"Error: Employee with ID {employee_id} or email {email} already exists.")
        else:
            # General database error
            print(f"Database error: {e}")
    except Exception as e:
        # Catch any unexpected errors
        print(f"An unexpected error occurred: {e}")


# Read and Display all Employee records
def read_employees(cursor, page_size=10):
    """
    Retrieve and display all employees from the database in a paginated and formatted table.
    This function fetches employee records, formats the data for easy display, and handles pagination.
    """
    try:
        # Step 1: Execute SQL query to fetch all employees ordered by employee ID
        cursor.execute("SELECT * FROM Employee ORDER BY employee_id")
        employees = cursor.fetchall()

        # Step 2: Check if there are any employees in the database
        if not employees:
            print("\nNo employees found.")
            return  # Return if no employee records exist

        # Step 3: Format the fetched employee data for better display
        formatted_employees = []
        for emp in employees:
            formatted_emp = {
                "ID": emp[0],  # Employee ID
                "First Name": emp[1],  # Employee's first name
                "Last Name": emp[2],  # Employee's last name
                "Email": emp[3],  # Employee's email address
                "Phone": emp[4] or "N/A",  # If phone is empty, display "N/A"
                "Role": emp[5],  # Employee's role/position
                "Hire Date": emp[6].strftime("%Y-%m-%d") if emp[6] else "N/A"  # Format the hire date if present, otherwise "N/A"
            }
            formatted_employees.append(formatted_emp)  # Add formatted employee to the list

        # Step 4: Paginate the results for easier viewing
        total_employees = len(formatted_employees)  # Total number of employee records
        start_index = 0  # Initialize the starting index for pagination

        # Step 5: Loop to display employees in pages
        while start_index < total_employees:
            print("\nEmployee Records:")
            # Display the current page of employee records in a formatted table
            print(tabulate(formatted_employees[start_index:start_index + page_size], headers="keys", tablefmt="grid", stralign="left"))
            print(f"\nDisplaying {start_index + 1} to {min(start_index + page_size, total_employees)} of {total_employees} employees.")

            # Step 6: Check if there are more employees to display
            if start_index + page_size < total_employees:
                # Ask user if they want to view the next page
                next_page = input("\nPress Enter to view the next page or 'q' to quit: ").strip().lower()
                if next_page == 'q':  # If the user inputs 'q', break out of the loop
                    break
            start_index += page_size  # Move the starting index to the next page

    except mysql.connector.Error as e:
        # Handle MySQL database errors (e.g., connection issues)
        print(f"\nDatabase error: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"\nAn unexpected error occurred: {e}")


# Update an Employee record
def update_employee(cursor):
    """
    Update employee details based on employee ID with validation and error handling.
    This function allows the user to update employee data and handles different types of validation for each field.
    """
    try:
        # Step 1: Get the employee ID to update
        employee_id = input("Enter Employee ID to update: ").strip()
        # Validate that the employee ID is numeric
        if not employee_id.isdigit():
            raise ValueError("Employee ID must be a numeric value.")

        # Step 2: Check if the employee exists in the database
        cursor.execute("SELECT * FROM Employee WHERE employee_id = %s", (employee_id,))
        employee_data = cursor.fetchone()

        if not employee_data:
            # If no employee is found, print a message and return
            print(f"Employee with ID {employee_id} not found.")
            return

        # Step 3: Display the current details of the employee
        print("\nCurrent Employee Details:")
        print(f"1. First Name: {employee_data[1]}")
        print(f"2. Last Name: {employee_data[2]}")
        print(f"3. Email: {employee_data[3]}")
        print(f"4. Phone: {employee_data[4] or 'N/A'}")  # Display 'N/A' if phone is null
        print(f"5. Role: {employee_data[5]}")
        print(f"6. Hire Date: {employee_data[6].strftime('%Y-%m-%d') if employee_data[6] else 'N/A'}")

        # Step 4: Define a dictionary to map option numbers to database field names
        fields = {
            "1": "first_name",
            "2": "last_name",
            "3": "email",
            "4": "phone",
            "5": "role",
            "6": "hire_date"
        }

        updates = {}  # Dictionary to store the fields that will be updated and their new values

        # Step 5: Prompt user to choose which fields they want to update
        print("\nWhich fields would you like to update?")
        print("1. First Name\n2. Last Name\n3. Email\n4. Phone\n5. Role\n6. Hire Date")
        print("Enter multiple numbers separated by commas (e.g., 1,3) or 'all' to update everything.")

        # Step 6: Get the user's choices for fields to update
        choices = input("Enter your choices: ").strip()

        # Step 7: Determine which fields to update based on user input
        if choices.lower() == "all":
            selected_fields = fields.keys()  # Select all fields if 'all' is entered
        else:
            selected_fields = choices.split(",")  # Split choices into a list of fields

        # Step 8: Loop through selected fields and gather new values
        for choice in selected_fields:
            choice = choice.strip()  # Clean up any spaces
            if choice in fields:
                # Prompt for new value for the selected field
                new_value = input(f"Enter new value for {fields[choice]} (press Enter to skip): ").strip()
                if new_value:  # Only update if a new value is provided
                    # Validate and convert input based on the field type
                    if fields[choice] == "email":
                        new_value = validate_email(new_value)  # Validate email format
                    elif fields[choice] == "phone":
                        new_value = validate_phone(new_value)  # Validate phone format
                    elif fields[choice] == "role":
                        new_value = validate_role(new_value)  # Validate role
                    elif fields[choice] == "hire_date":
                        new_value = validate_date(new_value)  # Validate date format
                    elif fields[choice] in ["first_name", "last_name"] and not new_value:
                        # Raise error if first or last name is empty
                        raise ValueError(f"{fields[choice]} cannot be empty.")

                    # Add the new value to the updates dictionary
                    updates[fields[choice]] = new_value
            else:
                # Handle invalid choices by skipping them
                print(f"Invalid choice: {choice}. Skipping...")

        # Step 9: If no valid fields were selected, print a message and return
        if not updates:
            print("No valid fields selected. Returning to menu.")
            return

        # Step 10: Confirm the changes with the user before updating
        print("\nChanges to be made:")
        for field, value in updates.items():
            print(f"{field}: {value}")

        # Step 11: Ask for user confirmation to proceed with the update
        confirm = input("\nAre you sure you want to update this employee? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Update canceled.")
            return  # Return if the user cancels the update

        # Step 12: Construct the SQL UPDATE query dynamically based on the fields to be updated
        set_clause = ", ".join(f"{field} = %s" for field in updates.keys())  # Generate SET clause for SQL
        query = f"UPDATE Employee SET {set_clause} WHERE employee_id = %s"

        # Step 13: Prepare the values for the SQL query
        values = list(updates.values()) + [employee_id]  # Add employee_id at the end

        # Step 14: Execute the SQL UPDATE query to apply the changes
        cursor.execute(query, values)

        # Step 15: Inform the user that the employee record was updated successfully
        print("Employee record updated successfully!")

    except ValueError as ve:
        # Step 16: Handle validation errors (e.g., invalid email or phone format)
        print(f"Input validation error: {ve}")
    except mysql.connector.Error as e:
        # Step 17: Handle MySQL database errors
        if e.errno == 1062:  # Duplicate entry error
            print(f"Error: Employee with email {updates.get('email')} already exists.")
        else:
            print(f"Database error: {e}")
    except Exception as e:
        # Step 18: Handle unexpected errors
        print(f"An unexpected error occurred: {e}")


# Delete an Employee record
def delete_employee(cursor):
    """
    Delete an employee record by ID with validation, error handling, and user confirmation.
    This function ensures the employee exists, checks for related records in other tables,
    and confirms deletion with the user before proceeding.
    """
    try:
        # Step 1: Get the employee ID to delete
        employee_id = input("Enter Employee ID to delete: ").strip()

        # Step 2: Validate that the employee ID is numeric
        if not employee_id.isdigit():
            print("Invalid employee ID. Please enter a numeric value.")
            return  # Exit if the ID is not valid

        # Step 3: Check if the employee exists in the database
        cursor.execute("SELECT * FROM Employee WHERE employee_id = %s", (employee_id,))
        employee_data = cursor.fetchone()

        if not employee_data:
            # If the employee doesn't exist, print a message and return
            print(f"Employee with ID {employee_id} not found.")
            return

        # Step 4: Display the current details of the employee for user confirmation
        print("\nEmployee Details:")
        print(f"ID: {employee_data[0]}")
        print(f"First Name: {employee_data[1]}")
        print(f"Last Name: {employee_data[2]}")
        print(f"Email: {employee_data[3]}")
        print(f"Phone: {employee_data[4] or 'N/A'}")  # Display 'N/A' if phone is null
        print(f"Role: {employee_data[5]}")
        print(f"Hire Date: {employee_data[6].strftime('%Y-%m-%d') if employee_data[6] else 'N/A'}")

        # Step 5: Check for related records in other tables before deletion
        # Check for maintenance requests linked to this employee
        cursor.execute("SELECT COUNT(*) FROM MaintenanceRequest WHERE employee_id = %s", (employee_id,))
        maintenance_count = cursor.fetchone()[0]

        # Check for payment records where the employee was the recipient
        cursor.execute("SELECT COUNT(*) FROM Payment WHERE received_by = %s", (employee_id,))
        payment_count = cursor.fetchone()[0]

        # Step 6: Warn user if there are related records that would be deleted
        if maintenance_count > 0 or payment_count > 0:
            print(f"\nWARNING: Deleting this employee will also remove {maintenance_count} maintenance request(s) and {payment_count} payment record(s).")

        # Step 7: Confirm with the user if they really want to delete the employee
        confirm = input("\nAre you sure you want to delete this employee? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Deletion canceled.")
            return  # If the user cancels, return without deleting

        # Step 8: Execute the delete query
        query = "DELETE FROM Employee WHERE employee_id = %s"
        cursor.execute(query, (employee_id,))

        # Step 9: Check if the deletion was successful
        if cursor.rowcount > 0:
            print(f"Employee with ID {employee_id} deleted successfully!")
        else:
            # If no rows were affected, the deletion was not successful
            print(f"No employee found with ID {employee_id}.")

    except mysql.connector.Error as e:
        # Step 10: Handle MySQL database errors
        if e.errno == 1451:  # Foreign key constraint error
            print("Cannot delete employee record due to related records in other tables.")
        else:
            print(f"Database error: {e}")  # Print other MySQL errors
    except Exception as e:
        # Step 11: Handle unexpected errors
        print(f"An unexpected error occurred: {e}")


# PropertyOwner Table CRUD Functions

def validate_ownership_percentage(percentage):
    """Validate that the ownership percentage is a valid number between 0 and 100."""
    try:
        # Try converting the input to a float
        percentage = float(percentage)

        # Check if the percentage is between 0 and 100
        if not (0 <= percentage <= 100):
            raise ValueError("Ownership percentage must be between 0 and 100.")

        return percentage  # Return the valid percentage

    except ValueError:
        # If the conversion to float fails or the value is out of range, raise a ValueError
        raise ValueError("Ownership percentage must be a valid number.")


# Create a new Property/Owner record
def create_property_owner(cursor):
    """
    Insert a new record into the PropertyOwner table with validation and error handling.
    This function ensures proper validation of inputs, checks for existing records, and provides
    confirmation before inserting a new Property-Owner relationship into the database.
    """
    try:
        # Step 1: Get the property ID and validate it
        property_id = input("Enter Property ID: ").strip()

        # Check if property ID is numeric
        if not property_id.isdigit():
            raise ValueError("Property ID must be a numeric value.")

        # Step 2: Check if the property exists in the database
        cursor.execute("SELECT * FROM Property WHERE property_id = %s", (property_id,))
        property_data = cursor.fetchone()

        # If no property is found, notify the user and return
        if not property_data:
            print(f"Property with ID {property_id} not found.")
            return

        # Step 3: Get the owner ID and validate it
        owner_id = input("Enter Owner ID: ").strip()

        # Check if owner ID is numeric
        if not owner_id.isdigit():
            raise ValueError("Owner ID must be a numeric value.")

        # Step 4: Check if the owner exists in the database
        cursor.execute("SELECT * FROM Owner WHERE owner_id = %s", (owner_id,))
        owner_data = cursor.fetchone()

        # If no owner is found, notify the user and return
        if not owner_data:
            print(f"Owner with ID {owner_id} not found.")
            return

        # Step 5: Get the ownership percentage and validate it using the helper function
        ownership_percentage = validate_ownership_percentage(input("Enter Ownership Percentage: ").strip())

        # Step 6: Check if the Property-Owner relationship already exists
        cursor.execute("SELECT * FROM PropertyOwner WHERE property_id = %s AND owner_id = %s", (property_id, owner_id))

        # If the relationship already exists, notify the user and return
        if cursor.fetchone():
            print(f"Property-Owner relationship for Property ID {property_id} and Owner ID {owner_id} already exists.")
            return

        # Step 7: Check if the total ownership percentage exceeds 100%
        cursor.execute("SELECT SUM(ownership_percentage) FROM PropertyOwner WHERE property_id = %s", (property_id,))
        total_percentage = cursor.fetchone()[0] or 0

        # If the new ownership percentage would exceed 100%, notify the user and return
        if total_percentage + ownership_percentage > 100:
            print(f"Total ownership percentage for Property ID {property_id} would exceed 100%.")
            return

        # Step 8: Display property and owner details for user confirmation
        print("\nProperty Details:")
        print(f"ID: {property_data[0]}")
        print(f"Address: {property_data[1]}")
        print(f"City: {property_data[2]}")
        print(f"State: {property_data[3]}")
        print(f"ZIP: {property_data[4]}")
        print(f"Type: {property_data[5]}")
        print(f"Square Feet: {property_data[6] or 'N/A'}")
        print(f"Year Built: {property_data[7] or 'N/A'}")
        print(f"Purchase Date: {property_data[8].strftime('%Y-%m-%d') if property_data[8] else 'N/A'}")
        print(f"Purchase Price: ${property_data[9]:,.2f}" if property_data[9] else "Purchase Price: N/A")

        print("\nOwner Details:")
        print(f"ID: {owner_data[0]}")
        print(f"First Name: {owner_data[1]}")
        print(f"Last Name: {owner_data[2]}")
        print(f"Email: {owner_data[3]}")
        print(f"Phone: {owner_data[4] or 'N/A'}")
        print(f"Mailing Address: {owner_data[5] or 'N/A'}")

        # Step 9: Confirm with the user before creating the Property-Owner relationship
        confirm = input(
            "\nAre you sure you want to create this Property-Owner relationship? (yes/no): ").strip().lower()

        # If the user doesn't confirm, cancel the creation
        if confirm != "yes":
            print("Creation canceled.")
            return

        # Step 10: SQL query to insert the new Property-Owner relationship into the PropertyOwner table
        query = """
        INSERT INTO PropertyOwner (property_id, owner_id, ownership_percentage)
        VALUES (%s, %s, %s)
        """
        values = (property_id, owner_id, ownership_percentage)

        # Step 11: Execute the query to insert the new record
        cursor.execute(query, values)

        # Step 12: Notify the user that the PropertyOwner record has been added successfully
        print("PropertyOwner record added successfully!")

    except ValueError as ve:
        # Step 13: Handle any validation errors (such as invalid inputs)
        print(f"Input validation error: {ve}")
    except mysql.connector.Error as e:
        # Step 14: Handle database-related errors
        if e.errno == 1062:  # Duplicate entry error (i.e., the relationship already exists)
            print(
                f"Error: Property-Owner relationship for Property ID {property_id} and Owner ID {owner_id} already exists.")
        else:
            print(f"Database error: {e}")
    except Exception as e:
        # Step 15: Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")


# Read and Display all PropertyOwner records
def read_property_owners(cursor, page_size=10):
    """
    Retrieve and display all PropertyOwner records in a paginated and formatted table.
    """
    try:
        # Step 1: Execute query to fetch all PropertyOwner records along with property and owner details
        query = """
        SELECT 
            po.property_id, p.address, po.owner_id, 
            CONCAT(o.first_name, ' ', o.last_name) AS owner_name, 
            po.ownership_percentage
        FROM PropertyOwner po
        JOIN Property p ON po.property_id = p.property_id
        JOIN Owner o ON po.owner_id = o.owner_id
        ORDER BY po.property_id, po.owner_id
        """
        cursor.execute(query)  # Execute the query
        records = cursor.fetchall()  # Fetch all records from the executed query

        # Step 2: Check if records are empty, and if so, notify the user and return
        if not records:
            print("\nNo PropertyOwner records found.")
            return

        # Step 3: Format results into a more readable structure (list of dictionaries)
        formatted_records = []  # List to hold formatted record dictionaries
        for record in records:
            formatted_record = {
                "Property ID": record[0],  # Property ID
                "Address": record[1],  # Property address
                "Owner ID": record[2],  # Owner ID
                "Owner Name": record[3],  # Full name of the owner (concatenated first and last name)
                "Ownership Percentage": f"{record[4]}%"  # Ownership percentage with a '%' sign
            }
            formatted_records.append(formatted_record)  # Add formatted record to the list

        # Step 4: Display results in a table format with pagination
        total_records = len(formatted_records)  # Get the total number of records
        start_index = 0  # Initialize the starting index for pagination

        # Step 5: Loop through the records and display in pages
        while start_index < total_records:
            print("\nProperty Owner Records:")
            # Print a table with the current page of records
            print(tabulate(formatted_records[start_index:start_index + page_size], headers="keys", tablefmt="grid", stralign="left"))
            # Display the range of records currently being shown (for pagination info)
            print(f"\nDisplaying {start_index + 1} to {min(start_index + page_size, total_records)} of {total_records} records.")

            # Step 6: Check if there are more records to show and ask the user for next page
            if start_index + page_size < total_records:
                next_page = input("\nPress Enter to view the next page or 'q' to quit: ").strip().lower()
                if next_page == 'q':  # If the user presses 'q', break out of the loop
                    break

            # Move the start index to the next page
            start_index += page_size

    except mysql.connector.Error as e:
        # Step 7: Handle database-related errors
        print(f"\nDatabase error: {e}")
    except Exception as e:
        # Step 8: Handle any unexpected errors
        print(f"\nAn unexpected error occurred: {e}")


# Update an ownership percentage
def update_property_owner(cursor):
    """
    Update the ownership percentage for a property-owner relationship with validation and error handling.
    """
    try:
        # Step 1: Get the Property ID and validate it
        property_id = input("Enter Property ID: ").strip()  # Prompt the user for Property ID
        if not property_id.isdigit():  # Validate that the Property ID is numeric
            raise ValueError("Property ID must be a numeric value.")

        # Step 2: Check if the property exists in the database
        cursor.execute("SELECT * FROM Property WHERE property_id = %s", (property_id,))
        property_data = cursor.fetchone()  # Fetch the property data from the database

        if not property_data:  # If no property is found, inform the user and return
            print(f"Property with ID {property_id} not found.")
            return

        # Step 3: Get the Owner ID and validate it
        owner_id = input("Enter Owner ID: ").strip()  # Prompt the user for Owner ID
        if not owner_id.isdigit():  # Validate that the Owner ID is numeric
            raise ValueError("Owner ID must be a numeric value.")

        # Step 4: Check if the owner exists in the database
        cursor.execute("SELECT * FROM Owner WHERE owner_id = %s", (owner_id,))
        owner_data = cursor.fetchone()  # Fetch the owner data from the database

        if not owner_data:  # If no owner is found, inform the user and return
            print(f"Owner with ID {owner_id} not found.")
            return

        # Step 5: Check if the property-owner relationship exists
        cursor.execute("SELECT * FROM PropertyOwner WHERE property_id = %s AND owner_id = %s", (property_id, owner_id))
        property_owner_data = cursor.fetchone()  # Fetch the existing property-owner relationship

        if not property_owner_data:  # If no relationship is found, inform the user and return
            print(f"Property-Owner relationship for Property ID {property_id} and Owner ID {owner_id} not found.")
            return

        # Step 6: Display current ownership percentage for the property-owner relationship
        print(f"\nCurrent Ownership Percentage: {property_owner_data[2]}%")  # Show the current percentage

        # Step 7: Get the new ownership percentage and validate it
        new_percentage = validate_ownership_percentage(
            input("Enter new Ownership Percentage: ").strip())  # Validate the new percentage

        # Step 8: Check if the total ownership percentage exceeds 100% after the update
        cursor.execute("SELECT SUM(ownership_percentage) FROM PropertyOwner WHERE property_id = %s", (property_id,))
        total_percentage = cursor.fetchone()[0] or 0  # Fetch the total percentage for the property

        # Adjust total percentage by removing the old value and adding the new one
        total_percentage = total_percentage - property_owner_data[2] + new_percentage

        if total_percentage > 100:  # If the total exceeds 100%, inform the user and return
            print(f"Total ownership percentage for Property ID {property_id} would exceed 100%.")
            return

        # Step 9: Confirm the update with the user before proceeding
        confirm = input("\nAre you sure you want to update this ownership percentage? (yes/no): ").strip().lower()
        if confirm != "yes":  # If the user doesn't confirm, cancel the update
            print("Update canceled.")
            return

        # Step 10: Construct the SQL query to update the ownership percentage in the database
        query = """
        UPDATE PropertyOwner
        SET ownership_percentage = %s
        WHERE property_id = %s AND owner_id = %s
        """
        values = (new_percentage, property_id, owner_id)  # Set the new percentage, property ID, and owner ID

        # Step 11: Execute the update query
        cursor.execute(query, values)  # Update the ownership percentage in the database
        print("Ownership percentage updated successfully!")  # Inform the user that the update was successful

    except ValueError as ve:  # Catch any validation errors (e.g., invalid inputs)
        print(f"Input validation error: {ve}")
    except mysql.connector.Error as e:  # Catch database-related errors
        if e.errno == 1062:  # Duplicate entry error (if applicable)
            print(
                f"Error: Property-Owner relationship for Property ID {property_id} and Owner ID {owner_id} already exists.")
        else:
            print(f"Database error: {e}")  # Handle any other database errors
    except Exception as e:  # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")


# Delete a Property/Owner record
def delete_property_owner(cursor):
    """
    Delete a property-owner relationship by property and owner ID with validation and error handling.
    """
    try:
        # Step 1: Get the Property ID and validate it
        property_id = input("Enter Property ID: ").strip()  # Prompt the user for the Property ID
        if not property_id.isdigit():  # Validate that the Property ID is numeric
            raise ValueError("Property ID must be a numeric value.")

        # Step 2: Check if the property exists in the database
        cursor.execute("SELECT * FROM Property WHERE property_id = %s", (property_id,))
        property_data = cursor.fetchone()  # Fetch the property data from the database

        if not property_data:  # If no property is found, inform the user and return
            print(f"Property with ID {property_id} not found.")
            return

        # Step 3: Get the Owner ID and validate it
        owner_id = input("Enter Owner ID: ").strip()  # Prompt the user for the Owner ID
        if not owner_id.isdigit():  # Validate that the Owner ID is numeric
            raise ValueError("Owner ID must be a numeric value.")

        # Step 4: Check if the owner exists in the database
        cursor.execute("SELECT * FROM Owner WHERE owner_id = %s", (owner_id,))
        owner_data = cursor.fetchone()  # Fetch the owner data from the database

        if not owner_data:  # If no owner is found, inform the user and return
            print(f"Owner with ID {owner_id} not found.")
            return

        # Step 5: Check if the property-owner relationship exists
        cursor.execute("SELECT * FROM PropertyOwner WHERE property_id = %s AND owner_id = %s", (property_id, owner_id))
        property_owner_data = cursor.fetchone()  # Fetch the property-owner relationship data

        if not property_owner_data:  # If no relationship is found, inform the user and return
            print(f"Property-Owner relationship for Property ID {property_id} and Owner ID {owner_id} not found.")
            return

        # Step 6: Display property and owner details for confirmation
        print("\nProperty Details:")
        print(f"ID: {property_data[0]}")
        print(f"Address: {property_data[1]}")
        print(f"City: {property_data[2]}")
        print(f"State: {property_data[3]}")
        print(f"ZIP: {property_data[4]}")
        print(f"Type: {property_data[5]}")
        print(f"Square Feet: {property_data[6] or 'N/A'}")
        print(f"Year Built: {property_data[7] or 'N/A'}")
        print(f"Purchase Date: {property_data[8].strftime('%Y-%m-%d') if property_data[8] else 'N/A'}")
        print(f"Purchase Price: ${property_data[9]:,.2f}" if property_data[9] else "Purchase Price: N/A")

        print("\nOwner Details:")
        print(f"ID: {owner_data[0]}")
        print(f"First Name: {owner_data[1]}")
        print(f"Last Name: {owner_data[2]}")
        print(f"Email: {owner_data[3]}")
        print(f"Phone: {owner_data[4] or 'N/A'}")
        print(f"Mailing Address: {owner_data[5] or 'N/A'}")

        # Step 7: Confirm deletion with the user
        confirm = input("\nAre you sure you want to delete this Property-Owner relationship? (yes/no): ").strip().lower()
        if confirm != "yes":  # If the user doesn't confirm, cancel the deletion
            print("Deletion canceled.")
            return

        # Step 8: Construct the SQL query to delete the property-owner relationship
        query = "DELETE FROM PropertyOwner WHERE property_id = %s AND owner_id = %s"
        values = (property_id, owner_id)  # Set the property and owner IDs to delete

        # Step 9: Execute the query to delete the relationship from the database
        cursor.execute(query, values)  # Perform the delete operation in the database

        # Step 10: Check if the deletion was successful
        if cursor.rowcount > 0:  # If rows were affected, the deletion was successful
            print("Property-Owner relationship deleted successfully!")
        else:  # If no rows were affected, inform the user that no such relationship was found
            print("No Property-Owner relationship found for the given IDs.")

    except ValueError as ve:  # Catch any validation errors (e.g., invalid inputs)
        print(f"Input validation error: {ve}")
    except mysql.connector.Error as e:  # Catch database-related errors
        if e.errno == 1451:  # Foreign key constraint error, meaning the relationship is in use elsewhere
            print("Cannot delete Property-Owner relationship due to related records in other tables.")
        else:  # Handle other database errors
            print(f"Database error: {e}")
    except Exception as e:  # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")


# Function to manage CRUD operations for different tables dynamically
def manage_table(table_name):
    """
    Manage CRUD operations for a specific table dynamically.
    This function allows users to choose actions (Create, Read, Update, Delete) on a specific table in the database.
    The table operations are defined in a dictionary to map user choices to the correct CRUD functions.
    """

    # Dictionary mapping table names to their respective CRUD functions
    # Each table has a set of operations where the keys are the menu options (1-4)
    # and the values are the corresponding functions to perform the operations.
    table_operations = {
        "Property": {
            "1": create_property,
            "2": read_properties,
            "3": update_property,
            "4": delete_property,
        },
        "Owner": {
            "1": create_owner,
            "2": read_owners,
            "3": update_owner,
            "4": delete_owner,
        },
        "PropertyOwner": {
            "1": create_property_owner,
            "2": read_property_owners,
            "3": update_property_owner,
            "4": delete_property_owner,
        },
        "Tenant": {
            "1": create_tenant,
            "2": read_tenants,
            "3": update_tenant,
            "4": delete_tenant,
        },
        "Lease": {
            "1": create_lease,
            "2": read_leases,
            "3": update_lease,
            "4": delete_lease,
        },
        "MaintenanceRequest": {
            "1": create_maintenance_request,
            "2": read_maintenance_requests,
            "3": update_maintenance_request,
            "4": delete_maintenance_request,
        },
        "Payment": {
            "1": create_payment,
            "2": read_payments,
            "3": update_payment,
            "4": delete_payment,
        },
        "Employee": {
            "1": create_employee,
            "2": read_employees,
            "3": update_employee,
            "4": delete_employee,
        },
    }

    # Step 1: Validate if the given table name exists in the dictionary of operations
    if table_name not in table_operations:
        print(f"Invalid table name: {table_name}.")  # Print an error if the table name is not valid
        return  # Exit the function if the table name is invalid

    # Step 2: Connect to the database
    conn = connect_db()  # Function that returns a database connection
    if not conn:
        return  # Exit if the connection fails

    # Step 3: Use a context manager for the cursor to ensure it is properly closed after use
    with conn.cursor() as cursor:
        while True:
            # Display menu options for managing records in the chosen table
            print(f"\nManaging {table_name}")
            print(
                "1. Create New Record\n2. Display All Records\n3. Update a Record\n4. Delete a Record\n5. Back to main menu")
            choice = input("Choose an option: ").strip()  # Get user's choice

            # If user chooses to go back to the main menu
            if choice == "5":
                print("Returning to main menu.")
                break  # Exit the loop and return to the main menu

            # Step 4: Retrieve the appropriate function based on the table and user choice
            operation = table_operations[table_name].get(choice)
            if operation:
                try:
                    # Call the appropriate CRUD function with the cursor as argument
                    operation(cursor)
                    conn.commit()  # Commit changes to the database after the operation
                except Exception as e:
                    # Handle any errors that occur during the operation
                    print(f"An error occurred: {e}")
                    conn.rollback()  # Rollback any changes if an error occurs
            else:
                # If the user selects an invalid option, inform them
                print("Invalid choice! Please select a valid option.")

    # Step 5: Close the database connection after all operations are done
    conn.close()  # Ensure the connection to the database is properly closed


# Main function that provides a menu for managing different database tables
def main():
    """
    Main function that provides a menu for managing different database tables.
    The user can select a table and perform CRUD operations on it.
    """

    # Dictionary mapping menu options to table names
    # This allows the program to display the options dynamically and handle different tables
    menu_options = {
        "1": "Property",
        "2": "Owner",
        "3": "Tenant",
        "4": "Lease",
        "5": "MaintenanceRequest",
        "6": "Payment",
        "7": "Employee",  # Added Employee table
        "8": "PropertyOwner",  # Added PropertyOwner table
        "9": "Exit",  # Moved Exit to option 9
    }

    # Infinite loop for displaying the menu and handling user input
    while True:
        # Display the title of the application
        print("\nReal Estate Property Management CLI")
        print("Select which table to manage:")

        # Dynamically display the menu options based on the `menu_options` dictionary
        for key, value in menu_options.items():
            print(f"{key}. {value}")  # Print the key-value pair as a menu item

        # Get the user's input choice from the menu
        choice = input("Select an option: ").strip()

        # If the user selects option 9, prompt to confirm exiting the application
        if choice == "9":  # Exit option (updated to 9)
            confirm = input("Are you sure you want to exit? (yes/no): ").strip().lower()
            if confirm == "yes":
                print("Exiting...")  # Exit message
                break  # Exit the loop and terminate the program
            else:
                print("Returning to main menu.")  # If user doesn't confirm, return to the menu
                continue  # Continue the loop and redisplay the menu

        # Retrieve the table name based on the user's choice from the dictionary
        table_name = menu_options.get(choice)

        # If a valid table name is retrieved, manage the selected table
        if table_name:
            manage_table(table_name)  # Call the function to manage the selected table
        else:
            # If the choice is invalid, inform the user
            print("Invalid choice! Please select a valid option.")


# Entry point of the script - Runs the main function when the script is executed
if __name__ == "__main__":
    main()  # Call the main function to start the program
