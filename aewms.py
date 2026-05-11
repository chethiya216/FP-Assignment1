from datetime import datetime # to get current date and time

# to create empty list to store data
awems = []

# txt file name
File_Name = "awems_data.txt"

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
                        "fee_per_kg":float(data[4]),
                        "storage_status":data[5],
                        "date_added": data[6]
                    }
                    awems.append(item)
    except FileNotFoundError:
        pass

load_data()

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
    print("8. Exit")

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
    item_category = input("Enter item category: ")
    item_storage_status = input("Enter item storage status: ")
    item_weight = float(input("Enter item weight in kg: "))
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
            new_category = input("Enter new category (leave blank to keep current): ")
            if new_category:
                item["category"] = new_category

            print(f"Current Storage Status: {item['storage_status']}")
            new_storage_status = input("Enter new storage status (leave blank to keep current): ")
            if new_storage_status:
                item["storage_status"] = new_storage_status

            print(f"Current Weight: {item['weight']} kg")
            new_weight_input = input("Enter new weight in kg (leave blank to keep current): ")
            if new_weight_input:
                item["weight"] = float(new_weight_input)

            print(f"Current Fee per kg: {item['fee_per_kg']}")
            new_fee_input = input("Enter new fee per kg (leave blank to keep current): ")
            if new_fee_input:
                item["fee_per_kg"] = float(new_fee_input)

            save_data()
            print("\nItem updated successfully.------------\n")
            return
    print("\nItem not found.------------\n")

def search_item():
    item_id = input("Enter item ID to search: ")
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
                fee += fee * 0.05  # Add surcharge to total fee
                print("Surcharge applied: 5% for items over 50kg")
            print("Total payable fee: ", fee, "\n")
            return
    print("\nItem not found.------------\n")


#main selection logic
while True:
    main_menu()
    choice = int(input("Enter Menu Item No: "))
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
            exit()
        case _:
            print("Invalid choice")

# //*def load_data():
# //*def save_data():
# //*def add_item():
# //*def update_item():
# //*def delete_item():
# //*def search_item():
# def calculate_fee(weight, fee_per_kg):
# def hazard_alert():
# def check_storage():
# def generate_report():