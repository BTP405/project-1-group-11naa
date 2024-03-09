import hashlib
import os
from dotenv import load_dotenv
load_dotenv()
import uuid
import supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")


# ########### DATABASE FUNCTIONS ##########
def createConnection():
    '''Creates a connection to the database that stores all the login info for users'''
    supabase_client = supabase.create_client(url, key)
    return supabase_client

supabase_client = createConnection()
########### DATABASE FUNCTIONS ##########
def createAccount(username, password):
    '''Create a new user account'''
    # use Secure Hash Algorithm for cryptographic security for the password
    # hexdigest for string representation of the hash
    hashedPass = hashlib.sha256(password.encode()).hexdigest()
    # Create accounts table if not exists
    supabase_client.table('accounts').insert({'username': username, 'password': hashedPass}).execute()

def authenticateAccount(username, password):
    '''Authenticate a user account'''
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # Retrieve account from Supabase
    response = supabase_client.table('accounts').select('*').eq('username', username).eq('password', hashed_password).execute()
    print(f'Response: {response}')
    account = response.data
    # print(f'IDDDDDD: {account[0]['id']}')
    if account:
        print(f"Authentication successful!")
        # Return the userID
        return account[0]['id']
    else:
        print("Invalid username or password.")
        return None

def getAccountDetails():
    '''Asks for user input for a username and password for register or login purposes'''
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    return (username, password)