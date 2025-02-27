-- 1. Create the RealEstateDB database if it doesn't already exist

DROP DATABASE IF EXISTS RealEstateDB;  -- Deletes the database if it exists to start fresh
CREATE DATABASE RealEstateDB;  -- Creates a new database named RealEstateDB
USE RealEstateDB;  -- Selects RealEstateDB as the active database

-- 2. Create Tables

-- Property Table: Stores details about properties
CREATE TABLE Property (
    property_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each property
    address VARCHAR(255) NOT NULL,  -- Street address (required)
    city VARCHAR(100) NOT NULL,  -- City (required)
    state VARCHAR(50) NOT NULL,  -- State (required)
    zip_code VARCHAR(20) NOT NULL,  -- ZIP code (required)
    property_type ENUM('Single Family', 'Apartment', 'Commercial', 'Condo'),  -- Type of property
    square_feet INT,  -- Property size in square feet
    year_built INT,  -- Year the property was built
    purchase_date DATE,  -- Date the property was purchased
    purchase_price DECIMAL(15,2)  -- Purchase price of the property
);

-- Owner Table: Stores information about property owners
CREATE TABLE Owner (
    owner_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each owner
    first_name VARCHAR(50) NOT NULL,  -- Owner's first name (required)
    last_name VARCHAR(50) NOT NULL,  -- Owner's last name (required)
    email VARCHAR(100) UNIQUE,  -- Unique email address for contact
    phone VARCHAR(20),  -- Phone number (optional)
    mailing_address VARCHAR(255)  -- Mailing address (optional)
);

-- Tenant Table: Stores information about tenants renting properties
CREATE TABLE Tenant (
    tenant_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each tenant
    first_name VARCHAR(50) NOT NULL,  -- Tenant's first name (required)
    last_name VARCHAR(50) NOT NULL,  -- Tenant's last name (required)
    email VARCHAR(100) UNIQUE,  -- Unique email address for contact
    phone VARCHAR(20),  -- Phone number (optional)
    employer VARCHAR(100),  -- Employer name (optional)
    emergency_contact VARCHAR(20)  -- Emergency contact phone number (optional)
);

-- Employee Table: Stores information about employees managing the properties
CREATE TABLE Employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each employee
    first_name VARCHAR(50) NOT NULL,  -- Employee's first name (required)
    last_name VARCHAR(50) NOT NULL,  -- Employee's last name (required)
    email VARCHAR(100) UNIQUE,  -- Unique email address for contact
    phone VARCHAR(20),  -- Phone number (optional)
    role ENUM('Property Manager', 'Maintenance Staff', 'Accountant', 'Leasing Agent'),  -- Employee role
    hire_date DATE  -- Date the employee was hired
);

-- Lease Table: Stores lease agreements between tenants and properties
CREATE TABLE Lease (
    lease_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each lease
    property_id INT,  -- Property being leased
    tenant_id INT,  -- Tenant renting the property
    start_date DATE NOT NULL,  -- Lease start date
    end_date DATE NOT NULL,  -- Lease end date
    monthly_rent DECIMAL(10,2) NOT NULL,  -- Monthly rent amount
    security_deposit DECIMAL(10,2),  -- Security deposit amount
    lease_status ENUM('Active', 'Expired', 'Terminated') DEFAULT 'Active',  -- Lease status
    due_day INT NOT NULL DEFAULT 1,  -- Rent due day (default is 1st of the month)
    FOREIGN KEY (property_id) REFERENCES Property(property_id) ON DELETE CASCADE,  -- Deletes lease if property is removed
    FOREIGN KEY (tenant_id) REFERENCES Tenant(tenant_id) ON DELETE CASCADE  -- Deletes lease if tenant is removed
);

-- MaintenanceRequest Table: Stores maintenance requests made by tenants
CREATE TABLE MaintenanceRequest (
    request_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each maintenance request
    property_id INT,  -- Property associated with the request
    tenant_id INT,  -- Tenant who made the request
    employee_id INT,  -- Employee assigned to the request
    description TEXT NOT NULL,  -- Description of the maintenance issue (required)
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp when the request was submitted
    completion_date DATE,  -- Date when the request was completed
    status ENUM('Open', 'In Progress', 'Completed') DEFAULT 'Open',  -- Status of the maintenance request
    cost DECIMAL(10,2),  -- Cost of maintenance (optional)
    FOREIGN KEY (property_id) REFERENCES Property(property_id) ON DELETE CASCADE,  -- Deletes request if property is removed
    FOREIGN KEY (tenant_id) REFERENCES Tenant(tenant_id) ON DELETE SET NULL,  -- Sets tenant_id to NULL if tenant is removed
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id) ON DELETE SET NULL  -- Sets employee_id to NULL if employee is removed
);

-- Payment Table: Stores payment transactions for lease agreements
CREATE TABLE Payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each payment
    lease_id INT,  -- Lease associated with the payment
    amount DECIMAL(10,2) NOT NULL,  -- Payment amount
    payment_date DATE NOT NULL,  -- Date payment was made
    payment_method ENUM('Credit Card', 'Check', 'Bank Transfer', 'Cash'),  -- Payment method
    received_by INT,  -- Employee who received the payment
    FOREIGN KEY (lease_id) REFERENCES Lease(lease_id) ON DELETE CASCADE,  -- Deletes payment if lease is removed
    FOREIGN KEY (received_by) REFERENCES Employee(employee_id) ON DELETE SET NULL  -- Sets received_by to NULL if employee is removed
);

-- PropertyOwner Table: Manages ownership of properties, allowing multiple owners per property
CREATE TABLE PropertyOwner (
    property_id INT,  -- Property being owned
    owner_id INT,  -- Owner of the property
    ownership_percentage DECIMAL(5,2) CHECK (ownership_percentage BETWEEN 0 AND 100),  -- Ownership percentage (0-100%)
    PRIMARY KEY (property_id, owner_id),  -- Composite primary key ensuring unique ownership records
    FOREIGN KEY (property_id) REFERENCES Property(property_id) ON DELETE CASCADE,  -- Deletes ownership record if property is removed
    FOREIGN KEY (owner_id) REFERENCES Owner(owner_id) ON DELETE CASCADE  -- Deletes ownership record if owner is removed
);

-- PaymentAudit Table: Stores audit records for payments
CREATE TABLE PaymentAudit (  
    audit_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each audit record
    payment_id INT,  -- Payment being audited
    late_fee DECIMAL(10,2),  -- Late fee charged (if applicable)
    audit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp when the audit record was created
    FOREIGN KEY (payment_id) REFERENCES Payment(payment_id)  -- Links to Payment table
);



