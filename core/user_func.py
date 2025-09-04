import pandas as pd
import matplotlib.pyplot as plt
import stdiomask
from db.queries_sql import mycon, cursor, engine, engcon

from styles import *  # Import style constants


def user_rejisteration():
    while True:
        name = input(f"{BRIGHT_YELLOW}ENTER YOUR NAME: ").strip()
        if name.replace(" ", "").isalpha():
            break
        print(f"{BRIGHT_RED}❌ INVALID NAME. Please enter a valid name (letters only).")

    while True:
        email = input(f"{BRIGHT_YELLOW}ENTER YOUR EMAIL: ").strip()
        # Simple email regex
        if '@' in email and '.' in email:
            break
        print(f"{BRIGHT_RED}❌ INVALID EMAIL. Please enter a valid email address.")

    while True:
        phone = input(f"{BRIGHT_YELLOW}ENTER YOUR PHONE NUMBER: ").strip()
        if phone.isdigit() and len(phone) in [10, 11, 12]:
            break
        print(f"{BRIGHT_RED}❌ INVALID PHONE NUMBER. Please enter a valid number (10-12 digits).")

    address = input(f"{BRIGHT_YELLOW}ENTER YOUR ADDRESS: ").strip()
    city = input(f"{BRIGHT_YELLOW}ENTER YOUR CITY: ").strip()
    state = input(f"{BRIGHT_YELLOW}ENTER YOUR STATE: ").strip()
    while True:
        username = input(f"{BRIGHT_YELLOW}CREATE YOUR NEW USERNAME: ").strip()
        if username:
            break
        print(f"{BRIGHT_RED}❌ USERNAME CANNOT BE EMPTY.")
    
    while True:
        password = stdiomask.getpass(prompt=f"{BRIGHT_YELLOW}ENTER NEW PASSWORD: ", mask='*')
        confirm_password = stdiomask.getpass(prompt=f"{BRIGHT_YELLOW}CONFIRM YOUR PASSWORD: ", mask='*')
        if len(password) < 6:
            print(f"{BRIGHT_RED}❌ PASSWORD TOO SHORT. Must be at least 6 characters.")
            continue
        if password != confirm_password:
            print(f"{BRIGHT_RED}❌ PASSWORDS DO NOT MATCH. Please try again.")
            continue
        break
    Entry_df = pd.DataFrame({  # I AM USING SCALAR VALUES HERE SO THEREFORE [ ] is mandatory
        'name': [name],
        'email': [email],
        'phone': [phone],
        'address': [address],
        'city': [city],
        'state': [state],
        'username': [username],
        'password': [password]
    })
    Entry_df.to_sql('users', con=engcon, if_exists='append', index=False)
    print(f"{BRIGHT_GREEN}✅ REGISTRATION SUCCESSFUL! You can now log in.")

def user_login():
    while True:
        username = input(f"{BRIGHT_YELLOW}ENTER YOUR USERNAME or Email: ").strip()
        password = stdiomask.getpass(prompt=f"{BRIGHT_YELLOW}ENTER YOUR PASSWORD: ", mask='*')
        
        if username and password:  # Placeholder for actual authentication logic
            query = """
                SELECT * FROM users 
                WHERE (username = %s OR email = %s) AND password = %s
            """
            logindf = pd.read_sql(query, con=engcon, params=(username, username, password))

            if not logindf.empty:
                print(f"\n{BRIGHT_GREEN}✅ LOGIN SUCCESSFUL!\n")
                show_info = logindf[['user_id', 'username', 'user_role']].to_string(index=False)
                print(show_info)  # Show some user info
                
                user_dashboard(logindf)  # Proceed to dashboard
                break
            else:
                print(f"\n{BRIGHT_RED}❌ INVALID CREDENTIALS. Please try again.\n")
                k = input(f"{DIM_YELLOW}Press Enter to try again or type 'exit' to quit: ")
                if k.lower() == 'exit':
                    print(f"{BRIGHT_RED}Exiting login.")
                    return
        else:
            print(f"\n{BRIGHT_RED}❌ Both fields are required.\n")

