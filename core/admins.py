from db.queries_sql import sql_connect, mycon, cursor, engcon
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import stdiomask
from styles import *  # Import style constants


def admin_login():
    while True:
        username = input(f"{BRIGHT_YELLOW}ENTER ADMIN USERNAME: ")
        password = input(f"{BRIGHT_YELLOW}ENTER ADMIN PASSWORD: ")
        if username and password:
            query = """select * from users where username=%s and password=%s and user_role='admin'"""
            df = pd.read_sql(query, con=engcon, params=(username, password))
            if not df.empty:
                print(f"\n{BRIGHT_GREEN}✅ ADMIN LOGIN SUCCESSFUL!\n")
                print(df[['user_id', 'username', 'user_role']])
                admin_dashboard(df)  # Call the admin dashboard function
                break
        else:
            print(f"{BRIGHT_RED}❌ Invalid credentials, please try again.")
            k = input(f"{DIM_YELLOW}Press Enter to continue... or 'exit' to quit: ")
            if k.lower() == 'exit':
                print(f"{BRIGHT_RED}Exiting login.")
                return

# def admin_dashboard(admin_df):
#     """
#     CLI Admin Dashboard — follows the 8-module flowchart:
#     1. Manage Users
#     2. Vehicles
#     3. Bookings
#     4. Mechanics
#     5. Inventory
#     6. Invoices
#     7. Feedback
#     8. Reports
#     """
#     # Pull a friendly name from admin_df (fallbacks if cols not present)
#     try:
#         row0 = admin_df.iloc[0]
#         admin_name = str(row0.get('name', row0.get('username', 'Admin')))
#         admin_id = str(row0.get('user_id', ''))
#     except Exception:
#         admin_name, admin_id = "Admin", ""

#     def header():
#         print("\n" + "=" * 64)
#         print(f"{BRIGHT_YELLOW}🚘 VEHICLE GARAGE MANAGEMENT SYSTEM — ADMIN DASHBOARD")
#         print(f"👤 Logged in as: {admin_name}")
#         print("=" * 64)

#     handlers = {
#         "1": admin_manage_users,
#         "2": admin_manage_vehicles,
#         "3": admin_manage_bookings,
#         "4": admin_manage_mechanics,
#         "5": admin_manage_inventory,
#         "6": admin_manage_invoices,
#         "7": admin_view_feedback,
#         "8": admin_view_reports,
#     }

#     while True:
#         header()
#         print("1) Manage Users")
#         print("2) Vehicles")
#         print("3) Bookings")
#         print("4) Mechanics")
#         print("5) Inventory")
#         print("6) Invoices")
#         print("7) Feedback")
#         print("8) Reports")
#         print("9) Logout / Back\n")

#         choice = input(f"{BRIGHT_YELLOW}Select an option [1-9]: ").strip()

#         if choice in handlers:
#             handlers[choice](admin_df)  # pass the admin details DataFrame to each stub
#         elif choice == "9" or choice.lower() in {"q", "quit", "exit", "0"}:
#             print(f"{BRIGHT_GREEN}👋 Logged out of Admin Dashboard.")
#             break
#         else:
#             print(f"{BRIGHT_RED}❌ Invalid choice. Please select 1-9.")
#             pause()

# -----------------------
# Stub Handlers (placeholders)
# Replace bodies with your real implementations later.
# Each receives `admin_df` so you can inspect/authorize if needed.
# -----------------------

# ---------- Small UI helpers ----------

def pause(msg="Press Enter to return..."):
    try:
        input(f"{DIM_YELLOW}{msg}")
    except EOFError:
        pass

# def menu_box(title, items):
#     print("\n+----------------------+")
#     print(f"| {title:<20}|")
#     print("+----------------------+")
#     for row in items:
#         print(f"| {row:<20}|")
#     print("+----------------------+")

def menu_box(title, items, input_displaytext="Select an option:  ",ask_input=True):
    table = [[row] for row in items]  # convert list into rows
    print(f"\n=== {title} ===")
    print(tabulate(table, tablefmt="fancy_grid"))
    return input(f"{BRIGHT_YELLOW}{input_displaytext}").strip() if ask_input else None  #I have used short hand if else here if input is not required then ask_input is false and it returns None


def print_header(section):
    print("\n" + "-" * 60)
    print(f"{BRIGHT_YELLOW}{section}")
    print("-" * 60)

# ---------- MAIN DASHBOARD ----------

