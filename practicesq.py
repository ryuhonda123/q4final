import sqlite3
import os
from datetime import datetime
import re
# https://chatgpt.com/s/t_6a1d8598ce4081919eca68f52a724931 function to clear the screen
# CONNECT TO DATABASE
db = sqlite3.connect('hotel.db') # REQUIRED

db.execute("PRAGMA foreign_keys = ON")

# CREATE CURSOR OBJECT
# This is the middleware between connection and queries
cursor = db.cursor() # REQUIRED

# https://chatgpt.com/s/t_6a1d8598ce4081919eca68f52a724931 function to clear the screen
def clear_screen():

    if os.name == "nt":
        os.system("cls")

    else:
        os.system("clear")


# TABLES ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Staff table
cursor.execute('''CREATE TABLE IF NOT EXISTS staff (
    StaffID INTEGER PRIMARY KEY AUTOINCREMENT,
    Staff_first_name CHAR(50),
    Staff_last_name CHAR(50),
    Job_occupation CHAR(30),
    Staff_join_date DATE,
    Experience TEXT,
    Salary DECIMAL,
    Shifts CHAR(50)
)''')

# Cleaning schedule table
cursor.execute('''CREATE TABLE IF NOT EXISTS cleaning_schedule (
    StaffID INTEGER,
    Staff_responsibility_room CHAR(50),
    Times TIME,
    Shifts CHAR(20),
    ScheduleID INTEGER PRIMARY KEY AUTOINCREMENT,

    FOREIGN KEY (StaffID) REFERENCES staff(StaffID)
)''')


# Guest table
cursor.execute('''CREATE TABLE IF NOT EXISTS guest (
    GuestID INTEGER PRIMARY KEY AUTOINCREMENT,
    Guest_first_name CHAR(50),
    Guest_last_name CHAR(50),
    Date_of_birth DATE,
    Join_date DATE,
    Payment_method CHAR(20),
    Membership_type CHAR(25),
    Email CHAR(80),
    Room_number INTEGER,
    Room_tier CHAR(20),
    Room_prices DECIMAL,

    FOREIGN KEY (Room_number) REFERENCES rooms(Room_number)
)''')

# Rooms table https://chatgpt.com/s/t_6a1dc2d56d2c8191b3b32a2de4209c1d asked AI how to customize the boolean values to be Availible and Occupied ONLY
cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
    Room_number INTEGER PRIMARY KEY,
    Room_tier CHAR(10),
    Room_floor INT(1),
    
    Room_availibility TEXT
    CHECK(
        Room_availibility IN
        ('Available','Occupied')
    ),
    Room_prices DECIMAL,
    GuestID INTEGER,
    Staff_responsibility_room CHAR(50),

    FOREIGN KEY (GuestID) REFERENCES guest(GuestID)

)''')

#https://chatgpt.com/s/t_6a1db1dfb314819190220ebbf1870601 for initially storing values and having the insert or ignore function (if value is already there then ignore it), also 
#taught me how to use the values for future purposes
# Standard 101-110
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (101,'Standard',1,'Available',99.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (102,'Standard',1,'Available',99.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (103,'Standard',1,'Available',99.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (104,'Standard',1,'Available',99.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (105,'Standard',1,'Available',99.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (106,'Standard',1,'Available',99.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (107,'Standard',1,'Available',99.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (108,'Standard',1,'Available',99.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (109,'Standard',1,'Available',99.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (110,'Standard',1,'Available',99.99,NULL,NULL)")

# Superior 201-210
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (201,'Superior',2,'Available',249.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (202,'Superior',2,'Available',249.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (203,'Superior',2,'Available',249.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (204,'Superior',2,'Available',249.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (205,'Superior',2,'Available',249.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (206,'Superior',2,'Available',249.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (207,'Superior',2,'Available',249.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (208,'Superior',2,'Available',249.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (209,'Superior',2,'Available',249.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (210,'Superior',2,'Available',249.99,NULL,NULL)")

# Deluxe 301-308
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (301,'Deluxe',3,'Available',599.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (302,'Deluxe',3,'Available',599.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (303,'Deluxe',3,'Available',599.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (304,'Deluxe',3,'Available',599.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (305,'Deluxe',3,'Available',599.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (306,'Deluxe',3,'Available',599.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (307,'Deluxe',3,'Available',599.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (308,'Deluxe',3,'Available',599.99,NULL,NULL)")

# Executive 401-405
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (401,'Executive',4,'Available',999.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (402,'Executive',4,'Available',999.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (403,'Executive',4,'Available',999.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (404,'Executive',4,'Available',999.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (405,'Executive',4,'Available',999.99,NULL,NULL)")

# Suites 501-503
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (501,'Suite',5,'Available',2499.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (502,'Suite',5,'Available',2499.99,NULL,NULL)")
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (503,'Suite',5,'Available',2499.99,NULL,NULL)")

# Luxury 601
cursor.execute("INSERT OR IGNORE INTO rooms VALUES (601,'Luxury',6,'Available',9999.99,NULL,NULL)")

db.commit()



# Reservations table
cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
    GuestID INTEGER,    
    Payment_status BOOLEAN,
    People_amount INTEGER,
    Room_number INTEGER,
    ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
    Join_date DATE,

    FOREIGN KEY (GuestID) REFERENCES guest(GuestID),
    FOREIGN KEY (Room_number) REFERENCES rooms(Room_number)
)''')



