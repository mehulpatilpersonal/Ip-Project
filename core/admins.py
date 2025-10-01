from db.queries_sql import sql_connect, mycon, cursor, engcon
import pandas as pd
from tabulate import tabulate
from styles import *  # uses your existing BRIGHT_* colors

# ================== tiny UI helpers ==================
def pause(msg="Press Enter to continue..."):
    try:
        input(f"{DIM_YELLOW}{msg}")
    except EOFError:
        pass

def menu_box(title, items, prompt="Select an option: "):
    print(f"\n{BRIGHT_YELLOW}{title}")
    print(tabulate([[i] for i in items], tablefmt="fancy_grid"))
    return input(f"{BRIGHT_YELLOW}{prompt}").strip()

def fetch_df(sql, params=None):
    try:
        return pd.read_sql(sql, con=engcon, params=params or ())
    except Exception as e:
        print(f"{BRIGHT_RED}DB Error: {e}")
        pause()
        return pd.DataFrame()

def exec_sql(sql, params=None, success="✅ Done."):
    try:
        cursor.execute(sql, params or ())
        mycon.commit()
        print(f"{BRIGHT_GREEN}{success}")
    except Exception as e:
        mycon.rollback()
        print(f"{BRIGHT_RED}DB Error: {e}")
    pause()

# ================== auth ==================
def admin_login():
    while True:
        username = input(f"{BRIGHT_YELLOW}ENTER ADMIN USERNAME: ").strip()
        password = input(f"{BRIGHT_YELLOW}ENTER ADMIN PASSWORD: ").strip()
        if not (username and password):
            print(f"{BRIGHT_RED}❌ Username & Password required.")
            if input(f"{DIM_YELLOW}Press Enter or type 'exit': ").lower() == "exit":
                return
            continue
        df = fetch_df(
            "SELECT * FROM users WHERE username=%s AND password=%s AND user_role='admin'",
            (username, password),
        )
        if not df.empty:
            print(f"\n{BRIGHT_GREEN}✅ ADMIN LOGIN SUCCESSFUL!\n")
            cols = [c for c in ("user_id", "username", "user_role") if c in df.columns]
            if cols:
                print(df[cols].head(1))
            admin_dashboard(df)
            return
        print(f"{BRIGHT_RED}❌ Invalid credentials.")

# ================== USERS ==================
def create_user():
    name = input("Name: ").strip()
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()
    address = input("Address: ").strip()
    city = input("City: ").strip()
    state = input("State: ").strip()
    password = input("Password: ").strip()
    role = input("Role (Admin/Mechanic/Customer): ").strip().title()
    if role.lower()=='mechanic':
        exec_sql("INSERT INTO mechanics_info(full_name,email) VALUES(%s,%s)",(name,email),success="✅ Mechanic profile created.")
    exec_sql(
        """INSERT INTO users(name,username,email,phone,address,city,state,password,user_role,registered_at)
           VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())""",
        (name,username,email,phone,address,city,state,password,role)
    )

def list_users():
    q = input("Search (leave empty for all): ").strip()
    if q:
        df = fetch_df("""SELECT user_id,name,username,email,phone,user_role,registered_at
                          FROM users WHERE name LIKE %s OR username LIKE %s OR email LIKE %s
                          ORDER BY registered_at DESC""", (f"%{q}%",f"%{q}%",f"%{q}%"))
    else:
        df = fetch_df("""SELECT user_id,name,username,email,phone,user_role,registered_at
                         FROM users ORDER BY registered_at DESC""")
    print(df.to_string(index=False) if not df.empty else f"{BRIGHT_RED}No users.")
    pause()

def update_user():
    uid = input("User ID to update: ").strip()
    field = input("Field (name, email, phone, address, city, state, username, password): ").strip()
    value = input("New value: ").strip()
    exec_sql(f"UPDATE users SET {field}=%s WHERE user_id=%s", (value, uid))

def delete_user():
    uid = input("User ID to delete: ").strip()
    exec_sql("DELETE FROM users WHERE user_id=%s", (uid,))

def change_role():
    uid = input("User ID: ").strip()
    role = input("New role (Admin/Mechanic/Customer): ").strip().title()
    exec_sql("UPDATE users SET user_role=%s WHERE user_id=%s", (role, uid))
    if role.lower()=='mechanic':    #ROLE CHANGE TO MECHANIC SO DATA INSERTED IN MECHANIC TABLE
        name_email = fetch_df("SELECT name,email FROM users WHERE user_id=%s",(uid,))
        if not name_email.empty:
            name, email = name_email.iloc[0][["name","email"]]
            exec_sql("INSERT INTO mechanics_info(full_name,email) VALUES(%s,%s)",(name,email),success="✅ Mechanic profile created.")
    

