import subprocess

def display_menu():
    print("IDENTIFICATION PROGRAM\n")
    print("Choose An Option:")
    print("1. Object Identification")
    print("2. Color Identification")
    print("3. Length Measurement")
    print("0. Exit")
    print("\nMade By: Aymaan Perwez")

def execute_option(option):
    if option == 1:
        subprocess.run(['python', 'amo.py'])
    elif option == 2:
        subprocess.run(['python', 'second.py'])
    elif option == 3:
        subprocess.run(['python', 'regards.py'])
    elif option == 0:
        print("Exiting program.")
    else:
        print("Invalid option")

def ask_to_run_again():
    return input("Do you want to run the program again? (yes/no): ").lower() == 'yes'

if __name__ == "__main__":
    while True:
        display_menu()
        user_choice = int(input("Select From The 3 Options (0-3): "))

        if user_choice == 0:
            print("Exiting program.")
            break  # Exit the loop if the user chooses 0
        else:
            execute_option(user_choice)

        run_again = ask_to_run_again()
        if not run_again:
            print("Exiting program.")
            break
