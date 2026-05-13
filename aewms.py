from datetime import datetime  # to get current date and time

# to create empty list to store data
awems = []

# txt file name
File_Name = "awems_data.txt"
MAX_CAPACITY = 1000  # in kg
today = datetime.now()

# to load data from txt file when program starts
def load_data():
    try:
        with open(File_Name, "r") as file:
            # awems.clear()
            for line in file:
                data = line.strip().split("|")
                if len(data) == 7:  # Ensure the line has all fields
                    # Create a dictionary to match your Technical Design Document
                    item = {
                        "item_id": data[0],
                        "device_name": data[1],
                        "category": data[2],
                        "weight": float(data[3]),
                        "fee_per_kg": float(data[4]),
                        "storage_status": data[5],
                        "date_added": data[6]
                    }
                    awems.append(item)
    except FileNotFoundError:
        pass


#to load data from txt file when program starts
load_data()


#to check storage capacity and alert if it is exceeded
def storage_check():
    storage_capacity = 1000  # in kg
    total_storage = 0
    for item in awems:
        total_storage = total_storage + float(item["weight"])
    if (total_storage*0.8) > storage_capacity:
        print(
            f"ALERT:! Total storage used: {total_storage} kg, which exceeds the limit of  80% of the storage capacity.\n")
    print(f"Total storage capacity used: {total_storage} kg")
    print(
        f"Available storage capacity: {storage_capacity - total_storage} kg\n")


#to save data to txt file when program is closed
def save_data():
    with open(File_Name, "w") as file:
        for item in awems:
            line = (f"{item['item_id']}|"
                    f"{item['device_name']}|"
                    f"{item['category']}|"
                    f"{item['weight']}|"
                    f"{item['fee_per_kg']}|"
                    f"{item['storage_status']}|"
                    f"{item['date_added']}\n")
            file.write(line)


# to show main menu
def main_menu():
    print("====== Welcome to E-Waste Management System ======"),
    print("1. View all items"),
    print("2. Add new item"),
    print("3. Update item"),
    print("4. Delete item"),
    print("5. Search item"),
    print("6. Calculate fee"),
    print("7. Generate report"),
    print("8. Hazardous items alert"),
    print("9. Exit")

# to automatically generate next item ID
def generate_id():
    if len(awems) == 0:
        return "EW001"
    else:
        last_id = awems[-1]["item_id"][2:]
        new_id = int(last_id) + 1
        new_id = f"EW{new_id:03d}"
        return new_id


# to display all items
def display_items():
    if len(awems) == 0:
        print("No items available.\n")
        return
    print("\n--- Current Inventory ---")
    for item in awems:
        print(f"Item ID: {item['item_id']} |",
              f"Name: {item['device_name']} |",
              f"Category: {item['category']} |",
              f"Storage Status: {item['storage_status']} |",
              f"Weight: {item['weight']} |",
              f"Fee per kg: {item['fee_per_kg']} |",
              f"Date Added: {item['date_added']}\n")


# to add items
def add_item():
    new_id = generate_id()
    print(f"Item ID: {new_id}")
    item_id = new_id
    item_name = input(("Enter item name: "))
    item_category = input(
        "Enter item category (Recyclable / Hazardous / Non-Recyclable) : ")
    item_storage_status = input("Enter item storage status: ")
    current_total = sum(float(item['weight']) for item in awems)
    item_weight = float(input(
        f"Enter item weight in kg (Current total: {current_total} kg / Maximum capacity: {MAX_CAPACITY} kg): "))
    if current_total + item_weight > MAX_CAPACITY:
        print(
            f"Cannot add item. Adding this item would exceed the maximum storage capacity of {MAX_CAPACITY} kg.\n")
        return
    item_fee_per_kg = float(input("Enter item fee per kg: "))
    date_added = datetime.now().strftime("%d/%m/%Y -- %H:%M:%S")
    item = {
        "item_id": new_id,
        "device_name": item_name,
        "category": item_category,
        "storage_status": item_storage_status,
        "weight": item_weight,
        "fee_per_kg": item_fee_per_kg,
        "date_added": date_added
    }
    awems.append(item)
    save_data()
    print("\nItem added successfully.------------\n")

