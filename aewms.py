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


# to load data from txt file when program starts
load_data()


# to check storage capacity and alert if it is exceeded
def storage_check():
    storage_capacity = 1000  # in kg
    storage = 0
    total_storage = sum(float(item["weight"]) for item in awems)
    percentage = (total_storage / storage_capacity) * 100
    print(f"\n=== STORAGE CAPACITY STATUS ===")
    print(f"Total Used    : {total_storage:.2f} kg")
    print(f"Total Capacity: {storage_capacity} kg")
    print(f"Usage         : {percentage:.1f}%")
    print(f"Available     : {storage_capacity - total_storage:.2f} kg")

    # warn if over 80%
    if total_storage >= storage_capacity:
        print("ALERT: Storage is FULL. Cannot add more items!")
    elif total_storage > (storage_capacity * 0.8):
        print("WARNING: Storage exceeds 80% capacity!")
    else:
        print("Storage level is normal.")
    print("================================\n")


# to save data to txt file when program is closed
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
    print("\n" + "="*20 + " GREEN LANTERN CORPS AEWMS " + "="*20)
    print("1. View Current Inventory")
    print("2. Add New E-Waste Item")
    print("3. Update Existing Item")
    print("4. Delete Item")
    print("5. Search Item by ID or Device Name")
    print("6. Calculate Processing Fee")
    print("7. Generate Storage Reports")
    print("8. Mark Item as Recycled or Disposed")
    print("9. Check Hazardous Expiry (30 Days)")
    print("10. Check Storage Capacity (80% Warning)")
    print("11. Save & Exit")
    print("="*67)

# to automatically generate next item ID


def generate_id():
    if len(awems) == 0:
        return "EW001"
    else:
        last_id = awems[-1]["item_id"][2:]
        new_id = int(last_id) + 1
        new_id = f"EW{new_id:03d}"
        return new_id


def get_weight(item):
    return float(item['weight'])


def get_category(item):
    return item['category']

# to display all items


def display_items():
    if len(awems) == 0:
        print("No items available.\n")
        return

    print("\n--- Display Options ---")
    print("1. Default (Order Added)")
    print("2. Sort by Weight (Highest to Lowest)")
    print("3. Sort by Category")
    sort_choice = input("Select an option (1-3): ")

    try:
        while sort_choice not in ["1", "2", "3"]:
            print("Invalid choice. Defaulting to option 1.")
            sort_choice = "1"
        sort_choice = int(sort_choice)
    except ValueError:
        print("Invalid input. Chose between 1 - 3.")
        sort_choice = "1"

    # to make a copy of awems list so that original list isnt affected
    display_list = list(awems)

    match sort_choice:
        case 1:
            print("\n--- Current Inventory ---")
        case 2:
            # to make the list go from large numbers to small ones
            display_list.sort(key=get_weight, reverse=True)
            print("\n--- Inventory Sorted by Weight (Heavy -> Light) ---")
        case 3:
            display_list.sort(key=get_category)
            print("\n--- Inventory Sorted by Catagory ---")
        case _:
            print("Invalid choice. Defaulting to option 1.")

    for item in display_list:
        print(f"Item ID: {item['item_id']} |",
              f"Name: {item['device_name']} |",
              f"Category: {item['category']} |",
              f"Storage Status: {item['storage_status']} |",
              f"Weight: {item['weight']} |",
              f"Fee per kg: {item['fee_per_kg']} |",
              f"Date Added: {item['date_added']}\n")


