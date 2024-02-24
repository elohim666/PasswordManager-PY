from PassManPackage.functions import *
from PassManPackage.display import *


def entry_point():
    display_welcome_menu()
    while True:      
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
                    display_welcome_menu()
                    #clean?
                
            elif choice == 2:
                if os.path.exists(master_user_data_file) and os.path.getsize(master_user_data_file) != 0:
                    master_User = str(input("Enter your master username: "))
                    master_Pass = getpass.getpass("Enter your master password: ")
                    login_master(master_User, master_Pass)
    
                    #After successful login:
                    while True:
                        try:
                            display_loggedin_menu()
                            login_choice = int(input("Enter your choice: "))
                            loggedin_menu(login_choice, master_User)
                        except ValueError:
                            print(f"\n {info} Sorry, only integers are allowed as input. \n")
                else:
                    
                    print(f"\n{error} You are not registered yet. Please register first!.\n")
                    display_welcome_menu()
                  
                            
            elif choice  == 3:
                print(f"\n{info} Bye ;)\n")
                sys.exit()
            else :
                print(f"\n {info} Please choose in this range: {1,2,3} \n")
                display_welcome_menu()
        except ValueError:
            print(f"\n {info} Only integers are allowed as input. \n")
            display_welcome_menu()
      

if __name__ == "__main__":
    entry_point()