-- 3. Load Data

-- Insert Properties
INSERT INTO Property (property_id, address, city, state, zip_code, property_type, square_feet, year_built, purchase_date, purchase_price) VALUES
(1, '123 Main St', 'Los Angeles', 'CA', '90001', 'Single Family', 1800, 1995, '2018-06-15', 450000.00),
(2, '456 Oak Ave', 'San Francisco', 'CA', '94103', 'Apartment', 900, 2010, '2020-09-20', 650000.00),
(3, '789 Pine Rd', 'Seattle', 'WA', '98101', 'Condo', 1200, 2005, '2019-04-10', 550000.00),
(4, '101 Maple Dr', 'Austin', 'TX', '73301', 'Single Family', 2200, 1988, '2017-12-01', 375000.00),
(5, '202 Birch Ln', 'Denver', 'CO', '80202', 'Commercial', 5000, 1992, '2021-07-30', 1200000.00),
(6, '303 Elm St', 'Miami', 'FL', '33101', 'Condo', 1100, 2008, '2022-05-05', 490000.00),
(7, '404 Cedar Ave', 'Chicago', 'IL', '60601', 'Apartment', 750, 2015, '2019-11-15', 320000.00),
(8, '505 Walnut St', 'Boston', 'MA', '02108', 'Single Family', 2600, 1975, '2016-08-22', 825000.00),
(9, '606 Spruce Ct', 'Las Vegas', 'NV', '89109', 'Commercial', 7200, 2000, '2020-02-10', 2500000.00),
(10, '707 Redwood Blvd', 'Portland', 'OR', '97201', 'Single Family', 1900, 1998, '2021-01-25', 410000.00),
(11, '808 Fir Dr', 'Phoenix', 'AZ', '85001', 'Condo', 1300, 2012, '2023-03-18', 375000.00),
(12, '909 Aspen Pl', 'Salt Lake City', 'UT', '84101', 'Apartment', 850, 2016, '2018-10-30', 295000.00),
(13, '1010 Sycamore St', 'Dallas', 'TX', '75201', 'Commercial', 6200, 1990, '2017-05-12', 1800000.00),
(14, '1111 Magnolia Way', 'Charlotte', 'NC', '28202', 'Single Family', 2400, 1985, '2015-09-05', 600000.00),
(15, '1212 Dogwood Ln', 'Atlanta', 'GA', '30301', 'Condo', 1400, 2014, '2019-06-28', 425000.00);

-- Insert Owners
INSERT INTO Owner (owner_id, first_name, last_name, email, phone, mailing_address) VALUES
(1, 'John', 'Doe', 'johndoe@example.com', '555-123-4567', '123 Main St, Los Angeles, CA 90001'),
(2, 'Jane', 'Smith', 'janesmith@example.com', '555-234-5678', '456 Oak Ave, San Francisco, CA 94103'),
(3, 'Michael', 'Johnson', 'michaelj@example.com', '555-345-6789', '789 Pine Rd, Seattle, WA 98101'),
(4, 'Emily', 'Davis', 'emilyd@example.com', '555-456-7890', '101 Maple Dr, Austin, TX 73301'),
(5, 'David', 'Martinez', 'davidm@example.com', '555-567-8901', '202 Birch Ln, Denver, CO 80202'),
(6, 'Sarah', 'Brown', 'sarahb@example.com', '555-678-9012', '303 Elm St, Miami, FL 33101'),
(7, 'James', 'Wilson', 'jamesw@example.com', '555-789-0123', '404 Cedar Ave, Chicago, IL 60601'),
(8, 'Jessica', 'Taylor', 'jessicat@example.com', '555-890-1234', '505 Walnut St, Boston, MA 02108'),
(9, 'Christopher', 'Anderson', 'chrisand@example.com', '555-901-2345', '606 Spruce Ct, Las Vegas, NV 89109'),
(10, 'Amanda', 'Thomas', 'amandat@example.com', '555-012-3456', '707 Redwood Blvd, Portland, OR 97201'),
(11, 'Matthew', 'Hernandez', 'matth@example.com', '555-123-6789', '808 Fir Dr, Phoenix, AZ 85001'),
(12, 'Ashley', 'Moore', 'ashleym@example.com', '555-234-7890', '909 Aspen Pl, Salt Lake City, UT 84101'),
(13, 'Daniel', 'Jackson', 'danielj@example.com', '555-345-8901', '1010 Sycamore St, Dallas, TX 75201'),
(14, 'Elizabeth', 'White', 'elizabethw@example.com', '555-456-9012', '1111 Magnolia Way, Charlotte, NC 28202'),
(15, 'Andrew', 'Harris', 'andrewh@example.com', '555-567-0123', '1212 Dogwood Ln, Atlanta, GA 30301');

-- Associate Owners with Properties
INSERT INTO PropertyOwner (property_id, owner_id, ownership_percentage) VALUES
(1, 1, 100.00),
(2, 2, 100.00),
(3, 3, 100.00),
(4, 4, 60.00),
(4, 5, 40.00),
(5, 5, 50.00),
(5, 6, 50.00),
(6, 6, 100.00),
(7, 7, 100.00),
(8, 8, 70.00),
(8, 9, 30.00),
(9, 9, 100.00),
(10, 10, 50.00),
(10, 11, 50.00),
(11, 11, 100.00),
(12, 12, 100.00),
(13, 13, 80.00),
(13, 14, 20.00),
(14, 14, 100.00),
(15, 15, 100.00);