# CLASSES
# Asked AI how to manage and organize information better with classes https://chatgpt.com/s/t_6a1d4432998c8191ad17460602680606
class Manager:

# Asked AI how to make a function for the user to input their information and then gets saved in the table https://chatgpt.com/s/t_6a1d28e7f37c8191a4659fa606fab51e
    def check_in():

# https://chatgpt.com/s/t_6a1df3912f9881919fdff1e040e63f53 for the methods in order to filter each input to ensure the correct format. In this case, text only, date only, email only.
        while True:
            first_name = input("What is your first name: ").strip()
            if first_name.isalpha():
                break
            else:
                print("First name must contain letters only.")

        while True:
            last_name = input("What is your last name: ").strip()
            if last_name.isalpha():
                break
            else:
                print("Last name must contain letters only.")

        while True:
            dob = input("What is your date of birth? (YYYY-MM-DD): ")
            try:
                datetime.strptime(dob, "%Y-%m-%d")
                break
            except:
                print("Invalid date format. Use YYYY-MM-DD.")

        while True:
            join_date = input("What date are you staying? (YYYY-MM-DD): ")
            try:
                datetime.strptime(join_date, "%Y-%m-%d")
                break
            except:
                print("Invalid date format. Use YYYY-MM-DD.")

        while True:
            membership = input("Membership type? (Regular/Vip): ").capitalize()
            if membership in ["Regular", "Vip"]:
                break
            else:
                print("Please enter Regular or Vip only.")

        while True:
            email = input("What is your email?: ").strip()

            pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

            if re.match(pattern, email):
                break
            else:
                print("Invalid email format.")

        while True:
            room_tier = input("What room tier would you like to stay in? (Standard, Superior, Deluxe, Executive, Suite, Luxury): ").capitalize()
            if room_tier in ["Standard", "Superior", "Deluxe", "Executive", "Suite", "Luxury"]:
                break
            else:
                print("Invalid room tier.")

        # Asked AI how to create a filter that searches for specific information in the table before moving on, in this case it is searching if room availibility is availible before allowing the user to actually stay
        # https://chatgpt.com/s/t_6a1dcaaa7608819191f674ab60970a08 understood limits better, so that it only takes one row then stops
        # Asked AI on how to get specific columns from the selected row, in this case instead of selecting * (which is all), it selected only room prices, availibility, and room number https://chatgpt.com/s/t_6a1dce384c3881919000f15c22e8a97c

        cursor.execute("""
        SELECT Room_tier, Room_prices, Room_number
        FROM rooms
        WHERE Room_tier = ?
        AND Room_availibility = 'Available'
        LIMIT 1
        """, (room_tier,))

        # room_data contains information of room tier and room price so then it just has to be accessed by using [0] and [1]
        room_data = cursor.fetchone()

        if room_data is None:

            clear_screen()

            print("""
        ╔══════════════════════════════════════════════╗
        ║                                              ║
        ║        Sorry, no rooms available.            ║
        ║                                              ║
        ║     Please try another room tier.            ║
        ║                                              ║
        ╚══════════════════════════════════════════════╝
        """)

            input("Press Enter to continue...")
            return

        room_tier = room_data[0]
        room_price = room_data[1]
        room_number = room_data[2]

        if membership == "Vip":
            discount = room_price * 0.20
            room_price = room_price - discount
            vip_message = "VIP Discount Applied! 20% Off"

        else:
            vip_message = ""

        room_message = f"{room_tier} Room Available! ${room_price:.2f}"

