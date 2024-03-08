import account
import database
import sqlite3

########## MAIN FUNCTION ##########
def main():
    conn = database.createConnection()
    choice = ""
    while choice != "x":
        # Main Menu
        print('''Welcome to Karaoke Songbook Manager!\nPlease choose between:
    1 - Register an Account
    2 - Sign Into an Existing Account
    x - Exit''')
        # Reset choice to empty string
        choice = ""
        
        while choice not in ['1', '2', 'x']:
            choice = input("> ")
            if choice not in ['1', '2', 'x']:
                print("Invalid choice. Please choose between 1 (Register), 2 (Login), or x (Exit)")

        if choice == "1":
            userPass = database.getAccountDetails()
            database.createAccount(conn, userPass[0], userPass[1])
        elif choice == "2":
            userPass = database.getAccountDetails()
            try:
                userID = database.authenticateAccount(conn, userPass[0], userPass[1])
                if userID is not None:
                    account.profileMenu(conn, userPass[0], userID)
            except sqlite3.OperationalError:
                print(f"No accounts exist in the database. Please make at least one account before trying to sign in.")
        else:
            print("Thank you for using Karaoke Songbook Manager!")
        print("\n")
    pass


if __name__ == "__main__":
    main()