def reset_password():
    uid = input("User ID: ").strip()
    pwd = input("New Password: ").strip()
    exec_sql("UPDATE users SET password=%s WHERE user_id=%s", (pwd, uid))

# ================== VEHICLES ==================
def add_vehicle():
    vehicle_no = input("Vehicle No: ").strip()
    brand = input("Brand: ").strip()
    model = input("Model: ").strip()
    vtype = input("Type (Car/Bike/Truck/Bus/Tractor/Other): ").strip().title()
    user_id = input("Owner User ID: ").strip()
    exec_sql("""INSERT INTO vehicles(vehicle_no,vehicle_brand,model,type,user_id)
                VALUES(%s,%s,%s,%s,%s)""", (vehicle_no,brand,model,vtype,user_id))

def list_vehicles():
    q = input("Search (vehicle_no/brand/model/owner): ").strip()
    if q:
        df = fetch_df("""SELECT v.vehicle_no,v.vehicle_brand,v.model,v.type,u.name AS owner
                         FROM vehicles v JOIN users u ON v.user_id=u.user_id
                         WHERE v.vehicle_no LIKE %s OR v.vehicle_brand LIKE %s OR v.model LIKE %s OR u.name LIKE %s
                         ORDER BY v.vehicle_no""", (f"%{q}%",)*4)
    else:
        df = fetch_df("""SELECT v.vehicle_no,v.vehicle_brand,v.model,v.type,u.name AS owner
                         FROM vehicles v JOIN users u ON v.user_id=u.user_id ORDER BY v.vehicle_no""")
    print(df.to_string(index=False) if not df.empty else f"{BRIGHT_RED}No vehicles.")
    pause()

def edit_vehicle():
    vno = input("Vehicle No to edit: ").strip()
    field = input("Field (vehicle_brand, model, type, user_id): ").strip()
    value = input("New value: ").strip()
    exec_sql(f"UPDATE vehicles SET {field}=%s WHERE vehicle_no=%s", (value, vno))

def delete_vehicle():
    vno = input("Vehicle No to delete: ").strip()
    exec_sql("DELETE FROM vehicles WHERE vehicle_no=%s", (vno,))

# ================== SERVICES ==================
def add_service():
    name = input("Service Name: ").strip()
    desc = input("Description: ").strip()
    price = float(input("Base Price: ").strip() or 0)
    hours = float(input("Estimated Hours: ").strip() or 0)
    warranty = int(input("Warranty Months: ").strip() or 0)
    category = input("Category (Maintenance/Repair/Inspection/Upgrade/Painting): ").strip().title()
    status = (input("Status (Active/Inactive): ").strip().title() or "Active")
    exec_sql("""INSERT INTO services(service_name,description,base_price,estimated_hours,
                warranty_months,category,status,created_at)
                VALUES(%s,%s,%s,%s,%s,%s,%s,NOW())""",
             (name,desc,price,hours,warranty,category,status))

def list_services():
    df = fetch_df("""SELECT service_id,service_name,category,base_price,estimated_hours,
                     warranty_months,status,created_at FROM services ORDER BY created_at DESC""")
    print(df.to_string(index=False) if not df.empty else f"{BRIGHT_RED}No services.")
    pause()

def update_service():
    sid = input("Service ID: ").strip()
    price = input("New base_price (blank skip): ").strip()
    hours = input("New estimated_hours (blank skip): ").strip()
    warranty = input("New warranty_months (blank skip): ").strip()
    desc = input("New description (blank skip): ").strip()
    category = input("New category (blank skip): ").strip()
    sets, params = [], []
    if price: sets.append("base_price=%s"); params.append(float(price))
    if hours: sets.append("estimated_hours=%s"); params.append(float(hours))
    if warranty: sets.append("warranty_months=%s"); params.append(int(warranty))
    if desc: sets.append("description=%s"); params.append(desc)
    if category: sets.append("category=%s"); params.append(category)
    if not sets:
        print(f"{BRIGHT_RED}Nothing to update.")
        pause()
        return
    params.append(sid)
    exec_sql(f"UPDATE services SET {', '.join(sets)} WHERE service_id=%s", tuple(params))