# Credits to https://chatgpt.com/s/t_6a1de292b8248191b3a7bf95c7a2d089 for spacing, makes the spaces after the text constant.  stats box will stay intact regardless of the length of the name.
        clear_screen()
        print(f"""
╔══════════════════════════════════════════════╗
║                                              ║
║{room_message:^46}║
║{vip_message:^46}║               
║   ────────────────────────────────────────   ║
║                                              ║
║   [1]  Cash                                  ║
║                                              ║
║   [2]  Card                                  ║
║                                              ║
╚══════════════════════════════════════════════╝""") 
        payment_choice = input("Would you like to pay with cash or card? (1/2): ").lower()
        while True:
            # Asked AI how to insert the user's input information direclty into the table https://chatgpt.com/s/t_6a1dd6dc5eec819191f394bb59e4ed6c
            if payment_choice == "1":
                payment_method = "Cash"
                break

            elif payment_choice == "2":
                payment_method = "Card"
                break

            else:
                payment_choice = input("Invalid choice, enter 1 or 2: ")
# To insert the inputted values into the guest table
        cursor.execute("""
        INSERT INTO guest(
            Guest_first_name,
            Guest_last_name,
            Date_of_birth,
            Join_date,
            Payment_method,
            Membership_type,
            Email,
            Room_number,
            Room_tier,
            Room_prices
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            first_name,
            last_name,
            dob,
            join_date,
            payment_method,
            membership,
            email,
            room_number,
            room_tier,
            room_price
        ))

# Asked AI how to get the guestID to input it to the rooms table https://chatgpt.com/s/t_6a1e054862008191a3f9d63e8fd65c2c
        guest_id = cursor.lastrowid


        room_number_message = f"Your room number is {room_number}"
        clear_screen()
        print(f"""
╔══════════════════════════════════════════════╗
║                                              ║
║{"Thank you for staying!":^46}║
║{room_number_message:^46}║
║   ────────────────────────────────────────   ║
╚══════════════════════════════════════════════╝""")
        
        input()

        # Asked AI how to update another table manually without the input functions, a few lines above this line is the function to pick specific columns and filter through it https://chatgpt.com/s/t_6a1de75b856c8191b24378c81820e181
        # In this case, it is updating the table rooms for its availibility to be occupied
        # Additionally, the GuestID value is also taken and put in the rooms table
        cursor.execute("""
        UPDATE rooms
        SET Room_availibility = 'Occupied',
            GuestID = ?
        WHERE Room_number = ?
        """, (guest_id, room_number))

        db.commit()

    

    def check_out():

        clear_screen()

        while True:
            first_name = input("Please enter your first name: ").strip()

            if first_name.isalpha():
                break
            else:
                print("First name must contain letters only.")

        while True:
            room_number = input("Please enter your room number: ")

            if room_number.isdigit():
                break
            else:
                print("Room number must be numbers only.")
#A filter to match the inputs to see if it is valid, in this case it is checking to see if the first name matches with it's room number
        cursor.execute("""
        SELECT *
        FROM guest
        WHERE Guest_first_name = ?
        AND Room_number = ?
        """, (first_name, room_number))

        guest_exists = cursor.fetchone()

        if guest_exists is None:

            clear_screen()

            print("""
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║         Guest details not found.             ║
    ║                                              ║
    ║     Please check your information.           ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    """)

            input("Press Enter to continue...")
            return

        clear_screen()

        print(f"""
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║      Are you sure you want to check out?     ║
    ║                                              ║
    ║               [Y] Yes                        ║
    ║               [N] No                         ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    """)

        confirm_checkout = input("Confirm checkout? (Y/N): ").lower()

        while True:
            if confirm_checkout == "y":
                break

            elif confirm_checkout == "n":
                return

            else:
                confirm_checkout = input("Invalid input, please enter Y or N: ").lower()

# This is to update the rooms availibility to make it availible again for future guests to come and check in
        cursor.execute("""
        UPDATE rooms
        SET Room_availibility = 'Available',
            GuestID = NULL
        WHERE Room_number = ?
        """, (room_number,))
# This is to delete the guest records so that it doesnt overfill with the same room numbers and get confusing
        cursor.execute("""
        DELETE FROM guest
        WHERE Room_number = ?
        """, (room_number,))

        db.commit()

        clear_screen()

        print(f"""
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║{"Checkout successful!":^46}║
    ║{"Thank you for staying with us.":^46}║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    """)

        input()

        



    def read_reservation_data():

        clear_screen()

        cursor.execute("""
        SELECT *
        FROM reservations
        """)
# The list of ALL the columns in the reservations table
        reservations = cursor.fetchall()

        if not reservations:
            print("No reservations found.")
            input()
            return

        for reservation in reservations:

            print(f"""
    ╔══════════════════════════════════════════════╗
    ║{"Reservation Record":^46}║
    ║──────────────────────────────────────────────║
    ║ Reservation ID : {reservation[4]}
    ║ Guest ID       : {reservation[0]}
    ║ Payment Status : {reservation[1]}
    ║ People Amount  : {reservation[2]}
    ║ Room Number    : {reservation[3]}
    ║ Join Date      : {reservation[5]}
    ╚══════════════════════════════════════════════╝
    """)

        input()


    def read_guest_data():

        clear_screen()
# Takes ALL the columns data from guest table
        cursor.execute("""
        SELECT *
        FROM guest
        """)

        guests = cursor.fetchall()

        if not guests:
            print("No guest records found.")
            input()
            return

        for guest in guests:

            print(f"""
    ╔══════════════════════════════════════════════╗
    ║{"Guest Record":^46}║
    ║──────────────────────────────────────────────║
    ║ Guest ID        : {guest[0]}
    ║ First Name      : {guest[1]}
    ║ Last Name       : {guest[2]}
    ║ Date of Birth   : {guest[3]}
    ║ Join Date       : {guest[4]}
    ║ Payment Method  : {guest[5]}
    ║ Membership Type : {guest[6]}
    ║ Email           : {guest[7]}
    ║ Room Number     : {guest[8]}
    ║ Room Tier       : {guest[9]}
    ║ Room Price      : ${guest[10]}
    ╚══════════════════════════════════════════════╝
    """)

        input()

    def billing_payments():
        # Credits to https://chatgpt.com/s/t_6a1e12569fd4819186eac5bdfb9106b4 for performing math operations on integer values from tables
        clear_screen()

        # Total room price revenue
        # Takes the sum of all the room prices from the guest table
        cursor.execute("""
        SELECT SUM(Room_prices)
        FROM guest
        """)
        # To take the final revenue result
        revenue_result = cursor.fetchone()
        revenue = revenue_result[0]

        if revenue is None:
            revenue = 0

        # Total staff salary
        # Takes the sum of all the salary from staff table
        cursor.execute("""
        SELECT SUM(Salary)
        FROM staff
        """)
        #Takeing final salary costs
        salary_result = cursor.fetchone()
        salary_cost = salary_result[0]

        if salary_cost is None:
            salary_cost = 0

        # Python calculations
        profit = revenue - salary_cost

        print(f"""
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║{"Billing and Payments Summary":^46}║
    ║──────────────────────────────────────────────║
    ║ Total Revenue : ${revenue:.2f}
    ║ Salary Costs  : ${salary_cost:.2f}
    ║ Net Profit    : ${profit:.2f}
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    """)

        input()


    def add_staff():

        clear_screen()

        while True:
            staff_first_name = input("Staff first name: ").strip().capitalize()

            if staff_first_name.isalpha():
                break
            else:
                print("First name must contain letters only.")

        while True:
            staff_last_name = input("Staff last name: ").strip().capitalize()

            if staff_last_name.isalpha():
                break
            else:
                print("Last name must contain letters only.")

        while True:
            job = input("Job occupation (Reception/Housekeeping/Maintenance/Manager): ").capitalize()

            if job in ["Reception", "Housekeeping", "Maintenance", "Manager"]:
                break
            else:
                print("Invalid job occupation.")

        while True:
            staff_join_date = input("Join date (YYYY-MM-DD): ")

            try:
                datetime.strptime(staff_join_date, "%Y-%m-%d")
                break

            except:
                print("Invalid date format.")

        while True:
            experience = input("Years of experience: ")

            if experience.isdigit():
                break
            else:
                print("Experience must be a number.")

        #Asked AI for string method for float https://chatgpt.com/s/t_6a1e0a8e76a881919973d69aa5a5edda
        while True:
            salary = input("Salary: ")

            try:
                salary = float(salary)

                if salary > 0:
                    break
                else:
                    print("Salary must be greater than 0.")

            except ValueError:
                print("Salary must be a number.")

        while True:
            shifts = input("Shift (Morning/Afternoon/Night): ").capitalize()

            if shifts in ["Morning", "Afternoon", "Night"]:
                break
            else:
                print("Invalid shift.")
# Saves the inputted data and stores it in the staff table
        cursor.execute("""
        INSERT INTO staff(
            Staff_first_name,
            Staff_last_name,
            Job_occupation,
            Staff_join_date,
            Experience,
            Salary,
            Shifts
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            staff_first_name,
            staff_last_name,
            job,
            staff_join_date,
            experience,
            salary,
            shifts
        ))

        db.commit()

        clear_screen()

        staff_message = f"{staff_first_name} {staff_last_name} added successfully"

        print(f"""
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║{"Staff Added Successfully!":^46}║
    ║{staff_message:^46}║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    """)

        input()

    def cleaning_schedule():

        clear_screen()