-- Insert Tenants
INSERT INTO Tenant (tenant_id, first_name, last_name, email, phone, employer, emergency_contact) VALUES
(1, 'Alice', 'Johnson', 'alicej@example.com', '555-111-2222', 'TechCorp Inc.', '555-333-4444'),
(2, 'Brian', 'Smith', 'brians@example.com', '555-222-3333', 'HealthCare Solutions', '555-444-5555'),
(3, 'Catherine', 'Williams', 'catherinew@example.com', '555-333-4444', 'EduTech Ltd.', '555-555-6666'),
(4, 'Daniel', 'Brown', 'danielb@example.com', '555-444-5555', 'FinanceCo', '555-666-7777'),
(5, 'Emma', 'Davis', 'emmad@example.com', '555-555-6666', 'RetailHub', '555-777-8888'),
(6, 'Frank', 'Miller', 'frankm@example.com', '555-666-7777', 'Logistics Inc.', '555-888-9999'),
(7, 'Grace', 'Wilson', 'gracew@example.com', '555-777-8888', 'AutoWorks', '555-999-0000'),
(8, 'Henry', 'Moore', 'henrym@example.com', '555-888-9999', 'MarketingPros', '555-000-1111'),
(9, 'Isabel', 'Taylor', 'isabelt@example.com', '555-999-0000', 'MediaHouse', '555-111-2222'),
(10, 'Jack', 'Anderson', 'jacka@example.com', '555-000-1111', 'City Bank', '555-222-3333'),
(11, 'Karen', 'Thomas', 'karent@example.com', '555-111-2223', 'GreenEnergy', '555-333-4445'),
(12, 'Leo', 'Hernandez', 'leoh@example.com', '555-222-3334', 'FoodMarket', '555-444-5556'),
(13, 'Mia', 'Jackson', 'miaj@example.com', '555-333-4445', 'TechSolutions', '555-555-6667'),
(14, 'Nathan', 'White', 'nathanw@example.com', '555-444-5556', 'GovServices', '555-666-7778'),
(15, 'Olivia', 'Harris', 'oliviah@example.com', '555-555-6667', 'RealEstate LLC', '555-777-8889');

-- Insert Leases
INSERT INTO Lease (lease_id, property_id, tenant_id, start_date, end_date, monthly_rent, security_deposit, lease_status) VALUES
(1, 2, 1, '2023-01-01', '2023-12-31', 1800.00, 3600.00, 'Active'),
(2, 3, 2, '2022-06-15', '2023-06-14', 2200.00, 4400.00, 'Expired'),
(3, 6, 3, '2024-02-01', '2025-01-31', 2000.00, 4000.00, 'Active'),
(4, 7, 4, '2023-08-01', '2024-07-31', 1500.00, 3000.00, 'Active'),
(5, 8, 5, '2021-05-01', '2022-04-30', 3200.00, 6400.00, 'Expired'),
(6, 10, 6, '2022-09-01', '2023-08-31', 1950.00, 3900.00, 'Expired'),
(7, 11, 7, '2024-03-01', '2025-02-28', 2500.00, 5000.00, 'Active'),
(8, 12, 8, '2023-07-01', '2024-06-30', 1600.00, 3200.00, 'Active'),
(9, 14, 9, '2022-02-01', '2023-01-31', 2800.00, 5600.00, 'Expired'),
(10, 15, 10, '2023-10-01', '2024-09-30', 2400.00, 4800.00, 'Active'),

-- Commercial Properties (Multiple Tenants)
(11, 5, 11, '2022-01-01', '2024-12-31', 5000.00, 10000.00, 'Active'),
(12, 5, 12, '2023-03-01', '2025-02-28', 7000.00, 14000.00, 'Active'),
(13, 9, 13, '2021-06-01', '2023-05-31', 8000.00, 16000.00, 'Expired'),
(14, 9, 14, '2022-07-01', '2024-06-30', 9000.00, 18000.00, 'Active'),
(15, 13, 15, '2023-05-01', '2024-04-30', 7200.00, 14400.00, 'Active'),
(16, 13, 3, '2022-09-01', '2023-08-31', 6200.00, 12400.00, 'Expired'),

-- Additional Residential Leases
(17, 4, 4, '2021-04-01', '2023-03-31', 2900.00, 5800.00, 'Expired'),
(18, 7, 6, '2024-01-15', '2025-01-14', 1800.00, 3600.00, 'Active'),
(19, 10, 8, '2023-06-01', '2024-05-31', 2000.00, 4000.00, 'Active'),
(20, 11, 9, '2022-08-01', '2023-07-31', 2300.00, 4600.00, 'Expired');

-- Insert Employees 
INSERT INTO Employee (employee_id, first_name, last_name, email, phone, role, hire_date) VALUES
(1, 'John', 'Doe', 'johndoe@example.com', '555-101-2020', 'Property Manager', '2018-06-15'),
(2, 'Jane', 'Smith', 'janesmith@example.com', '555-102-3030', 'Leasing Agent', '2019-09-10'),
(3, 'Michael', 'Johnson', 'michaelj@example.com', '555-103-4040', 'Maintenance Staff', '2020-01-20'),
(4, 'Emily', 'Davis', 'emilyd@example.com', '555-104-5050', 'Accountant', '2017-03-05'),
(5, 'David', 'Martinez', 'davidm@example.com', '555-105-6060', 'Property Manager', '2016-07-11'),
(6, 'Sarah', 'Brown', 'sarahb@example.com', '555-106-7070', 'Leasing Agent', '2021-05-22'),
(7, 'James', 'Wilson', 'jamesw@example.com', '555-107-8080', 'Maintenance Staff', '2022-08-19'),
(8, 'Jessica', 'Taylor', 'jessicat@example.com', '555-108-9090', 'Accountant', '2015-12-15'),
(9, 'Christopher', 'Anderson', 'chrisand@example.com', '555-109-1111', 'Property Manager', '2019-04-25'),
(10, 'Amanda', 'Thomas', 'amandat@example.com', '555-110-2222', 'Leasing Agent', '2023-02-18'),
(11, 'Matthew', 'Hernandez', 'matth@example.com', '555-111-3333', 'Maintenance Staff', '2018-09-30'),
(12, 'Ashley', 'Moore', 'ashleym@example.com', '555-112-4444', 'Accountant', '2020-06-14'),
(13, 'Daniel', 'Jackson', 'danielj@example.com', '555-113-5555', 'Property Manager', '2017-11-08'),
(14, 'Elizabeth', 'White', 'elizabethw@example.com', '555-114-6666', 'Leasing Agent', '2022-01-10'),
(15, 'Andrew', 'Harris', 'andrewh@example.com', '555-115-7777', 'Maintenance Staff', '2019-07-07'),
(16, 'Megan', 'Clark', 'meganc@example.com', '555-116-8888', 'Accountant', '2021-09-15'),
(17, 'Joshua', 'Rodriguez', 'joshuar@example.com', '555-117-9999', 'Property Manager', '2016-05-21'),
(18, 'Hannah', 'Lewis', 'hannahl@example.com', '555-118-0000', 'Leasing Agent', '2020-10-30'),
(19, 'Ryan', 'Walker', 'ryanw@example.com', '555-119-1212', 'Maintenance Staff', '2023-03-12'),
(20, 'Sophia', 'Hall', 'sophiah@example.com', '555-120-1313', 'Accountant', '2019-12-05');

