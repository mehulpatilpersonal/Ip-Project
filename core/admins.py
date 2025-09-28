from db.queries_sql import sql_connect, mycon, cursor, engcon
import pandas as pd
from tabulate import tabulate
from styles import *  # colors

# =========== tiny UI helpers ===========

def pause(msg="Press Enter to continue..."):
    try:
        input(f"{DIM_YELLOW}{msg}")
    except EOFError:
        pass

def menu_box(title, items, ask=True, prompt="Select an option: "):
    print(f"\n{BRIGHT_YELLOW}{title}{RESET}")
    print(tabulate([[i] for i in items], tablefmt="fancy_grid"))
    return input(f"{BRIGHT_YELLOW}{prompt}{RESET}").strip() if ask else None

# =========== auth ===========

def admin_login():
    while True:
        u = input(f"{BRIGHT_YELLOW}ENTER ADMIN USERNAME: {RESET}").strip()
        p = input(f"{BRIGHT_YELLOW}ENTER ADMIN PASSWORD: {RESET}").strip()
        if not (u and p):
            print(f"{BRIGHT_RED}❌ Username & Password required.{RESET}")
            if input(f"{DIM_YELLOW}Press Enter or type 'exit': {RESET}").lower() == "exit":
                return
            continue

        df = pd.read_sql(
            "SELECT * FROM users WHERE username=%s AND password=%s AND user_role='admin'",
            con=engcon, params=(u, p)
        )
        if not df.empty:
            print(f"\n{BRIGHT_GREEN}✅ ADMIN LOGIN SUCCESSFUL!{RESET}\n")
            cols = [c for c in ("user_id","username","user_role") if c in df.columns]
            if cols: print(df[cols].head(1))
            admin_dashboard(df)
            return
        print(f"{BRIGHT_RED}❌ Invalid credentials.{RESET}")

# =========== dashboard (super compact) ===========

SUBMENUS = {
    "1": ("👥 MANAGE USERS", [
        "1. Create User",
        "2. List / Search Users",
        "3. Update User",
        "4. Delete User",
        "5. Change Role",
        "6. Reset Password",
        "7. Back",
    ]),
    "2": ("🚗 VEHICLES", [
        "1. Add Vehicle to User",
        "2. List / Search Vehicles",
        "3. Edit Vehicle",
        "4. Delete Vehicle",
        "5. Service Catalog ▶",
        "6. Back",
    ]),
    "3": ("🗓️ BOOKINGS", [
        "1. Create Booking",
        "2. List / Filter by Status",
        "3. Update Status",
        "4. Change Service",
        "5. Assign Mechanic",
        "6. Cancel Booking",
        "7. Back",
    ]),
    "4": ("🧰 MECHANICS", [
        "1. Add Mechanic",
        "2. List / Search Mechanics",
        "3. Update Mechanic",
        "4. Delete Mechanic",
        "5. View Assignments / Workload",
        "6. Back",
    ]),
    "5": ("📦 INVENTORY", [
        "1. Add Part",
        "2. List / Search Parts",
        "3. Update Part",
        "4. Adjust Stock (In/Out)",
        "5. Delete Part",
        "6. Approve Parts Requests",
        "7. Back",
    ]),
    "6": ("🧾 INVOICES & PAYMENTS", [
        "1. Generate Invoice",
        "2. List / Search Invoices",
        "3. Mark Payment",
        "4. Refund / Adjustment",
        "5. Back",
    ]),
    "7": ("⭐ FEEDBACK", [
        "1. List All Feedback",
        "2. Filter (Mechanic/Service/Date)",
        "3. Export CSV",
        "4. Back",
    ]),
    "8": ("📈 REPORTS", [
        "1. Revenue (D/W/M)",
        "2. Top Services / Categories",
        "3. Mechanic Performance",
        "4. Low Stock Parts",
        "5. Export All (CSV)",
        "6. Back",
    ]),
}

def handle_action(title, label):
    """One-liner stub executor—replace prints with real SQL later."""
    print(f"\n{BRIGHT_CYAN}{title}{RESET} → {label}")
    print(f"{DIM_YELLOW}TODO: implement DB logic here.{RESET}")
    pause()

def submenu_services(admin_df):
    title = "🧩 SERVICE CATALOG"
    while True:
        ch = menu_box(title, [
            "1. Add Service",
            "2. List / Search Services",
            "3. Update (price/hours/warranty/desc)",
            "4. Activate / Deactivate",
            "5. Delete Service",
            "6. Back",
        ])
        if ch == "1": handle_action(title, "INSERT INTO services(...) VALUES(...)")
        elif ch == "2": handle_action(title, "SELECT * FROM services ...")
        elif ch == "3": handle_action(title, "UPDATE services SET ... WHERE service_id=?")
        elif ch == "4": handle_action(title, "UPDATE services SET status='Active'|'Inactive' WHERE service_id=?")
        elif ch == "5": handle_action(title, "DELETE FROM services WHERE service_id=?")
        elif ch == "6": return
        else: print(f"{BRIGHT_RED}❌ Invalid choice.{RESET}")

def run_submenu(key, admin_df):
    title, items = SUBMENUS[key]
    while True:
        ch = menu_box(title, items)
        # Quick routes per submenu (just a few examples wired)
        if key == "2" and ch == "5":          # Vehicles -> Service Catalog
            submenu_services(admin_df)
        elif ch in {"7","6","5","4"} and "Back" in items[int(ch)-1]:  # handles Back on any submenu
            return
        else:
            # generic stub
            idx = int(ch) if ch.isdigit() and 1 <= int(ch) <= len(items) else None
            if idx is None:
                print(f"{BRIGHT_RED}❌ Invalid choice.{RESET}")
            else:
                handle_action(title, items[idx-1])

def admin_dashboard(admin_df):
    # show name/id nicely if available
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
        if choice in SUBMENUS:     # open respective submenu
            run_submenu(choice, admin_df)
        elif choice in {"9","q","Q","exit"}:
            print(f"{BRIGHT_GREEN}👋 Logged out of Admin Dashboard.{RESET}")
            break
        else:
            print(f"{BRIGHT_RED}❌ Invalid choice.{RESET}")
            pause()
