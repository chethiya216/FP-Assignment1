from datetime import datetime  # to get current date and time

# to create empty list to store data
awems = []

# txt file name
FILE_NAME = "awems_data.txt"
MAX_CAPACITY = 1000  # in kg

# to load data from txt file when program starts


def load_data():
    """
    Load all saved e-waste records from the txt file on program startup.
    Reads each line, splits by '|', and stores as a dictionary in the awems list.
    If the file does not exist, the program starts with an empty list.
    """

    try:
        with open(FILE_NAME, "r") as file:
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


def storage_check():
    """
    Check the current total storage usage against the maximum capacity of 1000kg.
    Displays total used, total capacity, usage percentage, and available space.
    Prints a warning if usage exceeds 80% and an alert if storage is completely full.
    """

    storage_capacity = 1000  # in kg
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
    """
    Save all current e-waste records to the txt file before program exit.
    Each item is written as a single line with fields separated by '|'.
    Ensures no data is lost between sessions.
    """

    with open(FILE_NAME, "w") as file:
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
    """
    Display the main navigation menu for the Green Lantern Corps AEWMS.
    Shows all available options numbered 1 through 11.
    """

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
    """
    Automatically generate the next unique item ID in the format EW001, EW002, EW003.
    Reads the last item ID in the list, extracts the number, increments by 1,
    and returns the new ID formatted with leading zeros.
    Returns 'EW001' if the list is empty.
    """

    if len(awems) == 0:
        return "EW001"
    else:
        last_id = awems[-1]["item_id"][2:]
        new_id = int(last_id) + 1
        new_id = f"EW{new_id:03d}"
        return new_id


def get_weight(item):
    """
    Return the weight of an item as a float.
    Used as a key function for sorting items by weight.
    """

    return float(item['weight'])


def get_category(item):
    """
    Return the category of an item as a string.
    Used as a key function for sorting items alphabetically by category.
    """

    return item['category']


def display_items():
    """
    Display all e-waste items currently stored in the system.
    Offers three display options:
        1. Default order (order items were added)
        2. Sorted by weight from highest to lowest
        3. Sorted by category alphabetically
    Creates a copy of the list before sorting to not affect the original order.
    """
    if len(awems) == 0:
        print("No items available.\n")
        return

    print("\n--- Display Options ---")
    print("1. Default (Order Added)")
    print("2. Sort by Weight (Highest to Lowest)")
    print("3. Sort by Category")

    sort_choice = input("Select an option (1-3): ").strip()

    if sort_choice == "":
        sort_choice = "1"

    if sort_choice not in ["1", "2", "3"]:
        print("Invalid choice. Defaulting to option 1.")
        sort_choice = "1"
    else:
        sort_choice = int(sort_choice)

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
            print("\n--- Inventory Sorted by Category ---")
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
    """
    Add a new e-waste item to the system with full input validation.
    Automatically generates item ID and sets storage status to 'Stored'.
    Validates: item name (not empty), category (1-3 only), weight (positive number),
    fee per kg (positive number), and storage capacity (blocks if full).
    Saves updated records to file after successful addition.
    """

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
    """
    Delete an existing e-waste item from the system by item ID.
    Searches the list for a matching ID and removes it if found.
    Saves updated records to file after successful deletion.
    Prints an error message if the item ID is not found.
    """

    if not awems:
        print("No items found.")
        return

    item_id = input("Enter item ID to delete: ")

    while item_id.strip() == "":
        print("Item ID cannot be empty.")
        item_id = input("Enter item ID to delete: ").strip()

    while item_id not in [item["item_id"] for item in awems]:
        print("Item not found.")
        item_id = input("Enter item ID to delete: ").strip()

    print(f"Attempting to delete item with ID: {item_id}")
    print("1.Confirm Deletion")
    print("2.Cancel")

    choice = input("Enter your choice: ").strip()
    if choice == "1":
        for item in awems:
            if item["item_id"] == item_id:
                awems.remove(item)
                save_data()
                print("\nItem deleted successfully.------------\n")
                break
    else:
        print("Deletion cancelled.")