def toggle_service():
    sid = input("Service ID: ").strip()
    status = input("Status (Active/Inactive): ").strip().title()
    exec_sql("UPDATE services SET status=%s WHERE service_id=%s", (status, sid))

def delete_service():
    sid = input("Service ID to delete: ").strip()
    exec_sql("DELETE FROM services WHERE service_id=%s", (sid,))

# ================== BOOKINGS ==================
def create_booking():
    vno = input("Vehicle No: ").strip()
    sid = input("Service ID: ").strip()
    date = input("Booking Date (YYYY-MM-DD): ").strip()
    status = "Pending"
    exec_sql("""INSERT INTO service_bookings(vehicle_no,service_id,booking_date,status)
                VALUES(%s,%s,%s,%s)""", (vno,sid,date,status))

def list_bookings():
    status = input("Filter by Status (leave empty for all): ").strip().title()
    if status:
        df = fetch_df("""SELECT b.booking_id,b.booking_date,b.status,v.vehicle_no,s.service_name
                         FROM service_bookings b
                         JOIN vehicles v ON b.vehicle_no=v.vehicle_no
                         JOIN services s ON b.service_id=s.service_id
                         WHERE b.status=%s ORDER BY b.booking_date DESC""", (status,))
    else:
        df = fetch_df("""SELECT b.booking_id,b.booking_date,b.status,v.vehicle_no,s.service_name
                         FROM service_bookings b
                         JOIN vehicles v ON b.vehicle_no=v.vehicle_no
                         JOIN services s ON b.service_id=s.service_id
                         ORDER BY b.booking_date DESC""")
    print(df.to_string(index=False) if not df.empty else f"{BRIGHT_RED}No bookings.")
    pause()

def update_booking_status():
    bid = input("Booking ID: ").strip()
    status = input("New Status (Pending/In Progress/Completed/Cancelled): ").strip().title()
    exec_sql("UPDATE service_bookings SET status=%s WHERE booking_id=%s", (status, bid))

def change_booking_service():
    bid = input("Booking ID: ").strip()
    sid = input("New Service ID: ").strip()
    exec_sql("UPDATE service_bookings SET service_id=%s WHERE booking_id=%s", (sid, bid))

def assign_mechanic():
    bid = input("Booking ID: ").strip()
    mid = input("Mechanic ID: ").strip()
    exec_sql("""INSERT INTO mechanic_assignments(booking_id,mechanic_id,assigned_date)
                VALUES(%s,%s,NOW())""", (bid, mid))

def cancel_booking():
    bid = input("Booking ID to cancel: ").strip()
    exec_sql("UPDATE service_bookings SET status='Cancelled' WHERE booking_id=%s", (bid,))