-- Insert Payments
INSERT INTO Payment (payment_id, lease_id, amount, payment_date, payment_method, received_by) VALUES
(1, 1, 1800.00, '2024-01-01', 'Bank Transfer', 4),
(2, 2, 2200.00, '2024-01-15', 'Credit Card', 8),
(3, 3, 2000.00, '2024-02-01', 'Check', 12),
(4, 4, 1500.00, '2024-02-05', 'Cash', 16),
(5, 5, 6400.00, '2024-01-10', 'Bank Transfer', 20),  -- Security deposit
(6, 6, 1950.00, '2024-01-20', 'Check', 4),
(7, 7, 2500.00, '2024-03-01', 'Credit Card', 8),
(8, 8, 3200.00, '2024-03-05', 'Bank Transfer', 12),
(9, 9, 2800.00, '2024-02-10', 'Cash', 16),
(10, 10, 4800.00, '2024-02-15', 'Check', 20), -- Security deposit
(11, 11, 5000.00, '2024-01-01', 'Bank Transfer', 4),
(12, 12, 7000.00, '2024-01-15', 'Credit Card', 8),
(13, 13, 8000.00, '2024-02-01', 'Check', 12),
(14, 14, 9000.00, '2024-02-05', 'Cash', 16),
(15, 15, 14400.00, '2024-01-10', 'Bank Transfer', 20);  -- Security deposit

-- Insert Maintenance Requests
INSERT INTO MaintenanceRequest (request_id, property_id, tenant_id, employee_id, description, request_date, completion_date, status) VALUES
(1, 2, 1, 3, 'Leaking kitchen faucet needs repair.', '2024-01-10', '2024-01-12', 'Completed'),
(2, 3, 2, 7, 'HVAC system not working properly.', '2024-01-15', NULL, 'In Progress'),
(3, 6, 3, 11, 'Broken window in living room.', '2024-02-01', NULL, 'Open'),
(4, 7, 4, 15, 'Power outage in one of the bedrooms.', '2024-02-05', '2024-02-07', 'Completed'),
(5, 8, 5, 3, 'Clogged bathtub drain.', '2024-02-10', NULL, 'In Progress'),
(6, 10, 6, 7, 'Heating system making loud noises.', '2024-01-20', '2024-01-23', 'Completed'),
(7, 11, 7, 11, 'Leaking roof after heavy rain.', '2024-02-02', NULL, 'Open'),
(8, 12, 8, 15, 'Pest infestation in kitchen.', '2024-01-30', '2024-02-02', 'Completed'),
(9, 14, 9, 3, 'Front door lock is jammed.', '2024-02-08', NULL, 'In Progress'),
(10, 15, 10, 7, 'Water heater not producing hot water.', '2024-01-25', '2024-01-28', 'Completed'),
(11, 4, 4, 11, 'Mold issue in bathroom.', '2024-02-01', NULL, 'Open'),
(12, 7, 6, 15, 'Broken garage door motor.', '2024-01-18', '2024-01-20', 'Completed'),
(13, 10, 8, 3, 'Dishwasher not draining properly.', '2024-02-05', NULL, 'In Progress'),
(14, 11, 9, 7, 'Ceiling fan making loud noises.', '2024-02-10', NULL, 'Open'),
(15, 8, 5, 11, 'Cracked tile in bathroom.', '2024-01-15', '2024-01-17', 'Completed');



-- 4. Create Indexes

-- Creating an index on the "Property" table for the "city" and "zip_code" columns
-- This helps speed up searches and filters based on city and zip code, which are commonly used in queries.
CREATE INDEX idx_property_location
ON Property(city, zip_code);

-- Creating an index on the "Tenant" table for the "email" and "phone" columns
-- This allows for faster lookups of tenants by their contact information.
CREATE INDEX idx_tenant_contact
ON Tenant(email, phone);

-- Creating an index on the "Owner" table for the "email" and "phone" columns
-- Similar to tenants, this index optimizes owner lookups based on their contact details.
CREATE INDEX idx_owner_contact
ON Owner(email, phone);

-- Creating an index on the "Lease" table for the "lease_status" and "end_date" columns
-- This improves query performance when filtering leases by status (e.g., active, terminated) or lease end date.
CREATE INDEX idx_lease_status
ON Lease(lease_status, end_date);

-- Creating an index on the "MaintenanceRequest" table for the "status" column
-- This speeds up queries that check for open or completed maintenance requests.
CREATE INDEX idx_maintenance_status
ON MaintenanceRequest(status);

-- Creating an index on the "Payment" table for the "payment_date" column
-- This improves performance for queries related to rent payment reports based on date.
CREATE INDEX idx_payment_date
ON Payment(payment_date);



-- 5. Create Views

-- Creating a view to list active leases along with tenant and property details
-- This provides an easy-to-query summary of active rental agreements, including monthly rent and lease dates.
CREATE VIEW ActiveLeases AS
SELECT
  l.lease_id, 
  p.address, 
  CONCAT(t.first_name, ' ', t.last_name) AS tenant_name, -- Concatenates first and last name for readability
  l.monthly_rent, 
  l.start_date, 
  l.end_date
FROM Lease l
JOIN Property p ON l.property_id = p.property_id
JOIN Tenant t ON l.tenant_id = t.tenant_id
WHERE l.lease_status = 'Active'; -- Filters to only include active leases


-- Creating a view for open maintenance requests with assigned employee details
-- This helps track unresolved maintenance requests and who is responsible for them.
CREATE VIEW OpenMaintenanceRequests AS
SELECT
  mr.request_id, 
  p.address, 
  IFNULL(CONCAT(e.first_name, ' ', e.last_name), 'Unassigned') AS assigned_to, -- Shows 'Unassigned' if no employee is assigned
  mr.description, 
  mr.request_date
FROM MaintenanceRequest mr
JOIN Property p ON mr.property_id = p.property_id
LEFT JOIN Employee e ON mr.employee_id = e.employee_id -- Uses LEFT JOIN since some requests may not have an assigned employee
WHERE mr.status = 'Open'; -- Filters to only include open maintenance requests


-- Creating a view to summarize financial performance per property
-- This aggregates total rent collected and maintenance costs for each property.
CREATE VIEW FinancialSummary AS
SELECT
  p.property_id, 
  p.address,
  IFNULL(SUM(pay.amount), 0) AS total_rent, -- Ensures NULL values are replaced with 0 to avoid incorrect calculations
  IFNULL(SUM(mr.cost), 0) AS total_maintenance_cost -- Ensures NULL values are replaced with 0