# Takes these specific columns from the staff table
        cursor.execute("""
        SELECT StaffID,
            Staff_first_name,
            Staff_last_name,
            Job_occupation,
            Shifts
        FROM staff
        """)
# Prints all the staff but ONLY from those specific columns
        staff_members = cursor.fetchall()

        print("Available Staff")
        print()

        for staff in staff_members:
            print(staff)

        print()
        print("1st column = Staff ID")
        print("2nd = First Name")
        print("3rd = Last Name")
        print("4th = Job")
        print("5th = Shift")

        while True:
            staff_id = input("Select Staff ID: ")

            if staff_id.isdigit():
                break
            else:
                print("Invalid Staff ID.")
# A filter to really check if the staffID is valid and exists
        cursor.execute("""
        SELECT *
        FROM staff
        WHERE StaffID = ?
        """, (staff_id,))

        staff_exists = cursor.fetchone()

        if staff_exists is None:

            clear_screen()

            print("""
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║          Staff member not found.             ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    """)

            input()
            return

        while True:
            room_number = input("What room will you be responsible for?: ")

            if room_number.isdigit():
                break
            else:
                print("Room number must be numeric.")

# The same as before, it verifies if the room number actually exists before moving on
        cursor.execute("""
        SELECT *
        FROM rooms
        WHERE Room_number = ?
        """, (room_number,))

        room_exists = cursor.fetchone()

        if room_exists is None:

            print("Room does not exist.")
            input()
            return