# to add items
def add_item():
    current_total = sum(float(item["weight"])for item in awems)
    if current_total >= MAX_CAPACITY:
        print("ALERT: Storage is FULL. Cannot add more items!\n")
        return

    new_id = generate_id()
    print(f"Item ID: {new_id}")
    item_id = new_id

    item_name = input(("Enter item name: "))
    while item_name == "":
        print("Item name cannot be empty")
        item_name = input("Enter item name: ")

    while True:
        try:
            item_category = int(input(
                "Enter item category (1. Recyclable / 2. Hazardous / 3. Non-Recyclable) : "))
            match item_category:
                case 1:
                    item_category = "Recyclable"
                    break
                case 2:
                    item_category = "Hazardous"
                    break
                case 3:
                    item_category = "Non-Recyclable"
                    break
                case _:
                    print("Invalid category")
        except ValueError:
            print("Invalid Input. Enter a number.")

    item_storage_status = "Stored"  # default storage status

    current_total = sum(float(item['weight']) for item in awems)
    while True:
        try:
            item_weight = float(input(
                f"Enter item weight in kg (Current total: {current_total} kg / Maximum capacity: {MAX_CAPACITY} kg): "))
            if item_weight <= 0:
                print("Weight must be a positive number.")
                continue

            if current_total + item_weight > MAX_CAPACITY:
                print(
                    f"Cannot add item. Adding this item would exceed the maximum storage capacity of {MAX_CAPACITY} kg.\n")
                storage_check()
                return
            break

        except ValueError:
            print("Invalid weight. Please enter a number.")

    while True:
        try:
            item_fee_per_kg = float(input("Enter item fee per kg: "))
            if item_fee_per_kg <= 0:
                print("Fee cannot be negative.")
                continue
            break
        except ValueError:
            print("Invalid fee per kg. Enter only the amount without KG")

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
    search_text = input(
        "Enter item ID or Item Name to search: ").strip().lower()
    results = []

    for item in awems:
        if search_text in item["item_id"].lower() or search_text in item["device_name"].lower():
            results.append(item)

    if len(results) > 0:
        print(f"Found {len(results)} matches.")
        for match in results:
            print(f"Item ID         : {match['item_id']} |",
                  f"Name          : {match['device_name']} |",
                  f"Category      : {match['category']} |",
                  f"Storage Status: {match['storage_status']} |",
                  f"Weight        : {match['weight']} |",
                  f"Fee per kg    : {match['fee_per_kg']} |",
                  f"Date Added    : {match['date_added']}\n")
    else:
        print("\nNo matches found.------------\n")


# to calculate fee for an item
def calculate_fee():
    item_id = input("Enter item ID to calculate fee: ")
    for item in awems:
        if item["item_id"] == item_id:
            weight = float(item["weight"])
            fee_per_kg = float(item["fee_per_kg"])
            fee = weight * fee_per_kg  # Apply 5% surcharge for items over 50kg
            print("Total weight: ", weight, "kg")
            print("Fee per kg: ", fee_per_kg)
            if weight > 50:
                discount = fee * 0.05
                fee -= discount
                print("Discount applied: 5% for items over 50kg")
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
                print(
                    f"ALERT: Item {item['item_id']} ({item['device_name']}) Stored for {time_difference} days. Urgent disposal required!\n")


def mark_item_status():
    item_id = input("Enter item ID to mark: ")

    while True:
        try:
            status_choice = int(input("Select new status (1. Recycled | 2. Disposed): "))
            if status_choice in [1, 2]:
                break
            print("Enter a number between 1 and 2.")
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 2.")

    match status_choice:
        case 1:
            new_status = "Recycled"
        case 2:
            new_status = "Disposed"

    for item in awems:
        if item["item_id"] == item_id:
            item["storage_status"] = new_status
            save_data()
            print(f"\nItem {item_id} marked as {new_status}.------------\n")
            return
    print("\nItem not found.------------\n")


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

    # calculate totals
    total_items = len(filtered)
    total_weight = sum(item['weight'] for item in filtered)
    total_fee = sum(item['weight'] * item['fee_per_kg'] for item in filtered)

    # check category counts
    recyclable = len([i for i in filtered if i["category"] == "Recyclable"])
    hazardous = len([i for i in filtered if i["category"] == "Hazardous"])
    non_recyclable = len(
        [i for i in filtered if i["category"] == "Non-Recyclable"])

    # check status count
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

    # to build the report
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

    # to show
    print(report_content)

    # to save to a file
    file_name = f"report_{report_label.lower()}_{period.replace(' ', '_')}.txt"
    with open(file_name, "w") as f:
        f.write(report_content)

    print(f"Report saved as: {file_name}\n")


# main selection logic
while True:
    main_menu()  # to show the main menu

    check_hazard_alert()  # automatically check for hazardous items on every menu load

    try:
        choice = int(input("Select an option (1-10): "))

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
                mark_item_status()  # to manually mark items as recycled or disposed
            case 9:
                check_hazard_alert()  # to manually check
            case 10:
                storage_check()
            case 11:
                save_data()
                print("Inventory saved to file. System shutting down. Goodbye!")
                break
            case _:
                print("Invalid choice. Please select 1 through 11.")

    except ValueError:
        print("Invalid input! Please enter a number between 1 and 11.")

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