FROM Property p
LEFT JOIN Lease l ON p.property_id = l.property_id
LEFT JOIN Payment pay ON l.lease_id = pay.lease_id
LEFT JOIN MaintenanceRequest mr ON p.property_id = mr.property_id
GROUP BY p.property_id, p.address; -- Groups the data by property to provide financial totals per property


-- SELECT * FROM FinancialSummary;


-- 6. Create Temporary Table

-- Creating a temporary table "MonthlyRentRoll" to store rent-related data
-- This table is session-scoped, meaning it only exists for the duration of the session
-- and will be automatically deleted when the session ends.
CREATE TEMPORARY TABLE MonthlyRentRoll (
  property_id INT,         -- ID of the property
  address VARCHAR(255),    -- Address of the property
  expected_rent DECIMAL(10,2), -- Total expected rent for the month
  received_rent DECIMAL(10,2)  -- Total received rent for the month
);

-- Populating the temporary table with rent roll data
-- This query calculates the expected rent (sum of monthly rents for active leases)
-- and the received rent (sum of payments made) per property.
INSERT INTO MonthlyRentRoll (property_id, address, expected_rent, received_rent)
SELECT
  p.property_id, 
  p.address, 
  IFNULL(SUM(l.monthly_rent), 0) AS expected_rent, -- Avoids NULL values by defaulting to 0
  IFNULL(SUM(pay.amount), 0) AS received_rent      -- Avoids NULL values by defaulting to 0
FROM Property p
JOIN Lease l ON p.property_id = l.property_id
LEFT JOIN Payment pay ON l.lease_id = pay.lease_id -- Left join allows for properties with no payments
WHERE l.lease_status = 'Active' -- Filters only active leases
GROUP BY p.property_id, p.address;

-- Uncomment the following line to view the contents of the temporary table
-- SELECT * FROM MonthlyRentRoll;


-- 7. Create Triggers

-- Trigger: Automatically update lease status to 'Expired' when the end date is past
DELIMITER $$

CREATE TRIGGER trg_lease_status_update
BEFORE UPDATE ON Lease  -- This trigger runs before an UPDATE operation on the Lease table
FOR EACH ROW  -- Ensures the trigger runs for each row being updated
BEGIN
  -- Check if the new end_date value is before the current date/time
  IF NEW.end_date < NOW() THEN
    -- If the lease's end date is in the past, update the lease_status to 'Expired'
    SET NEW.lease_status = 'Expired';
  END IF;
END $$

DELIMITER ;


-- Trigger: Log late payments into the PaymentAudit table
DELIMITER $$  

CREATE TRIGGER trg_late_payment  
AFTER INSERT ON Payment  
FOR EACH ROW  
BEGIN  
  DECLARE lease_due_day INT;  -- Variable to store the due day of the lease
  DECLARE lease_due_date DATE;  -- Variable to store the calculated due date

  -- Fetch the due_day from the Lease table corresponding to the payment's lease_id
  SELECT due_day INTO lease_due_day FROM Lease WHERE lease_id = NEW.lease_id;  

  -- Calculate the expected due date based on the lease's due_day and the payment date's year and month
  SET lease_due_date = STR_TO_DATE(  
    CONCAT(YEAR(NEW.payment_date), '-', MONTH(NEW.payment_date), '-', lease_due_day),  
    '%Y-%m-%d'  
  );  

  -- If the payment date is after the due date, log it as a late payment in the PaymentAudit table
  IF NEW.payment_date > lease_due_date THEN  
    INSERT INTO PaymentAudit (payment_id, late_fee, audit_timestamp)  
    VALUES (NEW.payment_id, NEW.amount * 0.1, CURRENT_TIMESTAMP); -- Apply a 10% late fee
  END IF;  
END$$  

DELIMITER ;  

-- Example Insert: Insert a payment (this may trigger the late payment audit)
-- INSERT INTO Payment (lease_id, amount, payment_date, payment_method)  
-- VALUES (1, 1800.00, '2024-02-05', 'Bank Transfer');  

-- Uncomment the following line to check the PaymentAudit table for late payments
-- SELECT * FROM PaymentAudit;



-- 8. Create Stored Procedures

-- Procedure: Add New Lease with Validation
DELIMITER $$

CREATE PROCEDURE AddLease(
  IN p_property_id INT,       -- Property ID for the lease
  IN p_tenant_id INT,         -- Tenant ID for the lease
  IN p_start_date DATE,       -- Start date of the lease
  IN p_end_date DATE,         -- End date of the lease
  IN p_monthly_rent DECIMAL(10,2)  -- Monthly rent amount for the lease
)
BEGIN
  DECLARE lease_count INT;    -- Variable to store the number of overlapping leases

  -- Check for overlapping leases on the same property within the given start and end dates
  SELECT COUNT(*) INTO lease_count
  FROM Lease
  WHERE property_id = p_property_id
  AND (p_start_date BETWEEN start_date AND end_date);

  -- If there are overlapping leases, raise an error with a custom message
  IF lease_count > 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Property is already leased during this period';
  ELSE
    -- If no overlapping leases are found, insert the new lease into the Lease table
    INSERT INTO Lease (property_id, tenant_id, start_date, end_date, monthly_rent, lease_status)
    VALUES (p_property_id, p_tenant_id, p_start_date, p_end_date, p_monthly_rent, 'Active');
  END IF;
END$$

DELIMITER ;


-- Procedure: Process Monthly Rent Payment
DELIMITER $$

CREATE PROCEDURE ProcessRentPayment(
  IN p_lease_id INT,         -- Lease ID for which the rent payment is being made
  IN p_amount DECIMAL(10,2), -- Amount of the payment
  IN p_payment_method VARCHAR(20)  -- Payment method (e.g., 'Bank Transfer', 'Credit Card', etc.)
)
BEGIN
  -- Insert the rent payment record into the Payment table
  INSERT INTO Payment (lease_id, amount, payment_date, payment_method)
  VALUES (p_lease_id, p_amount, CURDATE(), p_payment_method);

  -- Update the last payment date for the lease in the Lease table
  UPDATE Lease
  SET last_payment_date = CURDATE()
  WHERE lease_id = p_lease_id;
END$$

DELIMITER ;


-- Procedure: Calculate Owner Payout
DELIMITER $$