def admin_dashboard(admin_df):
    # Name/id display from your DataFrame
    try:
        row0 = admin_df.iloc[0]
        admin_name = str(row0.get("name", row0.get("username", "Admin")))
        admin_id = str(row0.get("user_id", ""))
    except Exception:
        admin_name, admin_id = "Admin", ""

    while True:
        title = f"🚘 ADMIN DASHBOARD  (👤 {admin_name}{' | ID: ' + admin_id if admin_id else ''})"
        choice = menu_box(
            title,
            [
                "1. Manage Users",
                "2. Vehicles",
                "3. Bookings",
                "4. Mechanics",
                "5. Inventory",
                "6. Invoices",
                "7. Feedback",
                "8. Reports",
                "9. Logout / Back",
            ],
        )

        if choice == "1":
            submenu_manage_users(admin_df)
        elif choice == "2":
            submenu_vehicles(admin_df)
        elif choice == "3":
            submenu_bookings(admin_df)
        elif choice == "4":
            submenu_mechanics(admin_df)
        elif choice == "5":
            submenu_inventory(admin_df)
        elif choice == "6":
            submenu_invoices(admin_df)
        elif choice == "7":
            submenu_feedback(admin_df)
        elif choice == "8":
            submenu_reports(admin_df)
        elif choice in {"9", "q", "Q", "exit"}:
            print(f"{BRIGHT_GREEN}👋 Logged out of Admin Dashboard.")
            break
        else:
            print(f"{BRIGHT_RED}❌ Invalid choice.")
            pause()

# ---------- SUB-MENUS (all stubs; wire DB logic later) ----------

def submenu_manage_users(admin_df):
    while True:
        choice = menu_box(
            "👥 MANAGE USERS",
            [
                "1. Create User",
                "2. List / Search Users",
                "3. Update User",
                "4. Delete User",
                "5. Change Role (Customer/Mechanic/Admin)",
                "6. Reset Password",
                "7. Back",
            ],
        )
        if choice == "1":
            print_header("Create User")
            print("TODO: INSERT INTO users (...) VALUES (...);")
            pause()
        elif choice == "2":
            print_header("List / Search Users")
            print("TODO: SELECT * FROM users [WHERE ...] ORDER BY registered_at DESC;")
            pause()
        elif choice == "3":
            print_header("Update User")
            print("TODO: UPDATE users SET ... WHERE user_id = ?;")
            pause()
        elif choice == "4":
            print_header("Delete User")
            print("TODO: DELETE FROM users WHERE user_id = ?;")
            pause()
        elif choice == "5":
            print_header("Change Role")
            print("TODO: UPDATE users SET user_role = ? WHERE user_id = ?;")
            pause()
        elif choice == "6":
            print_header("Reset Password")
            print("TODO: UPDATE users SET password = ? WHERE user_id = ?;")
            pause()
        elif choice == "7":
            return
        else:
            print(f"{BRIGHT_RED}❌ Invalid choice.")
            pause()

def submenu_vehicles(admin_df):
    while True:
        choice = menu_box(
            "🚗 VEHICLES",
            [
                "1. Add Vehicle to a User",
                "2. List / Search Vehicles",
                "3. Edit Vehicle",
                "4. Delete Vehicle",
                "5. Service Catalog (Add / Update / Activate / Deactivate)",
                "6. Back",
            ],
        )
        if choice == "1":
            print_header("Add Vehicle")
            print("TODO: INSERT INTO vehicles (vehicle_no, brand, model, type, user_id) VALUES (...);")
            pause()
        elif choice == "2":
            print_header("List / Search Vehicles")
            print("TODO: SELECT v.*, u.name FROM vehicles v JOIN users u ON v.user_id=u.user_id [WHERE ...];")
            pause()
        elif choice == "3":
            print_header("Edit Vehicle")
            print("TODO: UPDATE vehicles SET ... WHERE vehicle_no = ?;")
            pause()
        elif choice == "4":
            print_header("Delete Vehicle")
            print("TODO: DELETE FROM vehicles WHERE vehicle_no = ?;")
            pause()
        elif choice == "5":
            submenu_services(admin_df)
        elif choice == "6":
            return
        else:
            print(f"{BRIGHT_RED}❌ Invalid choice.")
            pause()