# Asked AI to make input functions for times, e.g 8:00-12:30 https://chatgpt.com/s/t_6a1e0ccd4c80819186f8d6829b503498, if the Hours are beyond 24 or the minutes are beyond 60, program will have error
        while True:
            times = input("Cleaning time (HH:MM): ")

            try:
                times = datetime.strptime(times, "%H:%M")
                break

            except ValueError:
                print("Please enter a valid time.")

# Takes ONLY shift column from the staff table 
        cursor.execute("""
        SELECT Shifts
        FROM staff
        WHERE StaffID = ?
        """, (staff_id,))
# shift_data has the value but its formatted like ("Morning"), so shifts gets only the "Morning" by using [0]
        shift_data = cursor.fetchone()
        shifts = shift_data[0]
# Inserts the inputted information into the cleaning schedule
        cursor.execute("""
        INSERT INTO cleaning_schedule(
            StaffID,
            Staff_responsibility_room,
            Times,
            Shifts
        )
        VALUES (?, ?, ?, ?)
        """, (
            staff_id,
            room_number,
            times,
            shifts
        ))

        db.commit()

        clear_screen()

        schedule_message = f"Room {room_number} assigned"

        print(f"""
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║{"Cleaning Schedule Added!":^46}║
    ║{schedule_message:^46}║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    """)

        input()

    

