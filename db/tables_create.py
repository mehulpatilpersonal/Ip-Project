from db.queries_sql import mycon, cursor, engine
#Creating a database
def create_database():
    cursor.execute("CREATE DATABASE IF NOT EXISTS vehiclemanagement")
    mycon.database = 'vehiclemanagement'

#Creating all tables in the database
def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(15),
            address VARCHAR(225),
            city VARCHAR(50),
            state VARCHAR(50),
            password VARCHAR(100) NOT NULL,
            user_role ENUM('Admin','Mechanic','Customer') DEFAULT 'Customer',
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_no VARCHAR(30) PRIMARY KEY,
            vehicle_brand VARCHAR(50),
            model VARCHAR(50),
            type ENUM('Car','Bike','Truck','Bus','Tractor','other') NOT NULL,
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            service_id INT AUTO_INCREMENT PRIMARY KEY,
            service_name VARCHAR(100) UNIQUE NOT NULL,
            description TEXT,
            base_price DECIMAL(10,2) NOT NULL,
            estimated_hours DECIMAL(4,2),
            warranty_months INT DEFAULT 0,
            category ENUM('Maintenance','Repair','Inspection','Upgrade','Painting') NOT NULL,
            status ENUM('Active','Inactive') DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_bookings (
            booking_id INT AUTO_INCREMENT PRIMARY KEY,
            vehicle_no VARCHAR(30),
            service_id INT,
            booking_date DATE NOT NULL,
            status ENUM('Pending','In Progress','Completed','Cancelled') DEFAULT 'Pending',
            FOREIGN KEY (vehicle_no) REFERENCES vehicles(vehicle_no) ON DELETE CASCADE,
            FOREIGN KEY (service_id) REFERENCES services(service_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mechanics_info (
            mechanic_id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(100) NOT NULL,
            specialization VARCHAR(100),
            phone VARCHAR(15),
            email VARCHAR(100)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mechanic_assignments (
            assignment_id INT AUTO_INCREMENT PRIMARY KEY,
            booking_id INT,
            mechanic_id INT,
            assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (booking_id) REFERENCES service_bookings(booking_id) ON DELETE CASCADE,
            FOREIGN KEY (mechanic_id) REFERENCES mechanics_info(mechanic_id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id INT AUTO_INCREMENT PRIMARY KEY,
            booking_id INT,
            user_id INT,
            amount DECIMAL(10, 2) NOT NULL,
            payment_status ENUM('Pending','Paid','Failed') DEFAULT 'Pending',
            payment_method ENUM('Cash','Card','UPI','Bank Transfer') DEFAULT 'Cash',
            invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (booking_id) REFERENCES service_bookings(booking_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parts_inventory (
            part_id INT AUTO_INCREMENT PRIMARY KEY,
            part_name VARCHAR(100) NOT NULL,
            description TEXT,
            unit_price DECIMAL(10,2) NOT NULL,
            stock_quantity INT DEFAULT 0,
            supplier VARCHAR(100)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id INT AUTO_INCREMENT PRIMARY KEY,
            booking_id INT,
            rating INT CHECK (rating BETWEEN 1 AND 5),
            comments VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (booking_id) REFERENCES service_bookings(booking_id)
        )
    """)

    mycon.commit()

# Inserting data into the table-user
def in_users(username, email, phone, address, password, user_role):
    try:
        cursor.execute("""
                       INSERT INTO users (username, email, phone, address, password, user_role)
                       VALUES (%s, %s, %s, %s, %s, %s)
                       """, (username, email, phone, address, password, user_role))
        mycon.commit()
    except Exception as e:
        print(f"Error inserting user: {e}")
        mycon.rollback()

# Inserting data into the table-vehicles
def in_vehicles(vehicle_no, model, type, user_id):
    try:
        cursor.execute("""
                       INSERT INTO vehicles (vehicle_no, model, type, user_id)
                       VALUES (%s, %s, %s, %s)
                       """, (vehicle_no, model, type, user_id))
        mycon.commit()
    except Exception as e:
        print(f"Error inserting vehicle: {e}")
        mycon.rollback()

# Inserting data into the table-services
def in_services(service_type):
    try:
        cursor.execute("""
                       INSERT INTO services (service_type)
                       VALUES (%s)
                       """, (service_type,))
        mycon.commit()
    except Exception as e:
        print(f"Error inserting service: {e}")
        mycon.rollback()

# Inserting data into the table-service_bookings
def in_service_bookings(vehicle_no, service_type, booking_date, status):
    try:
        cursor.execute("""
                       INSERT INTO service_bookings (vehicle_no, service_type, booking_date, status)
                       VALUES (%s, %s, %s, %s)
                       """, (vehicle_no, service_type, booking_date, status))
        mycon.commit()
    except Exception as e:
        print(f"Error inserting service booking: {e}")
        mycon.rollback()

# Inserting data into the table-mechanics_info
def in_mechanics(mechanic):
    try:
        cursor.execute("""
                       INSERT INTO mechanics_info (mechanic)
                       VALUES (%s)
                       """, (mechanic,))
        mycon.commit()
    except Exception as e:
        print(f"Error inserting mechanic: {e}")
        mycon.rollback()

# Inserting data into the table-mechanic_assignments
def in_mechanic_assignments(service_id, mechanic_id):
    try:
        cursor.execute("""
                       INSERT INTO mechanic_assignments (service_id, mechanic_id)
                       VALUES (%s, %s)
                       """, (service_id, mechanic_id))
        mycon.commit()
    except Exception as e:
        print(f"Error inserting mechanic assignment: {e}")
        mycon.rollback()

# Inserting data into the table-invoices
def in_invoices(user_id, service_id, amount, invoice_date):
    try:
        cursor.execute("""
                       INSERT INTO invoices (user_id, service_id, amount, invoice_date)
                       VALUES (%s, %s, %s, %s)
                       """, (user_id, service_id, amount, invoice_date))
        mycon.commit()
    except Exception as e:
        print(f"Error inserting invoice: {e}")
        mycon.rollback()

# Inserting data into the table-feedback
def in_feedback(service_id, rating, comments):
    try:
        cursor.execute("""
                       INSERT INTO feedback (service_id, rating, comments)
                       VALUES (%s, %s, %s)
                       """, (service_id, rating, comments))
        mycon.commit()
    except Exception as e:
        print(f"Error inserting feedback: {e}")
        mycon.rollback()