def submenu_services(admin_df):
    # Manages `services` table (since Admin needs “Add Services / Update status”)
    while True:
        choice = menu_box(
            "🧩 SERVICE CATALOG",
            [
                "1. Add Service",
                "2. List / Search Services",
                "3. Update Service (price/hours/warranty/desc)",
                "4. Activate / Deactivate Service",
                "5. Delete Service",
                "6. Back",
            ],
        )
        if choice == "1":
            print_header("Add Service")
            print("TODO: INSERT INTO services(service_name, description, base_price, estimated_hours, warranty_months, category, status) VALUES (...);")
            pause()
        elif choice == "2":
            print_header("List / Search Services")
            print("TODO: SELECT * FROM services [WHERE status='Active' AND ...] ORDER BY created_at DESC;")
            pause()
        elif choice == "3":
            print_header("Update Service")
            print("TODO: UPDATE services SET base_price=?, estimated_hours=?, warranty_months=?, description=?, category=? WHERE service_id=?;")
            pause()
        elif choice == "4":
            print_header("Activate / Deactivate Service")
            print("TODO: UPDATE services SET status='Active'|'Inactive' WHERE service_id=?;")
            pause()
        elif choice == "5":
            print_header("Delete Service")
            print("TODO: DELETE FROM services WHERE service_id=?;")
            pause()
        elif choice == "6":
            return
        else:
            print(f"{BRIGHT_RED}❌ Invalid choice.")
            pause()

def submenu_bookings(admin_df):
    while True:
        choice = menu_box(
            "🗓️ BOOKINGS",
            [
                "1. Create Booking",
                "2. List All / Filter by Status",
                "3. Update Status (Pending/In Progress/Completed/Cancelled)",
                "4. Add / Change Service for Booking",
                "5. Assign Mechanic to Booking",
                "6. Cancel Booking",
                "7. Back",
            ],
        )
        if choice == "1":
            print_header("Create Booking")
            print("TODO: INSERT INTO service_bookings(vehicle_no, service_id, booking_date, status) VALUES (...);")
            pause()
        elif choice == "2":
            print_header("List / Filter Bookings")
            print("TODO: SELECT b.*, s.service_name, v.vehicle_no FROM service_bookings b JOIN services s ON b.service_id=s.service_id JOIN vehicles v ON b.vehicle_no=v.vehicle_no [WHERE status=?];")
            pause()
        elif choice == "3":
            print_header("Update Booking Status")
            print("TODO: UPDATE service_bookings SET status=? WHERE booking_id=?;")
            pause()
        elif choice == "4":
            print_header("Add / Change Service for Booking")
            print("TODO: UPDATE service_bookings SET service_id=? WHERE booking_id=?;")
            pause()
        elif choice == "5":
            print_header("Assign Mechanic")
            print("TODO: INSERT/UPDATE mechanic_assignments(booking_id, mechanic_id, assigned_date) ...;")
            pause()
        elif choice == "6":
            print_header("Cancel Booking")
            print("TODO: UPDATE service_bookings SET status='Cancelled' WHERE booking_id=?;")
            pause()
        elif choice == "7":
            return
        else:
            print(f"{BRIGHT_RED}❌ Invalid choice.")
            pause()

def submenu_mechanics(admin_df):
    while True:
        choice = menu_box(
            "🧰 MECHANICS",
            [
                "1. Add Mechanic",
                "2. List / Search Mechanics",
                "3. Update Mechanic",
                "4. Delete Mechanic",
                "5. View Assignments / Workload",
                "6. Back",
            ],
        )
        if choice == "1":
            print_header("Add Mechanic")
            print("TODO: INSERT INTO mechanics_info(full_name, specialization, phone, email) VALUES (...);")
            pause()
        elif choice == "2":
            print_header("List / Search Mechanics")
            print("TODO: SELECT * FROM mechanics_info [WHERE specialization LIKE ...];")
            pause()
        elif choice == "3":
            print_header("Update Mechanic")
            print("TODO: UPDATE mechanics_info SET ... WHERE mechanic_id=?;")
            pause()
        elif choice == "4":
            print_header("Delete Mechanic")
            print("TODO: DELETE FROM mechanics_info WHERE mechanic_id=?;")
            pause()
        elif choice == "5":
            print_header("View Assignments / Workload")
            print("TODO: SELECT m.full_name, COUNT(a.assignment_id) jobs FROM mechanics_info m LEFT JOIN mechanic_assignments a ON m.mechanic_id=a.mechanic_id GROUP BY m.mechanic_id;")
            pause()
        elif choice == "6":
            return
        else:
            print(f"{BRIGHT_RED}❌ Invalid choice.")
            pause()

