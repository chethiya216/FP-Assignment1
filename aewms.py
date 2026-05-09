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


def view_all_items():
    if len(awems) == 0:
        print("No items available.\n")
        return
    else:
        for item in awems:
            print("All items:")
            print(item)


while True:
    main_menu()
    choice = int(input("Enter Menu Item No: "))
    match choice:
        case 1:
                view_all_items()
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