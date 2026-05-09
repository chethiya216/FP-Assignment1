awems = []

while True:

    choice = int(input("Enter Menu Item No: "))
    match choice:
        case 1:
                main_menu()
        case 2;
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