def submenu_inventory(admin_df):
    while True:
        choice = menu_box(
            "📦 PARTS INVENTORY",
            [
                "1. Add Part",
                "2. List / Search Parts",
                "3. Update Part Details",
                "4. Adjust Stock (In/Out)",
                "5. Delete Part",
                "6. Approve Parts Requests (from Mechanics)",
                "7. Back",
            ],
        )
        if choice == "1":
            print_header("Add Part")
            print("TODO: INSERT INTO parts_inventory(part_name, description, unit_price, stock_quantity, supplier) VALUES (...);")
            pause()
        elif choice == "2":
            print_header("List / Search Parts")
            print("TODO: SELECT * FROM parts_inventory [WHERE part_name LIKE ...];")
            pause()
        elif choice == "3":
            print_header("Update Part")
            print("TODO: UPDATE parts_inventory SET description=?, unit_price=?, supplier=? WHERE part_id=?;")
            pause()
        elif choice == "4":
            print_header("Adjust Stock")
            print("TODO: UPDATE parts_inventory SET stock_quantity = stock_quantity +/- ? WHERE part_id=?;")
            pause()
        elif choice == "5":
            print_header("Delete Part")
            print("TODO: DELETE FROM parts_inventory WHERE part_id=?;")
            pause()
        elif choice == "6":
            print_header("Approve Parts Requests")
            print("TODO: Create a parts_requests table or workflow; approve/reject & deduct stock accordingly.")
            pause()
        elif choice == "7":
            return
        else:
            print(f"{BRIGHT_RED}❌ Invalid choice.")
            pause()

def submenu_invoices(admin_df):
    while True:
        choice = menu_box(
            "🧾 INVOICES & PAYMENTS",
            [
                "1. Generate Invoice for Booking",
                "2. List / Search Invoices",
                "3. Mark Payment (Paid/Pending/Failed)",
                "4. Refund / Adjustment",
                "5. Back",
            ],
        )
        if choice == "1":
            print_header("Generate Invoice")
            print("TODO: INSERT INTO invoices(booking_id, user_id, amount, payment_status, payment_method, invoice_date) VALUES (...);")
            pause()
        elif choice == "2":
            print_header("List / Search Invoices")
            print("TODO: SELECT i.*, u.name FROM invoices i JOIN users u ON i.user_id=u.user_id [WHERE payment_status=?];")
            pause()
        elif choice == "3":
            print_header("Mark Payment")
            print("TODO: UPDATE invoices SET payment_status=?, payment_method=? WHERE invoice_id=?;")
            pause()
        elif choice == "4":
            print_header("Refund / Adjustment")
            print("TODO: UPDATE invoices SET amount = amount - ? WHERE invoice_id=?; (and log it)")
            pause()
        elif choice == "5":
            return
        else:
            print(f"{BRIGHT_RED}❌ Invalid choice.")
            pause()

def submenu_feedback(admin_df):
    while True:
        choice = menu_box(
            "⭐ FEEDBACK",
            [
                "1. List All Feedback",
                "2. Filter by Mechanic / Service / Date",
                "3. Export Feedback (CSV)",
                "4. Back",
            ],
        )
        if choice == "1":
            print_header("List All Feedback")
            print("TODO: SELECT f.*, s.service_name, b.booking_id FROM feedback f JOIN service_bookings b ON f.booking_id=b.booking_id JOIN services s ON s.service_id=b.service_id;")
            pause()
        elif choice == "2":
            print_header("Filter Feedback")
            print("TODO: Add filters; WHERE rating>=? AND mechanic_id=? AND date BETWEEN ? AND ?;")
            pause()
        elif choice == "3":
            print_header("Export Feedback (CSV)")
            print("TODO: Use pandas to_csv(...) after SELECT.")
            pause()
        elif choice == "4":
            return
        else:
            print(f"{BRIGHT_RED}❌ Invalid choice.")
            pause()

def submenu_reports(admin_df):
    while True:
        choice = menu_box(
            "📈 REPORTS",
            [
                "1. Revenue Report (Daily/Weekly/Monthly)",
                "2. Top Services / Categories",
                "3. Mechanic Performance",
                "4. Low Stock Parts",
                "5. Export All Reports (CSV)",
                "6. Back",
            ],
        )
        if choice == "1":
            print_header("Revenue Report")
            print("TODO: SUM(i.amount) BY DATE; JOIN invoices i -> service_bookings b -> services s.")
            pause()
        elif choice == "2":
            print_header("Top Services / Categories")
            print("TODO: COUNT(bookings) GROUP BY service_id / category; ORDER BY desc.")
            pause()
        elif choice == "3":
            print_header("Mechanic Performance")
            print("TODO: COUNT(assignments, completed jobs), avg rating from feedback, avg hours, etc.")
            pause()
        elif choice == "4":
            print_header("Low Stock Parts")
            print("TODO: SELECT * FROM parts_inventory WHERE stock_quantity <= ? ORDER BY stock_quantity ASC;")
            pause()
        elif choice == "5":
            print_header("Export All Reports (CSV)")
            print("TODO: Use pandas to export results of above queries to CSV.")
            pause()
        elif choice == "6":
            return
        else:
            print(f"{BRIGHT_RED}❌ Invalid choice.")
            pause()