def update_item():
    """
    Update the details of an existing e-waste item by item ID.
    Allows updating: device name, category, storage status, weight, and fee per kg.
    Leaving any field blank keeps the current value unchanged.
    Saves updated records to file after successful update.
    """
    if not awems:
        print("No items available to update.\n")
        return

    # loop until a valid item ID is entered or user cancels
    while True:
        item_id = input(
            "Enter item ID to update (or type 'exit' to cancel): ").strip()

        if item_id.lower() == 'exit':
            print("Update cancelled.\n")
            return

        # to search for the item
        found_item = None
        for item in awems:
            if item["item_id"].strip().lower() == item_id.lower():
                found_item = item
                break

        if found_item:
            break  # Item found, exit the loop
        else:
            print(f"Item with ID '{item_id}' not found. Please try again.\n")

    # to show the updating field
    print(
        f"\nUpdating Item: {found_item['item_id']} - {found_item['device_name']}\n")

    print(f"Current Name : {found_item['device_name']}")
    new_name = input("Enter new name (leave blank to keep current): ").strip()
    if new_name:
        found_item["device_name"] = new_name

    print(f"Current Category : {found_item['category']}")
    new_category = input(
        "Choose new category (1. Recyclable / 2. Hazardous / 3. Non-Recyclable) (leave blank to keep current): ").strip()
    while new_category and new_category not in ["1", "2", "3"]:
        print("Invalid category input. Please enter 1, 2, or 3.")
        new_category = input(
            "Choose new category (1. Recyclable / 2. Hazardous / 3. Non-Recyclable) (leave blank to keep current): ").strip()
    if new_category:
        match new_category:
            case "1":
                new_category = "Recyclable"
            case "2":
                new_category = "Hazardous"
            case "3":
                new_category = "Non-Recyclable"
            case _:
                print("Invalid category input. Keeping old value.")
                new_category = None
    if new_category:
        found_item["category"] = new_category

    print(f"Current Status : {found_item['storage_status']}")
    new_status = input(
        "Choose new status (1. Stored / 2. Recycled / 3. Disposed) (leave blank to keep current): ").strip()
    while new_status and new_status not in ["1", "2", "3"]:
        print("Invalid status input. Please enter 1, 2, or 3.")
        new_status = input(
            "Choose new status (1. Stored / 2. Recycled / 3. Disposed) (leave blank to keep current): ").strip()
    if new_status:
        match new_status:
            case "1":
                new_status = "Stored"
            case "2":
                new_status = "Recycled"
            case "3":
                new_status = "Disposed"
            case _:
                print("Invalid status input. Keeping old value.")
                new_status = None
    if new_status:
        found_item["storage_status"] = new_status

    print(f"Current Weight : {found_item['weight']} kg")
    new_weight = input(
        "Enter new weight in kg (leave blank to keep current): ").strip()
    if new_weight:
        try:
            weight_value = float(new_weight)
            if weight_value <= 0:
                print("Warning: Weight must be positive. Keeping old value.")
            else:
                found_item["weight"] = weight_value
        except ValueError:
            print("Invalid weight input. Keeping old value.")

    print(f"Current Fee per kg : {found_item['fee_per_kg']}")
    new_fee = input(
        "Enter new fee per kg (leave blank to keep current): ").strip()
    if new_fee:
        try:
            fee_value = float(new_fee)
            if fee_value <= 0:
                print("Warning: Fee must be positive. Keeping old value.")
            else:
                found_item["fee_per_kg"] = fee_value
        except ValueError:
            print("Invalid fee input. Keeping old value.")

    save_data()
    print(f"\nItem {found_item['item_id']} updated successfully!\n")


