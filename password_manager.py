
import json, hashlib, getpass, os, pyperclip, sys
from cryptography.fernet import Fernet
from tabulate import tabulate
from termcolor import colored, cprint

success = colored('[+]', 'green', attrs=['blink'])
error = colored('[-]', 'red', attrs=['blink'])
info = colored('[.]', 'blue', attrs=['blink'])

master_user_data_file = 'master_user_data.json'
key_filename = 'encryption_key.key'


#Hashing the master password
def hash_pass(Pass):
    sha256 = hashlib.sha256()
    sha256.update(Pass.encode())
    return sha256.hexdigest()

#Generating a secret symetric key
def generate_key():
   return Fernet.generate_key()

#Initilizing Fernet cipher with provided key
def initialize_cipher(key):
   return Fernet(key)

#Encrypting our passwords
def encrypt_password(cipher, Pass):
   return cipher.encrypt(Pass.encode()).decode()

#Decrypting our passwords
def decrypt_password(cipher, encrypted_Pass):
   return cipher.decrypt(encrypted_Pass.encode()).decode()


#Registering the user with master username and master password
def register(master_User,master_Pass):
   
   hashed_master_Pass = hash_pass(master_Pass) #Hash the master password
   master_user_data = {'master_User': master_User,'master_Pass': hashed_master_Pass}

   if os.path.exists(master_user_data_file) and os.path.getsize(master_user_data_file) == 0: #if the file exists and is empty
        json.dump(master_user_data, master_user_data_file)
    
   else:
        with open(master_user_data_file, 'x') as file:
           json.dump(master_user_data, file)
   print(f"\n{success} Registration complete! Welcome {master_User} ;)\n")


#Login-in the master user
def login_master(username, typed_Pass):
   try:
      with open(master_user_data_file, 'r') as file:
          master_user_data = json.load(file)
          
          if hash_pass(typed_Pass) == master_user_data.get('master_Pass') and username == master_user_data.get('master_User'):
              print(f"\n{success} Login Successful! Welccome {master_user_data.get('master_User')}!\n")
          else:
              print(f"\n{error} Invalid Master-login credentials!\n")
              sys.exit()
   except Exception:
       print(f"\n{error} You have not registered yet. Please do so!\n")
       sys.exit()


# View saved websites
def view_websites():
    try:
        with open('passwords.json', 'r') as data:
            view = json.load(data)
            print(f"\n{success}Those are the webstites you saved:\n")
            websites_list = []
            state = []
            for x in view:
                state.append("Credentials saved")
                websites_list.append(x['website']) 
            print(tabulate({"Websites": websites_list, "State": state}, headers="keys"))          
            print('\n')
    except FileNotFoundError:
        print(f"\n{error} You have not saved any passwords yet!\n")

#Saving a new password
def add_password(website,username, password):
    if not os.path.exists('passwords.json'):
        data=[]
    else:
        try:
            with open('passwords.json','r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []
    encrypted_password = encrypt_password(cipher, password)
    password_entry = {'website':website,'username': username ,'password':encrypted_password}
    data.append(password_entry)
    with open('passwords.json', 'w') as file:
        json.dump(data, file, indent=4)

#retreive a saved password
def get_password(website):
    if not os.path.exists('passwords.json'):
        print(f"\n{error} No credentials Have been saved yet :/ ")
        print(f"\n{success} Bye {master_User} ;)\n")
        sys.exit()
    try:
        with open('passwords.json','r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        data = []
    for entry in data:
        if entry['website'] == website:
            decrypted_password = decrypt_password(cipher, entry['password'])
            username = entry['username']
            tuple = decrypted_password , username
            return list(tuple)
    return None

    



# The actual program
 

#Load the existing encryption key or generate it if it doesn't exist
if os.path.exists(key_filename):
    with open(key_filename, 'rb') as key_file:
        key = key_file.read()
else:
    key = generate_key()
    with open(key_filename, 'wb') as key_file:
        key_file.write(key)
#initialize the cipher
cipher = initialize_cipher(key)


#Welcome menu
def display_welcome_menu():
    print("1. Register")
    print("2. Login")
    print("3. Quit")

#display login menu
def diplay_loggedin_menu():
    print("1. Add a password")
    print("2. Get a password")
    print("3. View saved websites")
    print("4. Quit")

#login menu
def loggedin_menu(login_choice, master_User):
    if login_choice == 1:
        website = str(input("Enter the website: "))
        username = str(input("Enter its username/e-mail: "))
        password = getpass.getpass("Entre its password: ")
        add_password(website, username,password)
        print(f"\n{success} Password added for {website}!\n")
    elif login_choice == 2:
        website = str(input("Enter the website: "))
        credentials = get_password(website) # credentials is a list
        if website and credentials:
            pyperclip.copy(credentials[0])
            print(f"\n{success} Credentials for {website} are:\n\n\tUsername/e-mail\t:\t{credentials[1]}\n\tPassword\t:\t{credentials[0]}\n\n{info} The password has been automatically copied to your clipboard!\n")
        else:
            print(f"\n{error} Credentials not found! Did you save any for '{website} ?\n"
                  f"\n{error} Use option 3 to see the websites you saved.\n")
    elif login_choice == 3:
        view_websites()
    elif login_choice == 4:
        print(f"\n{info} Bye {master_User} ;)\n")
        sys.exit()
    else:
        print(f"\n {info} Please choose in this range: {1,2,3,4} \n")
        


#The Program
        
while True:
    display_welcome_menu()
    try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            if os.path.exists(master_user_data_file) and os.path.getsize(master_user_data_file) != 0:
                print(f"\n{info} Master user already exists!!\n")
                sys.exit()
            else:
                master_User = str(input("Enter your master username: "))
                master_Pass = getpass.getpass("Enter your master password: ")
                register(master_User, master_Pass)
                #clean?
            
        elif choice == 2:
            if os.path.exists(master_user_data_file) and os.path.getsize(master_user_data_file) != 0:
                master_User = str(input("Enter your master username: "))
                master_Pass = getpass.getpass("Enter your master password: ")
                login_master(master_User, master_Pass)
            else:
                print(f"\n{error} You have not registered. Please do that.\n")
                sys.exit()
            #After successful login:
            while True:
                try:
                    diplay_loggedin_menu()
                    login_choice = int(input("Enter your choice: "))
                    loggedin_menu(login_choice, master_User)
                except ValueError:
                    print(f"\n {info} Sorry, only integers are allowed as input. \n")
        elif choice  == 3:
            print(f"\n{info} Bye ;)\n")
            break
        else :
            print(f"\n {info} Please choose in this range: {1,2,3} \n")
    except ValueError:
        print(f"\n {info} Only integers are allowed as input. \n")