def delete_item():
    item_id = input("Enter item ID to delete: ")
    for item in awems:
        if item["item_id"] == item_id:
            awems.remove(item)
            save_data()
            print("\nItem deleted successfully.------------\n")
            return
    print("\nItem not found.------------\n")


def update_item():
    item_id = input("Enter item ID to update: ")
    for item in awems:
        if item["item_id"] == item_id:
            print(f"Current Name: {item['device_name']}")
            new_name = input("Enter new name (leave blank to keep current): ")
            if new_name:
                item["device_name"] = new_name

            print(f"Current Category: {item['category']}")
            new_category = input(
                "Enter new category (leave blank to keep current): ")
            if new_category:
                item["category"] = new_category

            print(f"Current Storage Status: {item['storage_status']}")
            new_storage_status = input(
                "Enter new storage status (leave blank to keep current): ")
            if new_storage_status:
                item["storage_status"] = new_storage_status

            print(f"Current Weight: {item['weight']} kg")
            new_weight_input = input(
                "Enter new weight in kg (leave blank to keep current): ")
            if new_weight_input:
                item["weight"] = float(new_weight_input)

            print(f"Current Fee per kg: {item['fee_per_kg']}")
            new_fee_input = input(
                "Enter new fee per kg (leave blank to keep current): ")
            if new_fee_input:
                item["fee_per_kg"] = float(new_fee_input)

            save_data()
            print("\nItem updated successfully.------------\n")
            return
    print("\nItem not found.------------\n")


def search_item():
    item = input("Enter item ID to search: ")
    for item in awems:
        if item["item_id"] == item_id:
            print(f"Item ID: {item['item_id']} |",
                  f"Name: {item['device_name']} |",
                  f"Category: {item['category']} |",
                  f"Storage Status: {item['storage_status']} |",
                  f"Weight: {item['weight']} |",
                  f"Fee per kg: {item['fee_per_kg']} |",
                  f"Date Added: {item['date_added']}\n")
            return
    print("\nItem not found.------------\n")


# to calculate fee for an item
def calculate_fee():
    item_id = input("Enter item ID to calculate fee: ")
    for item in awems:
        if item["item_id"] == item_id:
            weight = float(item["weight"])
            fee_per_kg = float(item["fee_per_kg"])
            fee = weight * fee_per_kg
            if weight > 50:
                fee *= 0.05  # Apply 5% surcharge for items over 50kg

            print("Total weight: ", weight, "kg")
            print("Fee per kg: ", fee_per_kg)
            if weight > 50:
                fee += fee * 0.95  # Add surcharge to total fee
                print("Surcharge applied: 5% for items over 50kg")
            print("Total payable fee Rs: ", fee, "\n")
            return
    print("\nItem not found.------------\n")


# to check hazardous items and alert if they are stored for over 30 days
def check_hazard_alert():
    today = datetime.now()
    for item in awems:
        if item["category"].lower() == "hazardous" and item["storage_status"].lower() == "stored":
            date_string = item["date_added"].split(" -- ")[0]
            date_added = datetime.strptime(date_string, "%d/%m/%Y")
            time_difference = (today - date_added).days
            if time_difference > 30:
                print("\n--- Hazardous Waste Disposal Alerts (Over 30 Days) ---")
                print(f"ALERT: Item {item['item_id']} ({item['device_name']}) Stored for {time_difference} days. Urgent disposal required!\n")