def user_dashboard(logindf):
    currentuserid = logindf.at[0, 'user_id']  # Get user_id of logged-in user
    currentuserid = int(currentuserid)  # DataFrame me int ka type nump.int64 return karta hai isliye integer me convert karna padta hai
    
    #HERE IMPROVING GUI FOR DASHBOARD SHOW DETAILS OF USERS PROPERLY


    while True:
        print(f"\n{BRIGHT_CYAN}===== USER DASHBOARD =====")
        print(f"{BRIGHT_GREEN}Welcome, {logindf.at[0,'name']}!\n")


        print(f"{BRIGHT_YELLOW}1.View / Update Profile")
        print(f"{BRIGHT_YELLOW}2.Add Vehicle")
        print(f"{BRIGHT_YELLOW}3.Manage Vehicles")
        print(f"{BRIGHT_YELLOW}4.Browse Services")
        print(f"{BRIGHT_YELLOW}5.Book Service")
        print(f"{BRIGHT_YELLOW}6.Make Payment")
        print(f"{BRIGHT_YELLOW}7.View Booking History")
        print(f"{BRIGHT_YELLOW}8.Track Order")
        print(f"{BRIGHT_YELLOW}9.Cancel Order")
        print(f"{BRIGHT_YELLOW}10.View / Download Invoice")
        print(f"{BRIGHT_YELLOW}11.Check Payment Status")
        print(f"{BRIGHT_YELLOW}12.Feedback")
        print(f"{BRIGHT_MAGENTA}0. Logout\n")
        print(f"{BRIGHT_RED} Type q or Q  for EXIT")
        print(f"{DIM_YELLOW}Select an option by entering the corresponding number.")


        choice = input(f"{BRIGHT_CYAN}Enter your choice: ").strip()
        if choice.lower() == 'q':
            print(f"{BRIGHT_RED}Exiting dashboard.")
            exit()
        elif choice == "0":
            print(f"{BRIGHT_MAGENTA}↩ Logging out...")
            break
        elif choice == "1":
            view_or_update_profile(currentuserid)
        elif choice == "2":
            add_vehicle(currentuserid)
        elif choice == "3":
            manage_vehicles(currentuserid)
        elif choice == "4":
            browse_services()
        elif choice == "5":
            book_service(currentuserid)
        elif choice == "6":
            make_payment(currentuserid)
        elif choice == "7":
            view_booking_history(currentuserid)
        elif choice == "8":
            track_order(currentuserid)
        elif choice == "9":
            cancel_order(currentuserid)
        elif choice == "10":
            view_or_download_invoice(currentuserid)
        elif choice == "11":
            check_payment_status(currentuserid)
        elif choice == "12":
            leave_feedback(currentuserid)
        else:
            print(f"{BRIGHT_RED}❌ Invalid choice. Try again.")


