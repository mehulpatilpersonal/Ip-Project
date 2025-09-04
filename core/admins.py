from db.queries_sql import sql_connect, mycon, cursor, engcon
import pandas as pd
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

def admin_dashboard(admin_df):
    """
    CLI Admin Dashboard — follows the 8-module flowchart:
    1. Manage Users
    2. Vehicles
    3. Bookings
    4. Mechanics
    5. Inventory
    6. Invoices
    7. Feedback
    8. Reports
    """
    # Pull a friendly name from admin_df (fallbacks if cols not present)
    try:
        row0 = admin_df.iloc[0]
        admin_name = str(row0.get('name', row0.get('username', 'Admin')))
        admin_id = str(row0.get('user_id', ''))
    except Exception:
        admin_name, admin_id = "Admin", ""

    def header():
        print("\n" + "=" * 64)
        print(f"{BRIGHT_YELLOW}🚘 VEHICLE GARAGE MANAGEMENT SYSTEM — ADMIN DASHBOARD")
        print(f"👤 Logged in as: {admin_name}")
        print("=" * 64)

    handlers = {
        "1": admin_manage_users,
        "2": admin_manage_vehicles,
        "3": admin_manage_bookings,
        "4": admin_manage_mechanics,
        "5": admin_manage_inventory,
        "6": admin_manage_invoices,
        "7": admin_view_feedback,
        "8": admin_view_reports,
    }

    while True:
        header()
        print("1) Manage Users")
        print("2) Vehicles")
        print("3) Bookings")
        print("4) Mechanics")
        print("5) Inventory")
        print("6) Invoices")
        print("7) Feedback")
        print("8) Reports")
        print("9) Logout / Back\n")

        choice = input(f"{BRIGHT_YELLOW}Select an option [1-9]: ").strip()

        if choice in handlers:
            handlers[choice](admin_df)  # pass the admin details DataFrame to each stub
        elif choice == "9" or choice.lower() in {"q", "quit", "exit", "0"}:
            print(f"{BRIGHT_GREEN}👋 Logged out of Admin Dashboard.")
            break
        else:
            print(f"{BRIGHT_RED}❌ Invalid choice. Please select 1-9.")
            pause()

# -----------------------
# Stub Handlers (placeholders)
# Replace bodies with your real implementations later.
# Each receives `admin_df` so you can inspect/authorize if needed.
# -----------------------

def pause(msg="Press Enter to return to the dashboard..."):
    try:
        input(f"{DIM_YELLOW}{msg}")
    except EOFError:
        pass

def admin_manage_users(admin_df):
    print("\n" + "-" * 48)
    print("👥 MANAGE USERS")
    print("-" * 48)
    print("TODO: Add/Update/Delete users, reset passwords, assign roles.")
    pause()

def admin_manage_vehicles(admin_df):
    print("\n" + "-" * 48)
    print("🚗 VEHICLES")
    print("-" * 48)
    print("TODO: View/Edit/Delete vehicles.")
    pause()

def admin_manage_bookings(admin_df):
    print("\n" + "-" * 48)
    print("🗓️ SERVICE BOOKINGS")
    print("-" * 48)
    print("TODO: View/Approve/Cancel bookings; track status (Pending/In Progress/Completed/Cancelled).")
    pause()

def admin_manage_mechanics(admin_df):
    print("\n" + "-" * 48)
    print("🧰 MECHANICS")
    print("-" * 48)
    print("TODO: Add/Update/Delete mechanics; assign to bookings; monitor workload/performance.")
    pause()

def admin_manage_inventory(admin_df):
    print("\n" + "-" * 48)
    print("📦 PARTS INVENTORY")
    print("-" * 48)
    print("TODO: Add/Update/Delete parts; manage stock, suppliers, pricing; approve/reject parts requests.")
    pause()

def admin_manage_invoices(admin_df):
    print("\n" + "-" * 48)
    print("🧾 INVOICES & PAYMENTS")
    print("-" * 48)
    print("TODO: Generate invoices; verify payments (Pending/Paid/Failed); handle refunds/adjustments.")
    pause()

def admin_view_feedback(admin_df):
    print("\n" + "-" * 48)
    print("⭐ FEEDBACK")
    print("-" * 48)
    print("TODO: View customer feedback and ratings; filter by service/mechanic/date.")
    pause()

def admin_view_reports(admin_df):
    print("\n" + "-" * 48)
    print("📈 REPORTS")
    print("-" * 48)
    print("TODO: Generate revenue/service/parts usage reports (daily/weekly/monthly). Export CSV/PDF.")
    pause()