CREATE PROCEDURE CalculateOwnerPayout(IN p_property_id INT)
BEGIN
  -- Calculate the total payout to each owner based on the ownership percentage and active leases
  SELECT
    CONCAT(o.first_name, ' ', o.last_name) AS owner_name,   -- Concatenate first and last name of the owner
    SUM(l.monthly_rent * po.ownership_percentage / 100) AS payout -- Calculate payout based on ownership percentage
  FROM PropertyOwner po
  JOIN Owner o ON po.owner_id = o.owner_id        -- Join PropertyOwner and Owner tables to get the owner's information
  JOIN Lease l ON po.property_id = l.property_id  -- Join Lease table to get the active leases for the property
  WHERE po.property_id = p_property_id            -- Filter by the given property_id
    AND l.lease_status = 'Active'                  -- Only consider active leases
  GROUP BY o.owner_id;                             -- Group the result by owner_id to get individual payouts
END$$

DELIMITER ;


-- Example call to the CalculateOwnerPayout procedure for property ID 5
-- CALL CalculateOwnerPayout(5);


-- 9. Create Function

-- Function: Check Lease Overlap
DELIMITER $$  

CREATE FUNCTION CheckLeaseOverlap(  
  p_property_id INT,        -- Property ID for which lease overlap is being checked
  p_start_date DATE,        -- Start date of the lease to check for overlap
  p_end_date DATE,          -- End date of the lease to check for overlap
  p_ignore_expired BOOLEAN  -- Flag to ignore expired leases during overlap check
) RETURNS INT                -- The function returns an integer (1 if overlap exists, 0 if not)
DETERMINISTIC                -- The function will always return the same result for the same inputs
BEGIN  
  DECLARE overlap_count INT;  -- Variable to store the number of overlapping leases

  -- Select the count of leases that overlap with the given start and end dates for the specified property
  SELECT COUNT(*)  
  INTO overlap_count  
  FROM Lease  
  WHERE  
    property_id = p_property_id  -- Filter by the property ID
    AND (p_start_date <= end_date AND p_end_date >= start_date)  -- Check if the dates overlap with existing leases' dates
    -- Conditionally filter leases based on their status and the flag p_ignore_expired
    AND (  
      (p_ignore_expired AND lease_status = 'Active')  -- If p_ignore_expired is TRUE, include only active leases
      OR NOT p_ignore_expired                          -- If p_ignore_expired is FALSE, include all leases (active and expired)
    );  

  -- Return 1 if overlap_count is greater than 0 (indicating overlap), otherwise return 0 (no overlap)
  RETURN IF(overlap_count > 0, 1, 0);  
END$$  

DELIMITER ;  

-- Example queries to check for lease overlaps with different conditions

-- Check for overlaps with only active leases (ignores expired leases)
SELECT CheckLeaseOverlap(5, '2024-01-01', '2024-12-31', TRUE) AS OverlapExists;  

-- Check for overlaps with all leases (includes expired leases as well)
SELECT CheckLeaseOverlap(5, '2024-01-01', '2024-12-31', FALSE) AS OverlapExists;  


-- 10. Complex Queries

-- Query 1: Calculate Owner Payouts and Rank Owners by Total Payout

WITH OwnerPayouts AS (
  -- This CTE (Common Table Expression) calculates the total payout for each owner based on their ownership percentage.
  SELECT
    o.owner_id,  -- Owner's ID
    CONCAT(o.first_name, ' ', o.last_name) AS owner_name,  -- Full name of the owner
    SUM(l.monthly_rent * (po.ownership_percentage / 100)) AS total_payout  -- Total payout calculated based on ownership percentage
  FROM PropertyOwner po
  JOIN Owner o ON po.owner_id = o.owner_id  -- Join PropertyOwner to Owner to get owner details
  JOIN Lease l ON po.property_id = l.property_id  -- Join Lease to PropertyOwner to get lease details
  WHERE l.lease_status = 'Active'  -- Only include active leases
  GROUP BY o.owner_id  -- Group by owner to aggregate the payout for each owner
)

-- Main query to retrieve owner name, total payout, rank by payout, and contribution percentage
SELECT
  owner_name,  -- Owner's full name
  total_payout,  -- Total payout for the owner
  RANK() OVER (ORDER BY total_payout DESC) AS payout_rank,  -- Rank owners by total payout in descending order
  ROUND((total_payout / SUM(total_payout) OVER ()) * 100, 2) AS contribution_percent  -- Calculate each owner's percentage contribution to the total payouts
FROM OwnerPayouts;  -- Use the CTE results to generate the final output

-- Query 2: Calculate Property Maintenance Requests and Compare to City Average

WITH PropertyRequests AS (
  -- This CTE calculates the number of open maintenance requests for each property.
  SELECT
    p.property_id,  -- Property ID
    p.address,  -- Property address
    p.city,  -- Property city
    COUNT(mr.request_id) AS property_requests  -- Count the number of open maintenance requests for each property
  FROM Property p
  LEFT JOIN MaintenanceRequest mr ON p.property_id = mr.property_id  -- Left join to MaintenanceRequest to include properties with no open requests
  WHERE mr.status = 'Open'  -- Only include open maintenance requests
  GROUP BY p.property_id, p.city, p.address  -- Group by property details to aggregate the request count per property
)

-- Main query to retrieve property details and compare with the average number of requests for the city
SELECT
  pr.address,  -- Property address
  pr.city,  -- Property city
  pr.property_requests,  -- Number of open maintenance requests for the property
  (SELECT AVG(property_requests)  -- Subquery to calculate the average number of open maintenance requests for properties in the same city
   FROM PropertyRequests 
   WHERE city = pr.city) AS city_avg_requests  -- Only compare to properties in the same city
FROM PropertyRequests pr;  -- Use the CTE results to generate the final output

-- Query 3: Identify Overlapping or Consecutive Leases for a Property

SELECT
  property_id,  -- The ID of the property
  tenant_id,  -- The tenant currently leasing the property
  end_date AS current_lease_end,  -- The end date of the current lease
  LEAD(start_date) OVER (  -- Get the start date of the next lease for the same property
    PARTITION BY property_id  -- Ensure the window function operates within each property
    ORDER BY start_date  -- Sort leases by start date to find the next lease
  ) AS next_lease_start
FROM Lease
WHERE lease_status = 'Active';  -- Only consider active leases

-- Explanation:
-- This query helps identify gaps or overlaps between leases for the same property.
-- The LEAD() function retrieves the start date of the next lease (if any) for each property.
-- If the next lease start date is after the current lease end date, there's a vacancy period.


-- Query 4: Year-Over-Year (YoY) Rent Growth for Each Property