def search_item():
    """
    Search for e-waste items by item ID or device name.
    Performs a case-insensitive partial match search across both fields.
    Displays all matching results or a not found message if no matches exist.
    """

    if not awems:
        print("No items available to search.\n")
        return

    search_text = input(
        "Enter item ID or Item Name to search: ").strip().lower()

    while search_text == "":
        print("Search text cannot be empty.\n")
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
    """
    Calculate the recycling fee for a specific e-waste item by item ID.
    Formula: Total Fee = Weight x Fee per kg.
    Applies a 5% bulk discount if the item weight exceeds 50kg.
    Displays a formatted receipt showing base fee, discount, and final total.
    """
    if not awems:
        print("No items available to calculate fee.\n")
        return

    item_id = input("Enter item ID to calculate fee: ").strip()
    found = False

    for item in awems:
        if item["item_id"].lower() == item_id.lower():
            found = True

            weight = float(item["weight"])
            fee_per_kg = float(item["fee_per_kg"])
            base_fee = weight * fee_per_kg

            discount = 0
            final_fee = base_fee

            if weight > 50:
                discount = base_fee * 0.05  # Apply 5% discount for bulk weight over 50kg
                final_fee = base_fee - discount

            # --- RECEIPT ---
            print("\n" + "*"*40)
            print("      GREEN LANTERN CORPS RECYCLERS")
            print("           OFFICIAL RECEIPT")
            print("*"*40)
            print(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            print(f"Item ID    : {item['item_id']}")
            print(f"Device     : {item['device_name']}")
            print(f"Category   : {item['category']}")
            print("-" * 40)
            print(f"Weight     : {weight:>20.2f} kg")
            print(f"Rate/kg    : {fee_per_kg:>20.2f} Rs")
            print(f"Base Fee   : {base_fee:>20.2f} Rs")

            if discount > 0:
                print(f"Bulk Disc. : -{discount:>19.2f} Rs (5%)")

            print("-" * 40)
            print(f"TOTAL DUE  : {final_fee:>20.2f} Rs")
            print("*"*40)
            print("    Thank you for recycling with us!")
            print("*"*40 + "\n")
            return

    if not found:
        print(f"\n[!] Error: Item ID '{item_id}' not found.\n")


# to check hazardous items and alert if they are stored for over 30 days
def check_hazard_alert(automatic=False):
    """
    Check hazardous items stored for more than 30 days and display warning alerts.

    The function also calculates the total weight for each category and warns
    if any category exceeds 80% of the maximum storage capacity.

    Parameters:
        automatic (bool):
            True  - Shows only important alerts and warnings.
            False - Shows a full hazard and storage report.
    """

    today = datetime.now()
    found_hazard = False
    hazard_alerts = []

    # to process all hazards
    for item in awems:

        if item["category"].lower() == "hazardous" and item["storage_status"].lower() == "stored":

            date_string = item["date_added"].split(" -- ")[0]
            date_added = datetime.strptime(date_string, "%d/%m/%Y")
            time_difference = (today - date_added).days

            if time_difference > 30:
                hazard_alerts.append(
                    f"ALERT: Item {item['item_id']} ({item['device_name']}) - {time_difference} days overdue! ")
                found_hazard = True

    # to calculate total weight per category
    total_weight_per_category = {}

    for item in awems:
        cat = item["category"]
        weight = item["weight"]
        total_weight_per_category[cat] = total_weight_per_category.get(
            cat, 0) + weight

    # to handle whether automatic or manual check
    if automatic:
        # SILENT MODE: Only print if there is a problem
        if found_hazard:
            print("\n--- URGENT DISPOSAL REQUIRED ---")

            for alert in hazard_alerts:
                print(alert)

        for category, total_weight in total_weight_per_category.items():
            percentage = (total_weight / MAX_CAPACITY) * 100

            if percentage > 80:
                print(
                    f"WARNING: {category} exceeds 80% capacity ({percentage:.1f}%)")
    else:
        # to show everything in a detailed report when manually checking
        print("\n" + "="*10 + " STORAGE & HAZARD REPORT " + "="*10)

        if not found_hazard:
            print("No overdue hazardous items.")
        else:
            for alert in hazard_alerts:
                print(alert)

        print("\n--- Weight Breakdown ---")
        for category, total_weight in total_weight_per_category.items():
            percentage = (total_weight / MAX_CAPACITY) * 100
            print(f"{category}: {total_weight:.2f} kg ({percentage:.1f}%)")
        print("=" * 45 + "\n")


def mark_item_status():
    """
    Update the storage status of an e-waste item to 'Recycled' or 'Disposed'.
    User enters the item ID and selects the new status from a numbered menu.
    Saves updated records to file after successful status change.
    Prints an error message if the item ID is not found.
    """

    if not awems:
        print("No items found.")
        return

    item_id = input("Enter item ID to mark: ").strip()

    while item_id == "":
        print("Item ID cannot be empty.")
        item_id = input("Enter item ID to mark: ").strip()

    while True:
        try:
            status_choice = int(
                input("Select new status (1. Recycled | 2. Disposed): "))
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
    """
    Generate a summary report for a selected time period (Daily, Monthly, or Yearly).
    Filters items from the awems list based on their date_added field.
    Report includes: total items, total weight, total fees collected,
    item counts by category, item counts by status, and individual item details.
    Saves the report as a formatted txt file and prints it to the console.
    """
    if not awems:
        print("No items available to generate report.\n")
        return

    print("\n--- Green Lantern Corps Recyclers ---")
    print("1. Daily Report")
    print("2. Monthly Report")
    print("3. Yearly Report")

    while True:
        try:
            report_type = int(input("Select report type: ").strip())
            if report_type in [1, 2, 3]:
                break
            print("Enter 1, 2 or 3.")
        except ValueError:
            print("Enter a valid number.")

    report_data = []
    today = datetime.now()

    for item in awems:
        item_date = datetime.strptime(
            item["date_added"].split(" -- ")[0], "%d/%m/%Y")

        if report_type == 1:
            if (item_date.day == today.day and
                    item_date.month == today.month and
                    item_date.year == today.year):
                report_data.append(item)

        elif report_type == 2:
            if (item_date.month == today.month and
                    item_date.year == today.year):
                report_data.append(item)

        elif report_type == 3:
            if item_date.year == today.year:
                report_data.append(item)

    # to calculate totals
    total_items = len(report_data)
    total_weight = sum(item['weight'] for item in report_data)
    total_fee = sum(item['weight'] * item['fee_per_kg'] for item in report_data)

    # to check category counts
    recyclable = len([i for i in report_data if i["category"] == "Recyclable"])
    hazardous = len([i for i in report_data if i["category"] == "Hazardous"])
    non_recyclable = len(
        [i for i in report_data if i["category"] == "Non-Recyclable"])

    # to check status count
    stored = len([i for i in report_data if i["storage_status"] == "Stored"])
    recycled = len([i for i in report_data if i["storage_status"] == "Recycled"])
    disposed = len([i for i in report_data if i["storage_status"] == "Disposed"])

    # to select report label and period
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
    separator = "=" * 80
    report_content = f"""
{separator}
                    GREEN LANTERN CORPS AEWMS
                    {report_label} Report - {period}
                    Generated: {today.strftime("%Y-%m-%d %H:%M:%S")}
{separator}

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

{separator}
                         ITEM DETAILS
{separator}
"""

    # to add column headers
    report_content += f"{'ID':<8} {'Device Name':<20} {'Category':<15} {'Weight':<8} {'Fee (Rs.)':<12} {'Status':<10}\n"
    report_content += "-" * 80 + "\n"

    # to add each item with fixed column widths
    for item in report_data:
        fee = item['weight'] * item['fee_per_kg']
        report_content += (f"{item['item_id']:<8} "
                           f"{item['device_name']:<20} "
                           f"{item['category']:<15} "
                           f"{item['weight']:<8.2f} "
                           f"{fee:<12.2f} "
                           f"{item['storage_status']:<10}\n")

    report_content += f"\n{separator}\n"

    # to display report
    print(report_content)

    # to save to file
    FILE_NAME = f"report_{report_label.lower()}_{period.replace(' ', '_')}.txt"
    with open(FILE_NAME, "w") as f:
        f.write(report_content)

    print(f"Report saved as: {FILE_NAME}\n")

# main selection logic
while True:
    main_menu()  # to show the main menu

    # automatically check for hazardous items on every menu load
    check_hazard_alert(automatic=True)

    try:
        choice = int(input("\nSelect an option (1-11): "))

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

    except Exception as e:
        print(f"An error occurred: {e}")