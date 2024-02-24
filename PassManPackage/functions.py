import json, getpass, os, pyperclip, sys
from tabulate import tabulate
from termcolor import colored
from PassManPackage.utils import *

#Colors
success = colored('[+]', 'green', attrs=['blink'])
error = colored('[-]', 'red', attrs=['blink'])
info = colored('[.]', 'blue', attrs=['blink'])


#Initilize file names
master_user_data_file = 'master_user_data.json'
key_filename = 'encryption_key.key'


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
              return
          
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
        print(f"\n{success} Bye  ;)\n")
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