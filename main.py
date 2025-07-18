from core import admin, user

def main_menu():
    while True:
        print(\"\"\"
        [1] Admin Login
        [2] User Registration Request
        [3] User Login
        [0] Exit
        \"\"\")
        choice = input(\">> \")
        if choice == '1':
            if admin.admin_login():
                admin.admin_dashboard()
        elif choice == '2':
            user.user_request()
        elif choice == '3':
            user.user_login()
        elif choice == '0':
            print(\"Exiting...\")
            break
        else:
            print(\"Invalid choice. Try again.\")

if __name__ == '__main__':
    main_menu()
