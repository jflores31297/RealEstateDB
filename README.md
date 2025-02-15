# 🏠 Real Estate Property Management CLI

## 📌 Project Overview
**Real Estate Property Management CLI** is a command-line application that allows real estate managers to **efficiently track and manage properties, owners, tenants, leases, rent payments, and maintenance requests** using a MySQL database.

### 🔹 **Features**
✅ Add, view, update, and delete properties, owners, and tenants  
✅ Manage lease agreements and rent payments  
✅ Submit and track maintenance requests  
✅ Validate user inputs (emails, phone numbers, zip codes, and dates)  
✅ User-friendly CLI interface for property managers  

---

## 🚀 Installation & Setup

### **1️⃣ Prerequisites**
- **Python 3.8+**  
- **MySQL Server** installed and running  
- Install required dependencies:
  ```sh
  pip install mysql-connector-python tabulate

2️⃣ Database Setup
	1.	Create the Database
Run the provided SQL script to create the database and tables:

mysql -u root -p < Deliverable_2.sql


	2.	Configure Environment Variables
Set up database credentials:

export DB_HOST="localhost"
export DB_USER="root"
export DB_PASSWORD="yourpassword"
export DB_NAME="RealEstateDB"

🎯 How to Use the CLI

🔹 Running the CLI

Start the application with:

python real_estate_crud.py

🔹 Main Features

🏡 1. Property Management

Action	Command
Add a new property	create_property()
View all properties	read_properties()
Update property details	update_property()
Delete a property	delete_property()

👤 2. Owner Management

Action	Command
Add a new owner	create_owner()
View all owners	read_owners()
Update owner details	update_owner()
Delete an owner	delete_owner()

👨‍💼 3. Tenant Management

Action	Command
Add a new tenant	create_tenant()
View all tenants	read_tenants()
Update tenant details	update_tenant()
Delete a tenant	delete_tenant()

📄 4. Lease Agreements

Action	Command
Create a new lease	create_lease()
View active leases	read_leases()
Update lease terms	update_lease()
End a lease	delete_lease()

💰 5. Rent Payments

Action	Command
Record a payment	record_payment()
View payment history	read_payments()

🔧 6. Maintenance Requests

Action	Command
Submit a request	create_maintenance_request()
View maintenance history	read_maintenance_requests()
Update request status	update_maintenance_request()

❓ Troubleshooting

Issue	Cause	Solution
Can't connect to MySQL	MySQL server is down or credentials are incorrect	Verify DB_HOST, DB_USER, DB_PASSWORD
Table not found	Database setup not completed	Run Deliverable_2.sql to initialize the database
Invalid email format	User entered an incorrect email format	Ensure email follows name@example.com pattern
Data truncation error	Input too long for a column	Check max length constraints in SQL schema

🔮 Future Improvements
	•	Implement a GUI for better user experience
	•	Add role-based access control for multi-user management
	•	Integrate property image storage with cloud services

Happy Property Managing! 🏡✨

---
