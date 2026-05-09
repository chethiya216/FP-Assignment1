from datetime import datetime

awems = []

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

# def load_data():
# def save_data():
# def add_item():
# def update_item():
# def delete_item():
# def search_item():
# def calculate_fee(weight, fee_per_kg):
# def hazard_alert():
# def check_storage():
# def generate_report():

# to automatically generate next item ID
def generate_id():
    if len(awems) == 0:
        return "EW001"
    else:
        last_id = awems[-1][0][-3:]
        new_id = int(last_id) + 1
        new_id = f"EW{new_id:03d}"
        return new_id

def display_items():
    if len(awems) == 0:
        print("No items available.\n")
        return
    else:
        print("All items:")
        print(f"{'Item ID':<20} {'Device Name':<20} {'Category':<20} {'Weight':<20} {'Storage Status':<20} {'Fee/kg':<20} {'Date Added':<20}")
        for item in awems:
            print(f"{item[0]:<20} {item[1]:<20} {item[2]:<20} {item[3]:<20} {item[4]:<20} {item[5]:<20} {item[6]:<20}")

def add_item():
    new_id = generate_id()
    print(f"Item ID: {new_id}")
    item_id = new_id
    item_name = input(("Enter item name: "))
    item_category = input("Enter item category: ")
    item_weight = float(input("Enter item weight in KG: "))
    item_storage_status = input("Enter item storage status: ")
    item_fee_per_kg = float(input("Enter item fee per KG: "))
    date_added = datetime.now().strftime("%d/%m/%Y")
    item = (item_id, item_name,item_category,item_weight,item_storage_status, item_fee_per_kg,date_added)
    awems.append(item)
    print("Item added successfully.")


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