# === 1) View / Update Profile (with optional password change) ===
def view_or_update_profile(currentuserid):
    # Fetch current profile
    user_q = """
        SELECT user_id, name, email, phone, address, city, state, username, password
        FROM users WHERE user_id = %s
    """
    user_df = pd.read_sql(user_q, con=engcon, params=(currentuserid,))
    if user_df.empty:
        print(f"{BRIGHT_RED}❌ User not found.")
        return

    row = user_df.iloc[0] #return Series object
    print(f"\n{BRIGHT_CYAN}Your Profile")
    print(row[['user_id','name','email','phone','address','city','state','username']].to_string())

    # Ask to update profile details
    ans = input(f"\n{BRIGHT_YELLOW} CHOOSE FROM BELOW \n Press \n 1. To Change Profile Details \n 2. To Change Password \n 3. To Skip and Continue to Dashboard").strip()
    if ans == "1":
        # Inline edit (Press Enter to keeps old value)
        name    = input(f"\nENTER New name  \n OLD WAS:[{row['name']}]: \n Press Enter to Skip : ").strip() or row['name']
        email   = input(f"\nENTER New email \n OLD WAS: [{row['email']}]\n Press Enter to Skip : ").strip() or row['email']
        phone   = input(f"\nENTER New phone \n OLD WAS: [{row['phone']}]\n Press Enter to Skip : ").strip() or row['phone']
        address = input(f"\nENTER New addre \n OLD WAS: [{row['address']}]\n Press Enter to Skip :").strip() or row['address']
        city    = input(f"\nENTER New city  \n OLD WAS:[{row['city']}]: \n Press Enter to Skip :").strip() or row['city']
        state   = input(f"\nENTER New state \n OLD WAS: [{row['state']}]\n Press Enter to Skip : ").strip() or row['state']

        # Preview
        preview_df = pd.DataFrame([{
            "user_id": currentuserid,
            "name": name, "email": email, "phone": phone,
            "address": address, "city": city, "state": state,
            "username": row['username'],
        }])
        print(BRIGHT_CYAN,"\n" + "="*12 + " UPDATED DETAILS PREVIEW " + "="*12)
        print(preview_df.T.to_string(header=False))  # Transposed for better readability

        ask = input("\nPress Enter to confirm update, or type 'b' to cancel and re-enter: ").strip().lower()
        if ask == 'b':
            print(f"{BRIGHT_RED}Cancelled profile update.")
            return

        # Update DB (DETAILS)
        cursor.execute(
            """
            UPDATE users
               SET name=%s, email=%s, phone=%s, address=%s, city=%s, state=%s
             WHERE user_id=%s
            """,
            (name, email, phone, address, city, state, int(currentuserid)),
        )
        mycon.commit()
        #engcon.dispose()  # Dispose/Refresh SQLAlchemy connection so that no old data removing from cache
        print(f"{BRIGHT_GREEN}✅ Profile details updated successfully.")

    # Ask to change password
    if ans != "2":
        return
    print(f"\n{BRIGHT_YELLOW}Change Password")

    # Verify old password
    old_pass = stdiomask.getpass(prompt="Enter OLD password: ", mask='*')
    # Check against DB to avoid stale in-memory copy
    check_df = pd.read_sql(
        "SELECT user_id FROM users WHERE user_id=%s AND password=%s",
        con=engcon, params=(currentuserid, old_pass)
    )
    if check_df.empty:
        print(f"{BRIGHT_RED}❌ Old password is incorrect.")
        return

    # Get new password (with confirmation)
    while True:
        new_pass = stdiomask.getpass(prompt="Enter NEW password (min 6 chars): ", mask='*')
        if len(new_pass) < 6:
            print(f"{BRIGHT_RED}❌ Too short. Try again.")
            continue
        new_pass2 = stdiomask.getpass(prompt="Confirm NEW password: ", mask='*')
        if new_pass != new_pass2:
            print(f"{BRIGHT_RED}❌ Passwords do not match. Try again.")
            continue
        break

    # Update DB (PASSWORD)
    cursor.execute(
        "UPDATE users SET password=%s WHERE user_id=%s",
        (new_pass, currentuserid)
    )
    mycon.commit()
    print(f"{BRIGHT_GREEN}✅ Password changed successfully.")


# === 2) Add Vehicle ===
def add_vehicle(currentuseridid: int):
    print(f"\n{BRIGHT_CYAN}Add Vehicle")
    vehicle_no = input("Vehicle No (unique): ").strip()
    brand = input("Brand: ").strip()
    model = input("Model: ").strip()
    vtype = input("Type (Car/Bike/Truck/Bus/Tractor/Other): ").strip()

    df = pd.DataFrame([{
        "vehicle_no": vehicle_no,
        "vehicle_brand": brand,
        "model": model,
        "type": vtype,
        "user_id": currentuseridid,
    }])
    try:
        df.to_sql("vehicles", con=engcon, if_exists="append", index=False)
        print(f"{BRIGHT_GREEN}✅ Vehicle added.")
    except Exception as e:
        print(f"{BRIGHT_RED}❌ Failed to add vehicle: {e}")


