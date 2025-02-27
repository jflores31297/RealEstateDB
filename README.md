# Real Estate Property Management CLI

## Overview

## Purpose

The Real Estate Property Management Command Line Interface (CLI) is designed to help manage a real estate property management system by allowing users to perform CRUD (Create, Read, Update, Delete) operations on property and owner records. This tool allows real estate administrators to efficiently handle property listings and owner information, providing a simple, interactive way to manage the database.

## Application Scope
- Manage property listings: Includes details such as address, type, purchase details, etc.
- Manage owner records: Stores personal and contact information for owners.
- Handle relationships between properties and owners: Each property may have one or more owners.

## Features

Property Management:
- Create: Add new property records with validation (e.g., date format, ZIP code, property type).
- Read: Display properties in a formatted table.
- Update: Modify property details interactively.
- Delete: Remove property records with confirmation and error handling.

Owner Management:
- Create: Add new owner records with validation (e.g., email, phone number format).
- Read: View owner records with pagination support.
- Update: Update owner information interactively.
- Delete: Delete owner records after confirming no properties are associated with them.

Logging & Error Handling:
- Error Logging: Logs errors to a file (e.g., database.log).
- User Prompts: Provides informative prompts and error messages to guide the user through each operation.

## Database Structure

### Database Name:
- RealEstateDB (default)

### Main Tables:
The database consists of nine tables, each serving a specific role in property management.

1. Property Table
- Stores details of real estate properties.
- Key attributes: `property_id`, `address`, `city`, `state`, `zip_code`, `property_type`, `square_feet`, `year_built`, `purchase_date`, `purchase_price`.

2. Owner Table
- Holds property owner details.
- Key attributes: `owner_id`, `first_name`, `last_name`, `email`, `phone`, `mailing_address`.

3. Tenant Table
- Contains tenant information.
- Key attributes: `tenant_id`, `first_name`, `last_name`, `email`, `phone`, `employer`, `emergency_contact`.

4. Employee Table
- Stores details of employees managing properties.
- Key attributes: `employee_id`, `first_name`, `last_name`, `email`, `phone`, `role`, `hire_date`.

5. Lease Table
- Manages lease agreements between tenants and properties.
- Key attributes: `lease_id`, `property_id` (FK), `tenant_id` (FK), `start_date`, `end_date`, `monthly_rent`, `security_deposit`, `lease_status`, `due_day`.
- Foreign Keys:
	- `property_id` → Property(`property_id`) (Deletes lease if property is removed).
	- `tenant_id` → Tenant(`tenant_id`) (Deletes lease if tenant is removed).

6. MaintenanceRequest Table
- Tracks property maintenance requests.
- Key attributes: `request_id`, `property_id` (FK), `tenant_id` (FK), `employee_id` (FK), `description`, `request_date`, `completion_date`, `status`, `cost`.
- Foreign Keys:
	- `property_id` → Property(`property_id`) (Deletes request if property is removed).
	- `tenant_id` → Tenant(`tenant_id`) (Sets NULL if tenant is removed).
	- `employee_id` → Employee(`employee_id`) (Sets NULL if employee is removed).

7. Payment Table
- Stores rental payments made by tenants.
- Key attributes: `payment_id`, `lease_id` (FK), `amount`, `payment_date`, `payment_method`, `received_by` (FK).
- Foreign Keys:
	- `lease_id` → Lease(`lease_id`) (Deletes payment if lease is removed).
	- `received_by` → Employee(`employee_id`) (Sets NULL if employee is removed).

8. PropertyOwner Table
- Establishes ownership relationships between properties and owners.
- Key attributes: `property_id` (FK), `owner_id` (FK), `ownership_percentage`.
- Foreign Keys:
	- `property_id` → Property(`property_id`) (Deletes record if property is removed).
	- `owner_id` → Owner(`owner_id`) (Deletes record if owner is removed).

9. PaymentAudit Table
- Logs audits of rental payments.
- Key attributes: `audit_id`, `payment_id` (FK), `late_fee`, `audit_timestamp`.
- Foreign Key:
	- `payment_id` → Payment(`payment_id`)

## Key Features & Relationships
- Property-Tenant-Lease: A Tenant can lease a Property, and this relationship is stored in the Lease table.
- Property-Owner: Multiple Owners can own a property, and ownership percentages are recorded in the PropertyOwner table.
- Maintenance & Employees: Employees handle maintenance requests assigned to them.
- Payments & Audits: Tenants make payments, which are audited for late fees.

## Installation & Setup

4.1 Prerequisites

Software Requirements:
	•	Python 3.7+
	•	MySQL Server

Python Dependencies:
	•	mysql-connector-python (for database connectivity)
	•	tabulate (for formatting tables in the CLI)
	•	pytest (for running tests)

Other Standard Libraries:
	•	logging, os, datetime, etc.

4.2 Database Setup

Run the SQL Script:
	1.	Locate the provided SQL file (e.g., Deliverable_2.sql).
	2.	Use your MySQL client (or MySQL Workbench) to run the script, which will create the RealEstateDB database and necessary tables.

Verify Database:
	•	Confirm that the tables (Property, Owner, PropertyOwner) have been created with the expected columns and relationships.

4.3 Environment Variables

Configuration:

Set up the following environment variables to enable the CLI to connect to the database:
	•	DB_HOST (default: localhost)
	•	DB_USER (default: root)
	•	DB_PASSWORD (default: your password)
	•	DB_NAME (default: RealEstateDB)

Example Setup:

For Unix-like systems, add the following to your shell configuration or export them in the terminal:

export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=RealEstateDB

4.4 Installing Dependencies

Use pip to install the required dependencies:

pip install mysql-connector-python tabulate pytest

## Usage

5.1 Running the CLI

Start the Application:

Run the Python script (e.g., real_estate_crud.py) from the command line:

python real_estate_crud.py

User Prompts:

The CLI will prompt you for input to perform various actions, such as adding a property or updating an owner.

5.2 Commands / Operations

Property Operations:
	•	Create: Enter property details such as address, city, state, zip code, and property type. Optional fields include square feet, year built, purchase date, and purchase price.
	•	Read: Display all property listings in a formatted table.
	•	Update: Select a property by ID, choose which fields to update, and enter new values.
	•	Delete: Enter the property ID to delete, with confirmation prompts.

Owner Operations:
	•	Create: Enter owner details, including first name, last name, email, phone (optional), and mailing address.
	•	Read: List all owners with pagination.
	•	Update: Select an owner by ID, choose fields to update, and provide new values.
	•	Delete: Remove an owner record after confirming that no properties are associated with the owner.

5.3 Example Walkthrough

Adding a Property:
	1.	Launch the CLI.
	2.	Select “Create Property” and follow the prompts to enter property details.

Updating an Owner:
	1.	Select the owner to update.
	2.	Choose the email field and enter a new valid email.

Deleting a Property/Owner:
	1.	Select the property or owner to delete.
	2.	Follow the confirmation prompts to ensure accidental deletions are avoided.

## Logging and Troubleshooting

7.1 Logging:
	•	All errors are logged to database.log.

7.2 Common Issues:
	•	Database Connection Failures: Check environment variable settings and ensure the MySQL server is running.
	•	Input Validation Errors: Ensure dates, emails, zip codes, and phone numbers are formatted correctly.

7.3 Troubleshooting Tips:
	•	Review the log file for error details.
	•	Re-run the SQL script if tables or relationships appear to be missing.

## Future Enhancements
•	Additional features like lease management and reporting.
•	Improved error handling and user experience.
•	Integration with web-based interfaces for broader accessibility.