SELECT
  property_id,  -- The ID of the property
  YEAR(start_date) AS year,  -- Extract the lease start year
  MONTH(start_date) AS month,  -- Extract the lease start month
  monthly_rent,  -- Monthly rent amount for the current lease
  LAG(monthly_rent, 12) OVER (  -- Get the monthly rent from 12 months ago (previous year)
    PARTITION BY property_id  -- Ensure the window function operates within each property
    ORDER BY start_date  -- Order by lease start date to track rent changes over time
  ) AS prev_year_rent,
  (monthly_rent - LAG(monthly_rent, 12) OVER (PARTITION BY property_id ORDER BY start_date)) /
  LAG(monthly_rent, 12) OVER (PARTITION BY property_id ORDER BY start_date) * 100 AS yoy_growth  -- Calculate the percentage change in rent
FROM Lease;

-- Explanation:
-- This query calculates the year-over-year (YoY) rent growth for each property.
-- The LAG() function retrieves the monthly rent from 12 months ago for comparison.
-- The percentage change formula [(current - previous) / previous] * 100 determines the growth rate.
-- If there's no prior year rent available, the YoY growth will be NULL.


-- Query 5: Categorize Active Leases into Rent Quartiles

SELECT
  property_id,  -- The ID of the property
  address,  -- The address of the property
  monthly_rent,  -- Monthly rent amount
  NTILE(4) OVER (ORDER BY monthly_rent DESC) AS rent_quartile  -- Divide the rents into 4 quartiles, ranked from highest to lowest
FROM Lease
JOIN Property USING (property_id)  -- Join with Property table to get the address
WHERE lease_status = 'Active';  -- Only include active leases

-- Explanation:
-- This query categorizes active leases into quartiles based on monthly rent.
-- The NTILE(4) function divides the rent data into four equal groups:
--   - Quartile 1: Top 25% highest rents
--   - Quartile 2: 25-50% range
--   - Quartile 3: 50-75% range
--   - Quartile 4: Bottom 25% lowest rents
-- This helps in analyzing rental price distribution among properties.



-- Query 6: Identify the Oldest Open Maintenance Request per Property

WITH RankedRequests AS (
  SELECT
    property_id,  -- The ID of the property where the maintenance request was made
    request_id,  -- The unique ID of the maintenance request
    description,  -- Description of the maintenance issue
    request_date,  -- Date the maintenance request was submitted
    ROW_NUMBER() OVER (  -- Assigns a rank to each request within the same property
      PARTITION BY property_id  -- Resets the numbering for each property
      ORDER BY request_date  -- Orders requests by date, with the earliest request ranked first
    ) AS request_rank
  FROM MaintenanceRequest
  WHERE status = 'Open'  -- Only consider open maintenance requests
)
SELECT *
FROM RankedRequests
WHERE request_rank = 1;  -- Select only the oldest open maintenance request per property

-- Explanation:
-- This query finds the **oldest open maintenance request** for each property.
-- The `ROW_NUMBER()` function assigns a rank to each request based on `request_date`.
-- The `WHERE request_rank = 1` ensures only the first-ranked request per property is retrieved.


-- Query 7: Calculate Property Occupancy Rate

SELECT
  property_id,  -- The ID of the property
  address,  -- The address of the property
  SUM(DATEDIFF(end_date, start_date)) AS total_occupied_days,  -- Sum of all lease durations for the property
  (SUM(DATEDIFF(end_date, start_date)) / 365) * 100 AS occupancy_rate_percent  -- Convert to percentage based on a 365-day year
FROM Lease
JOIN Property USING (property_id)  -- Join with Property table to get the address
GROUP BY property_id, address;  -- Group results by property

-- Explanation:
-- This query calculates the **total occupied days** for each property based on its lease durations.
-- The `DATEDIFF(end_date, start_date)` calculates the length of each lease in days.
-- The occupancy rate is derived by dividing the total occupied days by 365 and converting to a percentage.
-- This helps evaluate how well properties are leased throughout the year.


-- Query 8: Track Running Total of Tenant Payments

SELECT
  t.tenant_id,  -- The ID of the tenant
  CONCAT(t.first_name, ' ', t.last_name) AS tenant_name,  -- Full name of the tenant
  p.payment_date,  -- Date the payment was made
  p.amount,  -- Payment amount
  SUM(p.amount) OVER (
    PARTITION BY t.tenant_id  -- Resets the running total for each tenant
    ORDER BY p.payment_date  -- Orders payments by date to accumulate in chronological order
  ) AS running_total_paid  -- Running total of all payments made by the tenant
FROM Payment p
JOIN Lease l ON p.lease_id = l.lease_id  -- Link payments to the leases they belong to
JOIN Tenant t ON l.tenant_id = t.tenant_id;  -- Link leases to tenants

-- Explanation:
-- This query calculates the **running total of payments** made by each tenant over time.
-- The `SUM()` window function accumulates payments **chronologically** for each tenant.
-- This helps track payment history and identify any payment trends or inconsistencies.



-- Query 9: Calculate Rolling Average of Maintenance Costs for Each Property

SELECT
  p.address,  -- Property address
  mr.request_date,  -- Date when the maintenance request was submitted
  mr.cost,  -- Cost of the maintenance request
  AVG(mr.cost) OVER (  -- Calculate the rolling average maintenance cost
    PARTITION BY mr.property_id  -- Perform calculation separately for each property
    ORDER BY mr.request_date  -- Order by request date to maintain chronological order
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW  -- Include the current row and the two previous rows
  ) AS rolling_avg_cost  -- Rolling average maintenance cost for recent 3 requests
FROM MaintenanceRequest mr
JOIN Property p ON mr.property_id = p.property_id;  -- Join to get property address

-- Explanation:
-- This query calculates a **rolling average of maintenance costs** for each property.
-- The window function `AVG()` calculates the **average cost** for the **current and previous two requests**.
-- This provides insight into how maintenance costs fluctuate over time for each property.
-- The `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` ensures that the average includes at most three records (current + two previous).


-- Query 10: Calculate Tenant Lease Renewal Rate

WITH LeaseRenewals AS (
  SELECT
    tenant_id,  -- The tenant's unique ID
    COUNT(*) AS total_leases,  -- Total number of leases the tenant has had
    SUM(CASE WHEN end_date > start_date THEN 1 ELSE 0 END) AS renewed_leases  -- Count of renewed leases
  FROM Lease
  GROUP BY tenant_id  -- Aggregate lease data per tenant
)
SELECT
  tenant_id,  -- The tenant's unique ID
  CONCAT(t.first_name, ' ', t.last_name) AS tenant_name,  -- Full name of the tenant
  ROUND((renewed_leases / total_leases) * 100, 2) AS renewal_rate  -- Calculate renewal rate as a percentage
