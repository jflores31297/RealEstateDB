-- 1. Create Database
DROP DATABASE IF EXISTS RealEstateDB;
CREATE DATABASE RealEstateDB;
USE RealEstateDB;

-- 2. Create Tables

CREATE TABLE Property (
    property_id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    property_type ENUM('Single Family', 'Apartment', 'Commercial', 'Condo'),
    square_feet INT,
    year_built INT,
    purchase_date DATE,
    purchase_price DECIMAL(15,2)
);

CREATE TABLE Owner (
    owner_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    mailing_address VARCHAR(255)
);

CREATE TABLE Tenant (
    tenant_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    employer VARCHAR(100),
    emergency_contact VARCHAR(20)
);

CREATE TABLE Employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    role ENUM('Property Manager', 'Maintenance Staff', 'Accountant', 'Leasing Agent'),
    hire_date DATE
);

CREATE TABLE Lease (
    lease_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    tenant_id INT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    monthly_rent DECIMAL(10,2) NOT NULL,
    security_deposit DECIMAL(10,2),
    lease_status ENUM('Active', 'Expired', 'Terminated') DEFAULT 'Active',
    due_day INT NOT NULL DEFAULT 1,
    FOREIGN KEY (property_id) REFERENCES Property(property_id) ON DELETE CASCADE,
    FOREIGN KEY (tenant_id) REFERENCES Tenant(tenant_id) ON DELETE CASCADE
);

CREATE TABLE MaintenanceRequest (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    tenant_id INT,
    employee_id INT,
    description TEXT NOT NULL,
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completion_date DATE,
    status ENUM('Open', 'In Progress', 'Completed') DEFAULT 'Open',
    cost DECIMAL(10,2),
    FOREIGN KEY (property_id) REFERENCES Property(property_id) ON DELETE CASCADE,
    FOREIGN KEY (tenant_id) REFERENCES Tenant(tenant_id) ON DELETE SET NULL,
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id) ON DELETE SET NULL
);

CREATE TABLE Payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    lease_id INT,
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method ENUM('Credit Card', 'Check', 'Bank Transfer', 'Cash'),
    received_by INT,
    FOREIGN KEY (lease_id) REFERENCES Lease(lease_id) ON DELETE CASCADE,
    FOREIGN KEY (received_by) REFERENCES Employee(employee_id) ON DELETE SET NULL
);

CREATE TABLE PropertyOwner (
    property_id INT,
    owner_id INT,
    ownership_percentage DECIMAL(5,2) CHECK (ownership_percentage BETWEEN 0 AND 100),
    PRIMARY KEY (property_id, owner_id),
    FOREIGN KEY (property_id) REFERENCES Property(property_id) ON DELETE CASCADE,
    FOREIGN KEY (owner_id) REFERENCES Owner(owner_id) ON DELETE CASCADE
);

CREATE TABLE PaymentAudit (  
  audit_id INT AUTO_INCREMENT PRIMARY KEY,  
  payment_id INT,  
  late_fee DECIMAL(10,2),  
  audit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
  FOREIGN KEY (payment_id) REFERENCES Payment(payment_id)  
);  





-- Load Data

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







-- Create Indexes

-- Speed up searches by city/zip_code (common filters)
CREATE INDEX idx_property_location
ON Property(city, zip_code);

-- Optimize tenant/owner lookups by email/phone
CREATE INDEX idx_tenant_contact
ON Tenant(email, phone);

CREATE INDEX idx_owner_contact
ON Owner(email, phone);

-- Improve lease status and date filtering
CREATE INDEX idx_lease_status
ON Lease(lease_status, end_date);

-- Accelerate maintenance request status checks
CREATE INDEX idx_maintenance_status
ON MaintenanceRequest(status);

-- Speed up payment date reporting
CREATE INDEX idx_payment_date
ON Payment(payment_date);

-- Find all properties in Los Angeles  
-- SELECT * FROM Property WHERE city = 'Los Angeles';

-- Find properties in San Francisco with zip code 94103  
-- SELECT * FROM Property WHERE city = 'San Francisco' AND zip_code = '94103';  

-- Find a tenant by email  
-- SELECT * FROM Tenant WHERE email = 'alicej@example.com'; 

-- Find an owner by phone  
-- SELECT * FROM Owner WHERE phone = '555-234-5678'; 










-- View: Active Leases with Tenant & Property Details
CREATE VIEW ActiveLeases AS
SELECT
  l.lease_id, p.address, CONCAT(t.first_name, ' ', t.last_name) AS tenant_name, 
  l.monthly_rent, l.start_date, l.end_date
FROM Lease l
JOIN Property p ON l.property_id = p.property_id
JOIN Tenant t ON l.tenant_id = t.tenant_id
WHERE l.lease_status = 'Active';