# Asked AI how to make a updating function to update information in tables https://chatgpt.com/s/t_6a1d79a7e3208191adc7c0186b9fa9b8
# Asked AI how to make a read function beforehand so that the user can pick from the potential options and update their information https://chatgpt.com/s/t_6a1d7b6415e08191adeb9e40f345bd20
    def update_guest():

        while True:

            cursor.execute("""
            SELECT GuestID,
                Guest_first_name,
                Guest_last_name,
                Date_of_birth
            FROM guest
            """)
# To get the information from the guest table BUT only for columns first name, last name, and the date of birth
            guests = cursor.fetchall()
            clear_screen()
            for guest in guests:
                print(guest)
            
            print("1st column is GuestID")
            print("2nd column is First name")
            print("3rd column is Last name")
            print("4th column is Date of birth")


            guest_id = int(input("Please pick your Guest ID to edit: "))

            cursor.execute("""
            SELECT *
            FROM guest
            WHERE GuestID = ?
            """, (guest_id,))

            guest_exists = cursor.fetchone()

            if guest_exists is None:
                print("Guest ID not found.")
                continue
        
            clear_screen()
            print("1. First Name")
            print("2. Last Name")
            print("3. Email")
            print("4. Date of Birth")
            print("5. Join date")
            print("6. Payment_method")
            print("0. Cancel")

            update_choice = input("What do you want to update? ")

            if update_choice == "1":

                new_value = input("New first name: ")

                cursor.execute("""
                UPDATE guest
                SET Guest_first_name = ?
                WHERE GuestID = ?
                """, (new_value, guest_id))

            elif update_choice == "2":

                new_value = input("New last name: ")

                cursor.execute("""
                UPDATE guest
                SET Guest_last_name = ?
                WHERE GuestID = ?
                """, (new_value, guest_id))

            elif update_choice == "3":

                new_value = input("New email: ")

                cursor.execute("""
                UPDATE guest
                SET Email = ?
                WHERE GuestID = ?
                """, (new_value, guest_id))

            elif update_choice == "4":

                new_value = input("New Date of Birth: ")

                cursor.execute("""
                UPDATE guest
                SET Date_of_birth = ?
                WHERE GuestID = ?
                """, (new_value, guest_id))

            elif update_choice == "5":

                new_value = input("New Join date: ")

                cursor.execute("""
                UPDATE guest
                SET Join_date = ?
                WHERE GuestID = ?
                """, (new_value, guest_id))

            elif update_choice == "6":

                new_value = input("New payment method: ")

                cursor.execute("""
                UPDATE guest
                SET Payment_method = ?
                WHERE GuestID = ?
                """, (new_value, guest_id))

            elif update_choice == "0":
                return

            else:
                print("Invalid choice.")
                continue   
                    
            db.commit()

            again = input("Do you want to update anything else for guests? (Y/N): ").lower()

            while True:

                if again == "y":
                    break

                elif again == "n":
                    return
                    
                else:
                    again = input("Invalid input, try again: ").lower()

class Guest:

    def __init__(self, guest_first_name, guest_last_name, dob, join_date, payment_method, membership_type, email, room_number):

        self.first_name = guest_first_name
        self.last_name = guest_last_name
        self.dob = dob
        self.join_date = join_date
        self.payment_method = payment_method
        self.membership_type = membership_type
        self.email = email
        self.room_number = room_number
        

     