# ================== MECHANICS ==================
def add_mechanic():
    name = input("Full Name: ").strip()
    spec = input("Specialization: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    exec_sql("""INSERT INTO mechanics_info(full_name,specialization,phone,email)
                VALUES(%s,%s,%s,%s)""", (name,spec,phone,email))
    exec_sql("INSERT IGNORE INTO users(name,username,email,password,user_role,registered_at) VALUES(%s,%s,%s,%s,%s,NOW())",
             (name,name,email,"mechanic123","Mechanic"), success="✅ User profile created with default password 'mechanic123'.") #HERE I USED IGNORE WHICH IS A MYSQL SPECIFIC COMMAND TO AVOID DUPLICATE ENTRY ERROR

def list_mechanics():
    df = fetch_df("SELECT mechanic_id,full_name,specialization,phone,email FROM mechanics_info")
    print(df.to_string(index=False) if not df.empty else f"{BRIGHT_RED}No mechanics.")
    pause()

def update_mechanic():
    mid = input("Mechanic ID: ").strip()
    field = input("Field (full_name, specialization, phone, email): ").strip()
    value = input("New value: ").strip()
    exec_sql(f"UPDATE mechanics_info SET {field}=%s WHERE mechanic_id=%s", (value, mid))
    if field.lower() in ("full_name", "email"):
        # Also update in users table
        exec_sql(f"UPDATE users SET {field}=%s WHERE email=(SELECT email FROM mechanics_info WHERE mechanic_id=%s)",
                 (value, mid))

def delete_mechanic():
    mid = input("Mechanic ID to delete: ").strip()
    exec_sql("DELETE FROM mechanics_info WHERE mechanic_id=%s", (mid,))

def view_workload():
    df = fetch_df("""SELECT m.mechanic_id,m.full_name,COUNT(a.assignment_id) AS jobs
                     FROM mechanics_info m
                     LEFT JOIN mechanic_assignments a ON m.mechanic_id=a.mechanic_id
                     GROUP BY m.mechanic_id,m.full_name
                     ORDER BY jobs DESC""")
    print(df.to_string(index=False) if not df.empty else f"{BRIGHT_RED}No data.")
    pause()

# ================== INVENTORY ==================
def add_part():
    name = input("Part Name: ").strip()
    desc = input("Description: ").strip()
    price = float(input("Unit Price: ").strip() or 0)
    qty = int(input("Stock Quantity: ").strip() or 0)
    supplier = input("Supplier: ").strip()
    exec_sql("""INSERT INTO parts_inventory(part_name,description,unit_price,stock_quantity,supplier)
                VALUES(%s,%s,%s,%s,%s)""", (name,desc,price,qty,supplier))

def list_parts():
    df = fetch_df("""SELECT part_id,part_name,unit_price,stock_quantity,supplier
                     FROM parts_inventory ORDER BY part_name""")
    print(df.to_string(index=False) if not df.empty else f"{BRIGHT_RED}No parts.")
    pause()

def update_part():
    pid = input("Part ID: ").strip()
    field = input("Field (part_name, description, unit_price, supplier): ").strip()
    value = input("New value: ").strip()
    exec_sql(f"UPDATE parts_inventory SET {field}=%s WHERE part_id=%s", (value, pid))

def adjust_stock():
    pid = input("Part ID: ").strip()
    delta = int(input("Adjust qty (+in / -out): ").strip() or 0)
    exec_sql("UPDATE parts_inventory SET stock_quantity = stock_quantity + %s WHERE part_id=%s",
             (delta, pid), success="✅ Stock updated.")

def delete_part():
    pid = input("Part ID to delete: ").strip()
    exec_sql("DELETE FROM parts_inventory WHERE part_id=%s", (pid,))

def approve_parts_requests():
    print(f"{BRIGHT_CYAN}Parts request approval flow is project-specific. Hook your request table here.")
    pause()

# ================== INVOICES ==================
def generate_invoice():
    bid = input("Booking ID: ").strip()
    uid = input("User ID: ").strip()
    amount = float(input("Amount: ").strip() or 0)
    pay_status = input("Payment Status (Pending/Paid/Failed): ").strip().title() or "Pending"
    method = input("Payment Method (Cash/Card/UPI/Bank Transfer): ").strip().title() or "Cash"
    exec_sql("""INSERT INTO invoices(booking_id,user_id,amount,payment_status,payment_method,invoice_date)
                VALUES(%s,%s,%s,%s,%s,NOW())""", (bid,uid,amount,pay_status,method))

def list_invoices():
    df = fetch_df("""SELECT i.invoice_id,i.invoice_date,i.amount,i.payment_status,i.payment_method,u.name AS customer
                     FROM invoices i JOIN users u ON i.user_id=u.user_id
                     ORDER BY i.invoice_date DESC""")
    print(df.to_string(index=False) if not df.empty else f"{BRIGHT_RED}No invoices.")
    pause()

def mark_payment():
    iid = input("Invoice ID: ").strip()
    status = input("Set Payment Status (Pending/Paid/Failed): ").strip().title()
    method = input("Payment Method (Cash/Card/UPI/Bank Transfer): ").strip().title()
    exec_sql("UPDATE invoices SET payment_status=%s, payment_method=%s WHERE invoice_id=%s",
             (status, method, iid))

def refund_adjustment():
    iid = input("Invoice ID: ").strip()
    amt = float(input("Refund/Adjustment amount (- to reduce): ").strip() or 0)
    exec_sql("UPDATE invoices SET amount = amount + %s WHERE invoice_id=%s",
             (-abs(amt), iid), success="✅ Invoice adjusted.")

# ================== FEEDBACK ==================
def list_feedback():
    df = fetch_df("""SELECT f.feedback_id,f.rating,f.comments,f.created_at,
                            s.service_name,b.booking_id
                     FROM feedback f
                     JOIN service_bookings b ON f.booking_id=b.booking_id
                     JOIN services s ON b.service_id=s.service_id
                     ORDER BY f.created_at DESC""")
    print(df.to_string(index=False) if not df.empty else f"{BRIGHT_RED}No feedback.")
    pause()

def filter_feedback():
    minr = int(input("Min rating (1-5): ").strip() or 1)
    df = fetch_df("""SELECT f.feedback_id,f.rating,f.comments,f.created_at,
                            s.service_name,b.booking_id
                     FROM feedback f
                     JOIN service_bookings b ON f.booking_id=b.booking_id
                     JOIN services s ON b.service_id=s.service_id
                     WHERE f.rating >= %s
                     ORDER BY f.created_at DESC""", (minr,))
    print(df.to_string(index=False) if not df.empty else f"{BRIGHT_RED}No results.")
    pause()

def export_feedback_csv():
    df = fetch_df("""SELECT f.*, s.service_name
                     FROM feedback f
                     JOIN service_bookings b ON f.booking_id=b.booking_id
                     JOIN services s ON b.service_id=s.service_id""")
    if df.empty:
        print(f"{BRIGHT_RED}Nothing to export.")
    else:
        df.to_csv("feedback_export.csv", index=False)
        print(f"{BRIGHT_GREEN}✅ Exported to feedback_export.csv")
    pause()

# ================== REPORTS ==================
def revenue_report():
    grp = input("Group by (D/W/M): ").strip().upper() or "D"
    if grp == "W":
        sql = """SELECT YEAR(invoice_date) y, WEEK(invoice_date) w, SUM(amount) revenue
                 FROM invoices GROUP BY y,w ORDER BY y DESC,w DESC"""
    elif grp == "M":
        sql = """SELECT YEAR(invoice_date) y, MONTH(invoice_date) m, SUM(amount) revenue
                 FROM invoices GROUP BY y,m ORDER BY y DESC,m DESC"""
    else:
        sql = """SELECT DATE(invoice_date) d, SUM(amount) revenue
                 FROM invoices GROUP BY d ORDER BY d DESC"""
    df = fetch_df(sql)
    print(df.to_string(index=False) if not df.empty else f"{BRIGHT_RED}No data.")
    pause()

def top_services_report():
    df = fetch_df("""SELECT s.service_id,s.service_name,COUNT(b.booking_id) AS bookings
                     FROM services s
                     LEFT JOIN service_bookings b ON s.service_id=b.service_id
                     GROUP BY s.service_id,s.service_name
                     ORDER BY bookings DESC LIMIT 20""")
    print(df.to_string(index=False) if not df.empty else f"{BRIGHT_RED}No data.")
    pause()

def mechanic_perf_report():
    df = fetch_df("""SELECT m.mechanic_id,m.full_name,
                            COUNT(a.assignment_id) AS jobs
                     FROM mechanics_info m
                     LEFT JOIN mechanic_assignments a ON m.mechanic_id=a.mechanic_id
                     GROUP BY m.mechanic_id,m.full_name
                     ORDER BY jobs DESC""")
    print(df.to_string(index=False) if not df.empty else f"{BRIGHT_RED}No data.")
    pause()

def low_stock_report():
    threshold = int(input("Low stock threshold: ").strip() or 5)
    df = fetch_df("""SELECT part_id,part_name,stock_quantity
                     FROM parts_inventory
                     WHERE stock_quantity <= %s
                     ORDER BY stock_quantity ASC, part_name""", (threshold,))
    print(df.to_string(index=False) if not df.empty else f"{BRIGHT_GREEN}All good. No low stock!")
    pause()

def export_all_reports_csv():
    reports = {
        "revenue_daily.csv": """SELECT DATE(invoice_date) d, SUM(amount) revenue
                                FROM invoices GROUP BY d ORDER BY d DESC""",
        "top_services.csv": """SELECT s.service_id,s.service_name,COUNT(b.booking_id) AS bookings
                               FROM services s LEFT JOIN service_bookings b ON s.service_id=b.service_id
                               GROUP BY s.service_id,s.service_name ORDER BY bookings DESC""",
        "mechanic_perf.csv": """SELECT m.mechanic_id,m.full_name,COUNT(a.assignment_id) AS jobs
                                FROM mechanics_info m LEFT JOIN mechanic_assignments a ON m.mechanic_id=a.mechanic_id
                                GROUP BY m.mechanic_id,m.full_name ORDER BY jobs DESC""",
        "low_stock.csv": """SELECT part_id,part_name,stock_quantity
                            FROM parts_inventory WHERE stock_quantity <= 5
                            ORDER BY stock_quantity ASC, part_name""",
    }
    for fname, sql in reports.items():
        df = fetch_df(sql)
        if df.empty:
            continue
        df.to_csv(fname, index=False)
        print(f"{BRIGHT_GREEN}Exported {fname}")
    pause()

# ================== SUBMENUS (items) ==================
USERS_MENU = [
    "1. Create User",
    "2. List / Search Users",
    "3. Update User",
    "4. Delete User",
    "5. Change Role",
    "6. Reset Password",
    "7. Back",
]
VEHICLES_MENU = [
    "1. Add Vehicle to User",
    "2. List / Search Vehicles",
    "3. Edit Vehicle",
    "4. Delete Vehicle",
    "5. Service Catalog ▶",
    "6. Back",
]
SERVICES_MENU = [
    "1. Add Service",
    "2. List / Search Services",
    "3. Update (price/hours/warranty/desc)",
    "4. Activate / Deactivate",
    "5. Delete Service",
    "6. Back",
]
BOOKINGS_MENU = [
    "1. Create Booking",
    "2. List / Filter by Status",
    "3. Update Status",
    "4. Change Service",
    "5. Assign Mechanic",
    "6. Cancel Booking",
    "7. Back",
]
MECHANICS_MENU = [
    "1. Add Mechanic",
    "2. List / Search Mechanics",
    "3. Update Mechanic",
    "4. Delete Mechanic",
    "5. View Assignments / Workload",
    "6. Back",
]
INVENTORY_MENU = [
    "1. Add Part",
    "2. List / Search Parts",
    "3. Update Part",
    "4. Adjust Stock (In/Out)",
    "5. Delete Part",
    "6. Approve Parts Requests",
    "7. Back",
]
INVOICES_MENU = [
    "1. Generate Invoice",
    "2. List / Search Invoices",
    "3. Mark Payment",
    "4. Refund / Adjustment",
    "5. Back",
]
FEEDBACK_MENU = [
    "1. List All Feedback",
    "2. Filter (Min Rating)",
    "3. Export CSV",
    "4. Back",
]
REPORTS_MENU = [
    "1. Revenue (D/W/M)",
    "2. Top Services / Categories",
    "3. Mechanic Performance",
    "4. Low Stock Parts",
    "5. Export All (CSV)",
    "6. Back",
]

# ================== SUBMENUS (callbacks) ==================
def submenu_manage_users(_):
    while True:
        ch = menu_box("👥 MANAGE USERS", USERS_MENU)
        DISPATCH = {
            "1": create_user,
            "2": list_users,
            "3": update_user,
            "4": delete_user,
            "5": change_role,
            "6": reset_password,
            "7": lambda: "BACK",
        }
        fn = DISPATCH.get(ch)
        if not fn:
            print(f"{BRIGHT_RED}❌ Invalid choice."); pause(); continue
        if fn() == "BACK":
            return

def submenu_vehicles(admin_df):
    while True:
        ch = menu_box("🚗 VEHICLES", VEHICLES_MENU)
        DISPATCH = {
            "1": add_vehicle,
            "2": list_vehicles,
            "3": edit_vehicle,
            "4": delete_vehicle,
            "5": lambda: submenu_services(admin_df),
            "6": lambda: "BACK",
        }
        fn = DISPATCH.get(ch)
        if not fn:
            print(f"{BRIGHT_RED}❌ Invalid choice."); pause(); continue
        if fn() == "BACK":
            return

def submenu_services(_):
    while True:
        ch = menu_box("🧩 SERVICE CATALOG", SERVICES_MENU)
        DISPATCH = {
            "1": add_service,
            "2": list_services,
            "3": update_service,
            "4": toggle_service,
            "5": delete_service,
            "6": lambda: "BACK",
        }
        fn = DISPATCH.get(ch)
        if not fn:
            print(f"{BRIGHT_RED}❌ Invalid choice."); pause(); continue
        if fn() == "BACK":
            return

def submenu_bookings(_):
    while True:
        ch = menu_box("🗓️ BOOKINGS", BOOKINGS_MENU)
        DISPATCH = {
            "1": create_booking,
            "2": list_bookings,
            "3": update_booking_status,
            "4": change_booking_service,
            "5": assign_mechanic,
            "6": cancel_booking,
            "7": lambda: "BACK",
        }
        fn = DISPATCH.get(ch)
        if not fn:
            print(f"{BRIGHT_RED}❌ Invalid choice."); pause(); continue
        if fn() == "BACK":
            return

def submenu_mechanics(_):
    while True:
        ch = menu_box("🧰 MECHANICS", MECHANICS_MENU)
        DISPATCH = {
            "1": add_mechanic,
            "2": list_mechanics,
            "3": update_mechanic,
            "4": delete_mechanic,
            "5": view_workload,
            "6": lambda: "BACK",
        }
        fn = DISPATCH.get(ch)
        if not fn:
            print(f"{BRIGHT_RED}❌ Invalid choice."); pause(); continue
        if fn() == "BACK":
            return

def submenu_inventory(_):
    while True:
        ch = menu_box("📦 PARTS INVENTORY", INVENTORY_MENU)
        DISPATCH = {
            "1": add_part,
            "2": list_parts,
            "3": update_part,
            "4": adjust_stock,
            "5": delete_part,
            "6": approve_parts_requests,
            "7": lambda: "BACK",
        }
        fn = DISPATCH.get(ch)
        if not fn:
            print(f"{BRIGHT_RED}❌ Invalid choice."); pause(); continue
        if fn() == "BACK":
            return

def submenu_invoices(_):
    while True:
        ch = menu_box("🧾 INVOICES & PAYMENTS", INVOICES_MENU)
        DISPATCH = {
            "1": generate_invoice,
            "2": list_invoices,
            "3": mark_payment,
            "4": refund_adjustment,
            "5": lambda: "BACK",
        }
        fn = DISPATCH.get(ch)
        if not fn:
            print(f"{BRIGHT_RED}❌ Invalid choice."); pause(); continue
        if fn() == "BACK":
            return

def submenu_feedback(_):
    while True:
        ch = menu_box("⭐ FEEDBACK", FEEDBACK_MENU)
        DISPATCH = {
            "1": list_feedback,
            "2": filter_feedback,
            "3": export_feedback_csv,
            "4": lambda: "BACK",
        }
        fn = DISPATCH.get(ch)
        if not fn:
            print(f"{BRIGHT_RED}❌ Invalid choice."); pause(); continue
        if fn() == "BACK":
            return

def submenu_reports(_):
    while True:
        ch = menu_box("📈 REPORTS", REPORTS_MENU)
        DISPATCH = {
            "1": revenue_report,
            "2": top_services_report,
            "3": mechanic_perf_report,
            "4": low_stock_report,
            "5": export_all_reports_csv,
            "6": lambda: "BACK",
        }
        fn = DISPATCH.get(ch)
        if not fn:
            print(f"{BRIGHT_RED}❌ Invalid choice."); pause(); continue
        if fn() == "BACK":
            return

# ================== MAIN DASHBOARD ==================
def admin_dashboard(admin_df):
    try:
        r = admin_df.iloc[0]
        who = str(r.get("name", r.get("username", "Admin")))
        uid = str(r.get("user_id", ""))
    except Exception:
        who, uid = "Admin", ""
    while True:
        title = f"🚘 ADMIN DASHBOARD  (👤 {who}{' | ID: ' + uid if uid else ''})"
        choice = menu_box(title, [
            "1. Manage Users",
            "2. Vehicles",
            "3. Bookings",
            "4. Mechanics",
            "5. Inventory",
            "6. Invoices",
            "7. Feedback",
            "8. Reports",
            "9. Logout / Back",
        ])
        DISPATCH = {
            "1": lambda: submenu_manage_users(admin_df),
            "2": lambda: submenu_vehicles(admin_df),
            "3": lambda: submenu_bookings(admin_df),
            "4": lambda: submenu_mechanics(admin_df),
            "5": lambda: submenu_inventory(admin_df),
            "6": lambda: submenu_invoices(admin_df),
            "7": lambda: submenu_feedback(admin_df),
            "8": lambda: submenu_reports(admin_df),
            "9": lambda: "BACK",
            "q": lambda: "BACK", "Q": lambda: "BACK", "exit": lambda: "BACK",
        }
        fn = DISPATCH.get(choice)
        if not fn:
            print(f"{BRIGHT_RED}❌ Invalid choice.")
            pause()
            continue
        if fn() == "BACK":
            print(f"{BRIGHT_GREEN}👋 Logged out of Admin Dashboard.")
            break