-- View: Maintenance Requests with Employee Assignments
CREATE VIEW OpenMaintenanceRequests AS
SELECT
  mr.request_id, p.address, 
  IFNULL(CONCAT(e.first_name, ' ', e.last_name), 'Unassigned') AS assigned_to,
  mr.description, mr.request_date
FROM MaintenanceRequest mr
JOIN Property p ON mr.property_id = p.property_id
LEFT JOIN Employee e ON mr.employee_id = e.employee_id
WHERE mr.status = 'Open';

-- View: Financial Summary (Rent vs. Maintenance Costs)
CREATE VIEW FinancialSummary AS
SELECT
  p.property_id, p.address,
  IFNULL(SUM(pay.amount), 0) AS total_rent,  -- Ensure NULL sums return 0
  IFNULL(SUM(mr.cost), 0) AS total_maintenance_cost  -- Ensure NULL sums return 0
FROM Property p
LEFT JOIN Lease l ON p.property_id = l.property_id
LEFT JOIN Payment pay ON l.lease_id = pay.lease_id
LEFT JOIN MaintenanceRequest mr ON p.property_id = mr.property_id
GROUP BY p.property_id, p.address;


-- SELECT * FROM FinancialSummary;










-- Temporary Table: Monthly Rent Roll (Session-Scoped)
CREATE TEMPORARY TABLE MonthlyRentRoll (
  property_id INT, address VARCHAR(255), expected_rent DECIMAL(10,2), received_rent DECIMAL(10,2)
);

INSERT INTO MonthlyRentRoll (property_id, address, expected_rent, received_rent)
SELECT
  p.property_id, p.address, IFNULL(SUM(l.monthly_rent), 0) AS expected_rent,
  IFNULL(SUM(pay.amount), 0) AS received_rent
FROM Property p
JOIN Lease l ON p.property_id = l.property_id
LEFT JOIN Payment pay ON l.lease_id = pay.lease_id
WHERE l.lease_status = 'Active'
GROUP BY p.property_id, p.address;

-- SELECT * FROM MonthlyRentRoll;











-- Trigger: Update Lease Status on End Date
-- DELIMITER $$

-- CREATE TRIGGER trg_lease_status
-- BEFORE INSERT OR UPDATE ON Lease
-- FOR EACH ROW
-- BEGIN
--   IF NEW.end_date < CURDATE() THEN
--     SET NEW.lease_status = 'Expired';
--   END IF;
-- END$$

-- DELIMITER ;


-- Trigger: Log Late Payments
DELIMITER $$  

CREATE TRIGGER trg_late_payment  
AFTER INSERT ON Payment  
FOR EACH ROW  
BEGIN  
  DECLARE lease_due_day INT;  
  DECLARE lease_due_date DATE;  

  -- Fetch due_day from Lease  
  SELECT due_day INTO lease_due_day FROM Lease WHERE lease_id = NEW.lease_id;  

  -- Calculate due_date using payment_date's year/month and due_day  
  SET lease_due_date = STR_TO_DATE(  
    CONCAT(YEAR(NEW.payment_date), '-', MONTH(NEW.payment_date), '-', lease_due_day),  
    '%Y-%m-%d'  
  );  

  -- Log late payments  
  IF NEW.payment_date > lease_due_date THEN  
    INSERT INTO PaymentAudit (payment_id, late_fee, audit_timestamp)  
    VALUES (NEW.payment_id, NEW.amount * 0.1, CURRENT_TIMESTAMP);  
  END IF;  
END$$  

DELIMITER ;  

INSERT INTO Payment (lease_id, amount, payment_date, payment_method)  
VALUES (1, 1800.00, '2024-02-05', 'Bank Transfer');  

SELECT * FROM PaymentAudit;










-- Procedure: Add New Lease with Validation
DELIMITER $$

CREATE PROCEDURE AddLease(
  IN p_property_id INT,
  IN p_tenant_id INT,
  IN p_start_date DATE,
  IN p_end_date DATE,
  IN p_monthly_rent DECIMAL(10,2)
)
BEGIN
  DECLARE lease_count INT;

  -- Check for overlapping leases
  SELECT COUNT(*) INTO lease_count
  FROM Lease
  WHERE property_id = p_property_id
  AND (p_start_date BETWEEN start_date AND end_date);

  IF lease_count > 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Property is already leased during this period';
  ELSE
    INSERT INTO Lease (property_id, tenant_id, start_date, end_date, monthly_rent, lease_status)
    VALUES (p_property_id, p_tenant_id, p_start_date, p_end_date, p_monthly_rent, 'Active');
  END IF;
END$$

DELIMITER ;


-- Procedure: Process Monthly Rent Payment
DELIMITER $$