FROM LeaseRenewals
JOIN Tenant t USING (tenant_id);  -- Join with Tenant table to get tenant names

-- Explanation:
-- This query determines the **lease renewal rate** for each tenant.
-- The `LeaseRenewals` CTE calculates the **total leases** and **renewed leases** for each tenant.
-- A lease is considered **renewed** if its `end_date` is after its `start_date`.
-- The final query calculates the **renewal rate** by dividing renewed leases by total leases and converting it to a percentage.
-- This helps in understanding tenant retention and renewal behavior.


-- Query 11: Calculate Annual Rent Yield for Each Property

SELECT
  p.address,  -- Property address
  p.purchase_price,  -- Original purchase price of the property
  SUM(l.monthly_rent * 12) AS annual_rent,  -- Total annual rent collected from active leases
  ROUND((SUM(l.monthly_rent * 12) / p.purchase_price) * 100, 2) AS rent_yield_percent  -- Calculate rental yield percentage
FROM Lease l
JOIN Property p ON l.property_id = p.property_id  -- Join Lease with Property table to get purchase price
WHERE l.lease_status = 'Active'  -- Consider only active leases
GROUP BY p.property_id, p.address, p.purchase_price;

-- Explanation:
-- This query calculates the **annual rental yield** for each property.
-- The rental yield is computed as: **(Annual Rent / Purchase Price) * 100**.
-- The formula helps investors assess how much return they get from rental income relative to property value.
-- The `ROUND()` function ensures the result is formatted to **two decimal places**.


-- Query 12: Rank Properties by Number of Open Maintenance Requests

SELECT
  p.address,  -- Property address
  COUNT(mr.request_id) AS open_requests,  -- Count of open maintenance requests per property
  RANK() OVER (ORDER BY COUNT(mr.request_id) DESC) AS request_rank  -- Rank properties based on the number of open requests
FROM MaintenanceRequest mr
JOIN Property p ON mr.property_id = p.property_id  -- Join with Property table to get address
WHERE mr.status = 'Open'  -- Consider only open maintenance requests
GROUP BY p.property_id, p.address;

-- Explanation:
-- This query **ranks properties** based on the number of **open maintenance requests**.
-- The `COUNT()` function determines the total open requests per property.
-- The `RANK()` function assigns a rank, ordering properties **from highest to lowest** open requests.
-- This helps property managers identify properties that need urgent maintenance attention.


-- Query 13: Calculate Each Owner's Total Portfolio Value

SELECT
  o.owner_id,  -- Unique ID of the owner
  CONCAT(o.first_name, ' ', o.last_name) AS owner_name,  -- Full name of the owner
  SUM(p.purchase_price * (po.ownership_percentage / 100)) AS portfolio_value  -- Calculate the owner's share of property value
FROM PropertyOwner po
JOIN Owner o ON po.owner_id = o.owner_id  -- Join to get owner details
JOIN Property p ON po.property_id = p.property_id  -- Join to get property purchase prices
GROUP BY o.owner_id;

-- Explanation:
-- This query calculates **each owner's total portfolio value**.
-- Since properties can have multiple owners with different ownership percentages, the total value is computed as:
-- **(Property Purchase Price * Ownership Percentage)**
-- The `SUM()` function aggregates the values across multiple properties.
-- This helps owners understand their total property investment value.



-- Query 14: Calculate Overdue Days for Tenant Payments

SELECT
  t.tenant_id,  -- Unique ID of the tenant
  CONCAT(t.first_name, ' ', t.last_name) AS tenant_name,  -- Full name of the tenant
  p.payment_date,  -- Actual payment date
  DATE_FORMAT(p.payment_date, '%Y-%m') AS payment_month,  -- Extract year and month from the payment date
  -- Construct the due_date using the stored due_day from the Lease table
  DATE_FORMAT(p.payment_date, '%Y-%m-') || LPAD(l.due_day, 2, '0') AS due_date,
  -- Calculate the number of days the payment was overdue
  DATEDIFF(p.payment_date, DATE_FORMAT(p.payment_date, '%Y-%m-') || LPAD(l.due_day, 2, '0')) AS days_overdue
FROM Payment p
JOIN Lease l ON p.lease_id = l.lease_id  -- Join with Lease table to get due_day for each lease
JOIN Tenant t ON l.tenant_id = t.tenant_id  -- Join with Tenant table to get tenant details
WHERE p.payment_date > DATE_FORMAT(p.payment_date, '%Y-%m-') || LPAD(l.due_day, 2, '0');  -- Filter for overdue payments

-- Explanation:
-- This query determines how late a tenant's payment is by computing the **days overdue**.
-- The `due_date` is derived dynamically by taking the **year and month** from `payment_date` and appending the `due_day` from the `Lease` table.
-- The `DATEDIFF()` function calculates the number of days between the **actual payment date** and the **calculated due date**.
-- This helps landlords track overdue payments and potential late fees.
-- **Note**: The `||` operator used for string concatenation might not work in some SQL flavors like MySQL, where `CONCAT()` should be used instead.


-- Query 15: Allocate Maintenance Costs to Property Owners Based on Ownership Percentage

SELECT
  o.owner_id,  -- Unique ID of the owner
  CONCAT(o.first_name, ' ', o.last_name) AS owner_name,  -- Full name of the owner
  -- Allocate maintenance costs based on ownership percentage
  SUM(mr.cost * (po.ownership_percentage / 100)) AS allocated_cost
FROM MaintenanceRequest mr
JOIN Property p ON mr.property_id = p.property_id  -- Join with Property table to get property details
JOIN PropertyOwner po ON p.property_id = po.property_id  -- Join with PropertyOwner to determine ownership percentage
JOIN Owner o ON po.owner_id = o.owner_id  -- Join with Owner table to get owner details
GROUP BY o.owner_id;

-- Explanation:
-- This query calculates how much of the **maintenance cost** each property owner is responsible for.
-- Since properties can have multiple owners with different ownership percentages, the cost is distributed as:
-- **(Maintenance Cost * Ownership Percentage / 100)**
-- The `SUM()` function ensures that the total maintenance costs are correctly aggregated for each owner.
-- This helps in **fairly distributing maintenance expenses** among owners based on their stake in the property.