# === 3) Manage Vehicles ===
def manage_vehicles(currentuseridid: int):
    vdf = pd.read_sql(
        "SELECT vehicle_no, vehicle_brand, model, type FROM vehicles WHERE user_id=%s",
        con=engcon, params=(currentuseridid,)
    )
    if vdf.empty:
        print(f"{BRIGHT_RED}No vehicles found.")
        return
    print(f"\n{BRIGHT_CYAN}Your Vehicles")
    print(vdf.to_string(index=False))

    vno = input("Enter Vehicle No to select (blank to cancel): ").strip()
    if not vno:
        return

    print("1) Edit  2) Delete  (else cancel)")
    act = input("Choose: ").strip()
    if act == "1":
        row = vdf[vdf["vehicle_no"].astype(str) == str(vno)].iloc[0]
        brand = input(f"New brand [{row['vehicle_brand']}]: ").strip() or row['vehicle_brand']
        model = input(f"New model [{row['model']}]: ").strip() or row['model']
        vtype = input(f"New type [{row['type']}]: ").strip() or row['type']
        cursor.execute(
            "UPDATE vehicles SET vehicle_brand=%s, model=%s, type=%s WHERE vehicle_no=%s AND user_id=%s",
            (brand, model, vtype, vno, currentuseridid),
        )
        mycon.commit()
        print(f"{BRIGHT_GREEN}✅ Vehicle updated.")
    elif act == "2":
        ans = input(f"Delete vehicle {vno}? (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            cursor.execute(
                "DELETE FROM vehicles WHERE vehicle_no=%s AND user_id=%s",
                (vno, currentuseridid),
            )
            mycon.commit()
            print(f"{BRIGHT_GREEN}✅ Vehicle deleted.")


# === 4) Browse Services ===
def browse_services():
    sdf = pd.read_sql(
        "SELECT service_id, service_name, category, base_price, estimated_hours, warranty_months FROM services WHERE status='Active' ORDER BY category, service_name",
        con=engcon,
    )
    if sdf.empty:
        print(f"{BRIGHT_RED}No active services.")
        return
    print(f"\n{BRIGHT_CYAN}Active Services")
    print(sdf.to_string(index=False))


# === 5) Book Service ===
def book_service(currentuseridid: int):
    vdf = pd.read_sql(
        "SELECT vehicle_no, vehicle_brand, model FROM vehicles WHERE user_id=%s",
        con=engcon, params=(currentuseridid,)
    )
    if vdf.empty:
        print(f"{BRIGHT_RED}No vehicles found. Add one first.")
        return
    print(f"\n{BRIGHT_CYAN}Your Vehicles")
    print(vdf.to_string(index=False))
    vno = input("Enter Vehicle No: ").strip()
    if not vno:
        return

    sdf = pd.read_sql(
        "SELECT service_id, service_name, base_price FROM services WHERE status='Active'",
        con=engcon,
    )
    if sdf.empty:
        print(f"{BRIGHT_RED}No services available.")
        return
    print(f"\n{BRIGHT_CYAN}Available Services")
    print(sdf.to_string(index=False))
    sid = input("Enter Service ID: ").strip()
    if not sid:
        return

    bdf = pd.DataFrame([{
        "vehicle_no": vno,
        "service_id": int(sid),
        "booking_date": pd.Timestamp.now(),
        "status": "Pending",
    }])
    try:
        bdf.to_sql("service_bookings", con=engcon, if_exists="append", index=False)
        print(f"{BRIGHT_GREEN}✅ Booking created (Pending).")
    except Exception as e:
        print(f"{BRIGHT_RED}❌ Failed to create booking: {e}")


# === 6) Make Payment ===
def make_payment(currentuseridid: int):
    idf = pd.read_sql(
        "SELECT invoice_id, booking_id, amount, payment_status FROM invoices WHERE user_id=%s AND payment_status='Pending'",
        con=engcon, params=(currentuseridid,)
    )
    if idf.empty:
        print(f"{BRIGHT_RED}No pending invoices.")
        return
    print(f"\n{BRIGHT_CYAN}Pending Invoices")
    print(idf.to_string(index=False))
    inv_id = input("Enter Invoice ID to pay: ").strip()
    if not inv_id:
        return

    method = input("Payment method (Cash/Card/UPI/Bank Transfer): ").strip() or "Cash"
    cursor.execute(
        "UPDATE invoices SET payment_status='Paid', payment_method=%s, invoice_date=NOW() WHERE invoice_id=%s AND user_id=%s",
        (method, inv_id, currentuseridid),
    )
    mycon.commit()
    print(f"{BRIGHT_GREEN}✅ Payment recorded.")


# === 7) View Booking History ===
def view_booking_history(currentuseridid: int):
    q = """
    SELECT b.booking_id, b.booking_date, b.status,
           v.vehicle_no, v.vehicle_brand, v.model,
           s.service_name
      FROM service_bookings b
      JOIN vehicles v ON b.vehicle_no = v.vehicle_no
      JOIN services s ON b.service_id = s.service_id
      JOIN users u ON v.user_id = u.user_id
     WHERE u.user_id = %s
     ORDER BY b.booking_date DESC
    """
    h = pd.read_sql(q, con=engcon, params=(currentuseridid,))
    if h.empty:
        print(f"{BRIGHT_RED}No bookings yet.")
        return
    print(f"\n{BRIGHT_CYAN}Your Booking History")
    print(h.to_string(index=False))