while True:
    clear_screen()
    print("""
╔══════════════════════════════════════════════╗
║                                              ║
║                GUEST OR STAFF?               ║
║   ────────────────────────────────────────   ║
║                                              ║
║   [1]  Guest  (New or old guest)             ║
║                                              ║
║   [2]  Staff  (Manage system)                ║
║                                              ║
╚══════════════════════════════════════════════╝""")   

    staff_guest_choice = input("Welcome, are you a new/old guest or staff?: ")   

    if staff_guest_choice == "1":
        clear_screen()
        # https://chatgpt.com/s/t_6a1d3a41956c81919f44a0e2594c4558 for the menu design for guest and staff menu
        print("""
╔══════════════════════════════════════════════╗
║   ██████╗ ██╗   ██╗███████╗███████╗████████╗ ║
║  ██╔════╝ ██║   ██║██╔════╝██╔════╝╚══██╔══╝ ║
║  ██║  ███╗██║   ██║█████╗  ███████╗   ██║    ║
║  ██║   ██║██║   ██║██╔══╝  ╚════██║   ██║    ║
║  ╚██████╔╝╚██████╔╝███████╗███████║   ██║    ║
║   ╚═════╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝    ║
║                                              ║
║               G U E S T  M E N U             ║
╠══════════════════════════════════════════════╣
║                                              ║
║   [1] Check in/Check out                     ║
║                                              ║
║   [2] Back                                   ║
║                                              ║
╚══════════════════════════════════════════════╝""")

        guest_choice = input("Hello, what would you like to do today?: ")
        while True:
            if guest_choice == "1":
                    while True:
                        clear_screen()
                        print("""
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║   CHECK IN / CHECK OUT                       ║
    ║   ────────────────────────────────────────   ║
    ║                                              ║
    ║   [1]  Check In  (New guest arriving)        ║
    ║                                              ║
    ║   [2]  Check Out (Guest departing)           ║
    ║                                              ║
    ║   [0]  Back to Main Menu                     ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝""")
                        checkinchoice = input("What would you like to do?: ")

                        if checkinchoice == "1":
                                Manager.check_in()
                                
                        elif checkinchoice == "2":
                                Manager.check_out()

                        elif checkinchoice == "0":
                                break
                        else:
                            print("Invalid choice, try again")
                            continue
                    break

            elif guest_choice == "2":
                    break
                    
            else:
                print("Invalid choice, try again")
                guest_choice = input("Hello, what would you like to do today?: ")
                         
    
    elif staff_guest_choice == "2":
        clear_screen()
        print("""
╔══════════════════════════════════════════════╗
║  ███████╗████████╗ █████╗ ███████╗███████╗   ║
║  ██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝   ║
║  ███████╗   ██║   ███████║█████╗  █████╗     ║
║  ╚════██║   ██║   ██╔══██║██╔══╝  ██╔══╝     ║
║  ███████║   ██║   ██║  ██║██║     ██║        ║
║  ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝        ║
║                                              ║
║               S T A F F  P A N E L           ║
╠══════════════════════════════════════════════╣
║                                              ║
║   [1] Update Guests                          ║
║                                              ║
║   [2] Reservations Management                ║
║                                              ║
║   [3] Guest Records                          ║
║                                              ║
║   [4] Billing / Payments                     ║
║                                              ║
║   [5] Staff Management                       ║
║                                              ║
║   [0] Back to Main Menu                      ║
║                                              ║
╚══════════════════════════════════════════════╝""")
                
        staff_choice = input("Hello, what would you like to do today?: ")
        while True:
            if staff_choice == "1":
                Manager.update_guest()

            elif staff_choice == "2":
                Manager.read_reservation_data()

            elif staff_choice == "3":
                Manager.read_guest_data()

            elif staff_choice == "4":
                Manager.billing_payments()

            elif staff_choice == "5":
                    while True:
                        clear_screen()
                        print("""
╔══════════════════════════════════════════════╗
║                                              ║
║   STAFF MANAGEMENT                           ║
║   ────────────────────────────────────────   ║
║                                              ║
║   [1]  Add Staff                             ║
║                                              ║
║   [2]  Update Schedule                       ║
║                                              ║
║   [0]  Back to Main Menu                     ║
║                                              ║
╚══════════════════════════════════════════════╝""")
                        staff_management_choice = input("What would you like to do?: ")

                        if staff_management_choice == "1":
                                Manager.add_staff()
                                        
                        elif staff_management_choice == "2":
                                Manager.cleaning_schedule()
                        
                        elif staff_management_choice == "0":
                            break
                        else:
                            print("Invalid choice, try again")
                            continue

            elif staff_choice == "0":
                break

            else:
                print("Invalid choice, try again")

            staff_choice = input("Hello, what would you like to do today? (1,2,3,4,5): ")