def generate_report():
    """Generate daily, monthly or yearly report."""
    print("\n--- Green Lantern Corps Recyclers ---")
    print("1. Daily Report")
    print("2. Monthly Report")
    print("3. Yearly Report")

    while True:
        try:
            report_type = int(input("Select report type: "))
            if report_type in [1, 2, 3]:
                break
            print("Enter 1, 2 or 3.")
        except ValueError:
            print("Enter a valid number.")

    filtered = []
    today = datetime.now()

    for item in awems:
        item_date = datetime.strptime(
            item["date_added"].split(" -- ")[0], "%d/%m/%Y")

        if report_type == 1:
            if (item_date.day == today.day and
                    item_date.month == today.month and
                    item_date.year == today.year):
                filtered.append(item)

        elif report_type == 2:
            if (item_date.month == today.month and
                    item_date.year == today.year):
                filtered.append(item)

        elif report_type == 3:
            if item_date.year == today.year:
                filtered.append(item)

    # totals
    total_items = len(filtered)
    total_weight = sum(item['weight'] for item in filtered)
    total_fee = sum(item['weight'] * item['fee_per_kg'] for item in filtered)

    # category counts
    recyclable = len([i for i in filtered if i["category"] == "Recyclable"])
    hazardous = len([i for i in filtered if i["category"] == "Hazardous"])
    non_recyclable = len([i for i in filtered if i["category"] == "Non-Recyclable"])

    # status counts
    stored = len([i for i in filtered if i["storage_status"] == "Stored"])
    recycled = len([i for i in filtered if i["storage_status"] == "Recycled"])
    disposed = len([i for i in filtered if i["storage_status"] == "Disposed"])

    # report label and period
    if report_type == 1:
        report_label = "Daily"
        period = today.strftime("%Y-%m-%d")
    elif report_type == 2:
        report_label = "Monthly"
        period = today.strftime("%B %Y")
    else:
        report_label = "Yearly"
        period = today.strftime("%Y")

    # build report
    report_content = f"""
                            ================================================
                            GREEN LANTERN CORPS AEWMS
                            {report_label} Report - {period}
                            Generated: {today.strftime("%Y-%m-%d %H:%M:%S")}
                            ================================================

                            SUMMARY
                            -------
                            Total Items Collected : {total_items}
                            Total Weight          : {total_weight:.2f} kg
                            Total Fees Collected  : Rs. {total_fee:.2f}

                            BY CATEGORY
                            -----------
                            Recyclable            : {recyclable} items
                            Hazardous             : {hazardous} items
                            Non-Recyclable        : {non_recyclable} items

                            BY STATUS
                            ---------
                            Stored                : {stored} items
                            Recycled              : {recycled} items
                            Disposed              : {disposed} items

                            ITEM DETAILS
                            ------------
                    """

    for item in filtered:
        fee = item['weight'] * item['fee_per_kg']
        report_content += (f"ID: {item['item_id']} | "
                           f"{item['device_name']} | "
                           f"{item['category']} | "
                           f"{item['weight']}kg | "
                           f"Rs.{fee:.2f} | "
                           f"{item['storage_status']}\n")

    report_content += "\n================================================\n"

    # print to screen
    print(report_content)

    # save to file
    file_name = f"report_{report_label.lower()}_{period.replace(' ', '_')}.txt"
    with open(file_name, "w") as f:
        f.write(report_content)

    print(f"Report saved as: {file_name}\n")

# main selection logic
while True:
    main_menu()
    check_hazard_alert()
    choice = int(input("Enter Menu Item No: "))
    # storage_check()
    match choice:
        case 1:
            display_items()
        case 2:
            add_item()
        case 3:
            update_item()
        case 4:
            delete_item()
        case 5:
            search_item()
        case 6:
            calculate_fee()
        case 7:
            generate_report()
        case 8:
            check_hazard_alert()
        case 9:
            save_data()
            print("Data saved successfully. Good Bye!!!\n")
            exit()
        case 10:
            storage_check()
        case _:
            print("Invalid choice")

# //*def load_data():
# //*def save_data():
# //*def add_item():
# //*def update_item():
# //*def delete_item():
# //*def search_item():
# //*def calculate_fee():
# //*def hazard_alert():
# //*def check_storage():
# //*def generate_report():