CREATE PROCEDURE ProcessRentPayment(
  IN p_lease_id INT,
  IN p_amount DECIMAL(10,2),
  IN p_payment_method VARCHAR(20)
)
BEGIN
  -- Insert payment record
  INSERT INTO Payment (lease_id, amount, payment_date, payment_method)
  VALUES (p_lease_id, p_amount, CURDATE(), p_payment_method);

  -- Update last_payment_date in Lease table
  UPDATE Lease
  SET last_payment_date = CURDATE()
  WHERE lease_id = p_lease_id;
END$$

DELIMITER ;


-- Procedure: Calculate Owner Payout
DELIMITER $$

CREATE PROCEDURE CalculateOwnerPayout(IN p_property_id INT)
BEGIN
  SELECT
    CONCAT(o.first_name, ' ', o.last_name) AS owner_name,
    SUM(l.monthly_rent * po.ownership_percentage / 100) AS payout
  FROM PropertyOwner po
  JOIN Owner o ON po.owner_id = o.owner_id
  JOIN Lease l ON po.property_id = l.property_id
  WHERE po.property_id = p_property_id
    AND l.lease_status = 'Active'
  GROUP BY o.owner_id;
END$$

DELIMITER ;


CALL CalculateOwnerPayout(5);  














-- Function: Check Lease Overlap
DELIMITER $$  

CREATE FUNCTION CheckLeaseOverlap(  
  p_property_id INT,  
  p_start_date DATE,  
  p_end_date DATE,  
  p_ignore_expired BOOLEAN 
) RETURNS INT  
DETERMINISTIC  
BEGIN  
  DECLARE overlap_count INT;  

  SELECT COUNT(*)  
  INTO overlap_count  
  FROM Lease  
  WHERE  
    property_id = p_property_id  
    AND (p_start_date <= end_date AND p_end_date >= start_date)  
    -- Conditionally filter by lease status  
    AND (  
      (p_ignore_expired AND lease_status = 'Active') -- Include only active leases  
      OR NOT p_ignore_expired -- Include all leases if p_ignore_expired = FALSE  
    );  

  RETURN IF(overlap_count > 0, 1, 0);  
END$$  

DELIMITER ;  

-- Check Overlaps with Active Leases Only:
SELECT CheckLeaseOverlap(5, '2024-01-01', '2024-12-31', TRUE) AS OverlapExists;  


SELECT CheckLeaseOverlap(5, '2024-01-01', '2024-12-31', FALSE) AS OverlapExists;  















WITH OwnerPayouts AS (
  SELECT
    o.owner_id,
    CONCAT(o.first_name, ' ', o.last_name) AS owner_name,
    SUM(l.monthly_rent * (po.ownership_percentage / 100)) AS total_payout
  FROM PropertyOwner po
  JOIN Owner o ON po.owner_id = o.owner_id
  JOIN Lease l ON po.property_id = l.property_id
  WHERE l.lease_status = 'Active'
  GROUP BY o.owner_id
)
SELECT
  owner_name,
  total_payout,
  RANK() OVER (ORDER BY total_payout DESC) AS payout_rank,
  ROUND((total_payout / SUM(total_payout) OVER ()) * 100, 2) AS contribution_percent
FROM OwnerPayouts;












WITH PropertyRequests AS (
  SELECT
    p.property_id,
    p.address,
    p.city,
    COUNT(mr.request_id) AS property_requests
  FROM Property p
  LEFT JOIN MaintenanceRequest mr ON p.property_id = mr.property_id
  WHERE mr.status = 'Open'
  GROUP BY p.property_id, p.city, p.address
)
SELECT
  pr.address,
  pr.city,
  pr.property_requests,
  (SELECT AVG(property_requests) 
   FROM PropertyRequests 
   WHERE city = pr.city) AS city_avg_requests
FROM PropertyRequests pr;











SELECT
  property_id,
  tenant_id,
  end_date AS current_lease_end,
  LEAD(start_date) OVER (
    PARTITION BY property_id
    ORDER BY start_date
  ) AS next_lease_start
FROM Lease
WHERE lease_status = 'Active';










SELECT
  property_id,
  YEAR(start_date) AS year,
  MONTH(start_date) AS month,
  monthly_rent,
  LAG(monthly_rent, 12) OVER (
    PARTITION BY property_id
    ORDER BY start_date
  ) AS prev_year_rent,
  (monthly_rent - LAG(monthly_rent, 12) OVER (PARTITION BY property_id ORDER BY start_date)) /
  LAG(monthly_rent, 12) OVER (PARTITION BY property_id ORDER BY start_date) * 100 AS yoy_growth
FROM Lease;











