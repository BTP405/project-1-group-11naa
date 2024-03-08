import sqlite3
import hashlib

########### DATABASE FUNCTIONS ##########
def createConnection():
    '''Creates a connection to the database that stores all the login info for users'''
    conn = sqlite3.connect('karaoke.db')
    return conn

def createAccount(conn, username, password):
    '''Create a new user account'''
    # use Secure Hash Algorithm for cryptographic security for the password
    # hexdigest for string representation of the hash
    hashedPass = hashlib.sha256(password.encode()).hexdigest()
    # cursor object to execute SQL statements
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts
                (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)
                ''')
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS favorites
                (userID INTEGER, songID INTEGER UNIQUE, FOREIGN KEY(userID) REFERENCES accounts(id))
                ''')
    try:
        # create user account
        cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, hashedPass))

        # then commit the change to the database
        conn.commit()
        print(f"User '{username}' created successfully!")
    except sqlite3.IntegrityError:
        print(f"Username '{username} already exists. Please choose a different one.")
    cursor.close()

def authenticateAccount(conn, username, password):
    '''Authenticate a user account'''
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE username=? AND password=?", (username, hashed_password))
    account = cursor.fetchone()
    cursor.close()
    if account:
        print("Authentication successful!")
        # Return the userID
        return account[0]
    else:
        print("Invalid username or password.")
        return None

def getAccountDetails():
    '''Asks for user input for a username and password for register or login purposes'''
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    return (username, password)