# === 8) Track Order ===
def track_order(currentuseridid: int):
    q = """
    SELECT b.booking_id, b.status, b.booking_date,
           s.service_name,
           COALESCE(m.full_name, '-') AS mechanic,
           ma.assigned_date
      FROM service_bookings b
      JOIN services s ON b.service_id = s.service_id
      JOIN vehicles v ON b.vehicle_no = v.vehicle_no
      LEFT JOIN mechanic_assignments ma ON ma.booking_id = b.booking_id
      LEFT JOIN mechanics_info m ON ma.mechanic_id = m.mechanic_id
      JOIN users u ON v.user_id = u.user_id
     WHERE u.user_id = %s
     ORDER BY b.booking_date DESC
    """
    df = pd.read_sql(q, con=engcon, params=(currentuseridid,))
    if df.empty:
        print(f"{BRIGHT_RED}No orders to track.")
        return
    print(f"\n{BRIGHT_CYAN}Order Tracking")
    print(df.to_string(index=False))


# === 9) Cancel Order ===
def cancel_order(currentuseridid: int):
    q = """
    SELECT b.booking_id, b.status, s.service_name, b.booking_date
      FROM service_bookings b
      JOIN services s ON b.service_id = s.service_id
      JOIN vehicles v ON b.vehicle_no = v.vehicle_no
     WHERE v.user_id = %s AND b.status IN ('Pending','In Progress')
     ORDER BY b.booking_date DESC
    """
    cdf = pd.read_sql(q, con=engcon, params=(currentuseridid,))
    if cdf.empty:
        print(f"{BRIGHT_RED}No cancellable bookings.")
        return
    print(f"\n{BRIGHT_CYAN}Cancellable Bookings")
    print(cdf.to_string(index=False))
    bid = input("Enter Booking ID to cancel: ").strip()
    if not bid:
        return

    ans = input(f"Cancel booking {bid}? (y/n): ").strip().lower()
    if ans in ("y", "yes"):
        cursor.execute(
            "UPDATE service_bookings SET status='Cancelled' WHERE booking_id=%s",
            (bid,),
        )
        mycon.commit()
        print(f"{BRIGHT_GREEN}✅ Booking cancelled.")


# === 10) View / Download Invoice ===
def view_or_download_invoice(currentuseridid: int):
    q = """
    SELECT invoice_id, booking_id, amount, payment_status, payment_method, invoice_date
      FROM invoices
     WHERE user_id=%s
     ORDER BY invoice_date DESC
    """
    df = pd.read_sql(q, con=engcon, params=(currentuseridid,))
    if df.empty:
        print(f"{BRIGHT_RED}No invoices yet.")
        return
    print(f"\n{BRIGHT_CYAN}Your Invoices")
    print(df.to_string(index=False))


# === 11) Check Payment Status ===
def check_payment_status(currentuseridid: int):
    q = "SELECT invoice_id, amount, payment_status FROM invoices WHERE user_id=%s ORDER BY invoice_id DESC"
    df = pd.read_sql(q, con=engcon, params=(currentuseridid,))
    if df.empty:
        print(f"{BRIGHT_RED}No invoices found.")
        return
    print(f"\n{BRIGHT_CYAN}Payment Status")
    print(df.to_string(index=False))


# === 12) Feedback ===
def leave_feedback(currentuseridid: int):
    q = """
    SELECT b.booking_id, s.service_name, b.booking_date
      FROM service_bookings b
      JOIN services s ON b.service_id = s.service_id
      JOIN vehicles v ON b.vehicle_no = v.vehicle_no
      LEFT JOIN feedback f ON f.booking_id = b.booking_id
     WHERE v.user_id = %s AND b.status='Completed' AND f.booking_id IS NULL
     ORDER BY b.booking_date DESC
    """
    df = pd.read_sql(q, con=engcon, params=(currentuseridid,))
    if df.empty:
        print(f"{BRIGHT_RED}No completed bookings available for feedback.")
        return
    