SELECT
  property_id,
  address,
  monthly_rent,
  NTILE(4) OVER (ORDER BY monthly_rent DESC) AS rent_quartile
FROM Lease
JOIN Property USING (property_id)
WHERE lease_status = 'Active';












WITH RankedRequests AS (
  SELECT
    property_id,
    request_id,
    description,
    request_date,
    ROW_NUMBER() OVER (
      PARTITION BY property_id
      ORDER BY request_date
    ) AS request_rank
  FROM MaintenanceRequest
  WHERE status = 'Open'
)
SELECT *
FROM RankedRequests
WHERE request_rank = 1;






SELECT
  property_id,
  address,
  SUM(DATEDIFF(end_date, start_date)) AS total_occupied_days,
  (SUM(DATEDIFF(end_date, start_date)) / 365) * 100 AS occupancy_rate_percent
FROM Lease
JOIN Property USING (property_id)
GROUP BY property_id, address;








SELECT
  t.tenant_id,
  CONCAT(t.first_name, ' ', t.last_name) AS tenant_name,
  p.payment_date,
  p.amount,
  SUM(p.amount) OVER (
    PARTITION BY t.tenant_id
    ORDER BY p.payment_date
  ) AS running_total_paid
FROM Payment p
JOIN Lease l ON p.lease_id = l.lease_id
JOIN Tenant t ON l.tenant_id = t.tenant_id;









SELECT
  p.address,
  mr.request_date,
  mr.cost,
  AVG(mr.cost) OVER (
    PARTITION BY mr.property_id
    ORDER BY mr.request_date
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS rolling_avg_cost
FROM MaintenanceRequest mr
JOIN Property p ON mr.property_id = p.property_id;









WITH LeaseRenewals AS (
  SELECT
    tenant_id,
    COUNT(*) AS total_leases,
    SUM(CASE WHEN end_date > start_date THEN 1 ELSE 0 END) AS renewed_leases
  FROM Lease
  GROUP BY tenant_id
)
SELECT
  tenant_id,
  CONCAT(t.first_name, ' ', t.last_name) AS tenant_name,
  ROUND((renewed_leases / total_leases) * 100, 2) AS renewal_rate
FROM LeaseRenewals
JOIN Tenant t USING (tenant_id);







SELECT
  p.address,
  p.purchase_price,
  SUM(l.monthly_rent * 12) AS annual_rent,
  ROUND((SUM(l.monthly_rent * 12) / p.purchase_price) * 100, 2) AS rent_yield_percent
FROM Lease l
JOIN Property p ON l.property_id = p.property_id
WHERE l.lease_status = 'Active'
GROUP BY p.property_id, p.address, p.purchase_price;









SELECT
  p.address,
  COUNT(mr.request_id) AS open_requests,
  RANK() OVER (ORDER BY COUNT(mr.request_id) DESC) AS request_rank
FROM MaintenanceRequest mr
JOIN Property p ON mr.property_id = p.property_id
WHERE mr.status = 'Open'
GROUP BY p.property_id, p.address;









SELECT
  o.owner_id,
  CONCAT(o.first_name, ' ', o.last_name) AS owner_name,
  SUM(p.purchase_price * (po.ownership_percentage / 100)) AS portfolio_value
FROM PropertyOwner po
JOIN Owner o ON po.owner_id = o.owner_id
JOIN Property p ON po.property_id = p.property_id
GROUP BY o.owner_id;








SELECT
  t.tenant_id,
  CONCAT(t.first_name, ' ', t.last_name) AS tenant_name,
  p.payment_date,
  -- Calculate due_date using due_day and payment_date
  DATE_FORMAT(p.payment_date, '%Y-%m') AS payment_month,  -- Extract year and month from payment_date
  DATE_FORMAT(p.payment_date, '%Y-%m-') || LPAD(l.due_day, 2, '0') AS due_date,  -- Construct due_date
  DATEDIFF(p.payment_date, DATE_FORMAT(p.payment_date, '%Y-%m-') || LPAD(l.due_day, 2, '0')) AS days_overdue
FROM Payment p
JOIN Lease l ON p.lease_id = l.lease_id
JOIN Tenant t ON l.tenant_id = t.tenant_id
WHERE p.payment_date > DATE_FORMAT(p.payment_date, '%Y-%m-') || LPAD(l.due_day, 2, '0');










SELECT
  o.owner_id,
  CONCAT(o.first_name, ' ', o.last_name) AS owner_name,
  SUM(mr.cost * (po.ownership_percentage / 100)) AS allocated_cost
FROM MaintenanceRequest mr
JOIN Property p ON mr.property_id = p.property_id
JOIN PropertyOwner po ON p.property_id = po.property_id
JOIN Owner o ON po.owner_id = o.owner_id
GROUP BY o.owner_id;

