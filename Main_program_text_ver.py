from Functions_text_ver import *
import os
alfa_chars, digit_chars, spec_symbols, all_chars_ordered = all_chars()
file_found = False
current_file_folder_path = r"V:\Python projects\IdeaProjects\password_manger_project"
file_name = "hidden_file.txt"
chosen_file = current_file_folder_path + "\\" + file_name
files_in_fold = os.listdir(current_file_folder_path)
passwords = {}


# Checks if the default file inside the same folder
# True: Just read the file continue
# False or File found but bugged: Ask user for path of the need file or ask user if he/she want to make a new file
if file_name not in files_in_fold:
    while True:
        user_input = input('Did you already save your passwords?(Yes or no): ').casefold()
        if user_input == "yes":
            file_path = input("Give the exact path to the file: ")
            try:
                passwords, char_to_key, key_to_char, de_encryption_order, de_encryption_keys = \
                    read_passwords_file(file_path)
                file_found = True
                chosen_file = file_path
                break
            except WrongFile:
                print("Not the right file")
            except FileNotFoundError:
                print("Could not find that file")
            except PermissionError:
                print("I do not have permissions for that file")
        elif user_input == "no":
            file_found = False
            passwords, char_to_key, key_to_char, de_encryption_order, de_encryption_keys = {}, None, None, None, None
            chosen_file = os.getcwd() + "\\hidden_file.txt"
            break
        else:
            print("yes or no please")
else:
    while True:
        while True:
            ask_user = input("Password file found. Want to use this file?(yes or no)"
                             ": ").casefold()
            if ask_user == "yes" or ask_user == "no":
                break
            else:
                print("Please give yes or no")
        if ask_user == "yes":
            try:
                passwords, char_to_key, key_to_char, de_encryption_order, de_encryption_keys = \
                    read_passwords_file(chosen_file)
                file_found = True
                chosen_file = current_file_folder_path + "\\" + file_name
                break
            except WrongFile:
                print("Sorry file did not work.")
                user_input = input('Did you already save your passwords?(Yes or no): ').casefold()
                if user_input == "yes":
                    file_path = input("Give the exact path to the file: ")
                    try:
                        passwords, char_to_key, key_to_char, de_encryption_order, de_encryption_keys = \
                            read_passwords_file(file_path)
                        file_found = True
                        chosen_file = file_path
                        break
                    except WrongFile:
                        print("Not the right file")
                    except FileNotFoundError:
                        print("Could not find that file")
                    except PermissionError:
                        print("I do not have permissions for that file")
                elif user_input == "no":
                    file_found = False
                    passwords, char_to_key, key_to_char, de_encryption_order, de_encryption_keys = \
                        {}, None, None, None, None
                    chosen_file = os.getcwd() + "\\hidden_file.txt"
                    break
                else:
                    print("yes or no please")
        else:
            user_input = input('Did you already save your passwords?(Yes or no): ').casefold()
            if user_input == "yes":
                file_path = input("Give the exact path to the file: ")
                try:
                    passwords, char_to_key, key_to_char, de_encryption_order, de_encryption_keys = \
                        read_passwords_file(file_path)
                    file_found = True
                    chosen_file = file_path
                    break
                except WrongFile:
                    print("Not the right file")
                except FileNotFoundError:
                    print("Could not find that file")
                except PermissionError:
                    print("I do not have permissions for that file")
            elif user_input == "no":
                file_found = False
                passwords, char_to_key, key_to_char, de_encryption_order, de_encryption_keys = \
                    {}, None, None, None, None
                chosen_file = os.getcwd() + "\\hidden_file.txt"
                break
            else:
                print("yes or no please")

if not file_found:
    # Creating encryption Keys for not having a file
    key_to_char, char_to_key, de_encryption_order, de_encryption_keys = creating_encryption_key()

passwords_we_have = []
for password in passwords.keys():
    passwords_we_have.append(de_encrypting(password, key_to_char))
if "Program Password" in passwords_we_have:
    while True:
        sys_password = de_encrypting(passwords[encrypting("Program Password", char_to_key)], key_to_char)
        user_answer = input("What is the password for this program: ")
        if user_answer == sys_password:
            break
        else:
            print("Incorrect")
else:
    user_chose_password = False
    print("You need a password for accessing this file")
    while not user_chose_password:
        sys_password = input("What is the password(random for random password): ")
        if sys_password.casefold() == "random":
            sys_password = generate_random_password()
        print(f'This is your password: {sys_password}')
        while True:
            user_choice = input("You want this to be your password (yes or no): ").casefold()
            if user_choice == "yes":
                user_chose_password = True
                break
            elif user_choice == "no":
                break
            else:
                print("Yes or no please")
        passwords[encrypting("Program Password", char_to_key)] = encrypting(sys_password, char_to_key)

while True:
    # User decides if she/he want to look at passwords, create/edit passwords, or remove/delete passwords
    print("1: Look at passwords\n"
          "2: Create New password\n"
          "3: Edit exiting password\n"
          "4: Remove password\n"
          "0: exit")
    user_input = input("What do you want to do?(Give a number): ")
    if user_input == "0":
        break
    elif user_input == "1":
        if passwords:
            print_passwords(passwords, key_to_char)
        else:
            print("You do not have any passwords saved")
    elif user_input == "2":
        passwords = updating_passwords(passwords, key_to_char, char_to_key, user_input)
    elif user_input == "3":
        if passwords:
            passwords = updating_passwords(passwords, key_to_char, char_to_key, user_input)
        else:
            print("You do not have any passwords")
    elif user_input == "4":
        if passwords:
            passwords = updating_passwords(passwords, key_to_char, char_to_key, user_input)
        else:
            print("You do not have any passwords")
    else:
        print("Check input please")

# Encrypt passwords and write to txt file
while True:
    print(f'Chose the file path to save your passwords:\n'
          f'1: {chosen_file} (This is the default)\n'
          f'2: Create your own path')
    user_input = input("Type a number for what you want to do.: ")
    if user_input == "1":
        while True:
            user_choice = input(f'{chosen_file}\n'
                                f'Are you sure you want this to be where you keep your passwords?(yes or no): '
                                f'').casefold()
            if user_choice == "yes" or user_choice == "no":
                break
            else:
                print("Check input")
        if user_choice == "yes":
            write_passwords(passwords, char_to_key, key_to_char, chosen_file, de_encryption_order, de_encryption_keys)
            break
    elif user_input == "2":
        old_file_path = chosen_file
        chosen_file = input("Do not give a folder. Make a path to the folder then make the last part what you want the "
                            "file name to be."
                            "\nType path: ")
        while True:
            user_choice = input(f'{chosen_file}\n'
                                f'Are you sure you want this to be where you keep your passwords?(yes or no): '
                                f'').casefold()
            if user_choice == "yes" or user_choice == "no":
                break
            else:
                print("Check input")
        if user_choice == "yes":
            try:
                os.remove(old_file_path)
                write_passwords(
                    passwords, char_to_key, key_to_char, chosen_file, de_encryption_order, de_encryption_keys)
                break
            except FileNotFoundError:
                print("Check your file path. It did not work.")
    else:
        print("Please give a number")
print(f'The file path for your passwords is: \n'
      f'{chosen_file}')
# Updating python file so that it can automatically find the passwords
lines_of_code = []
with open("Main_program_text_ver.py", "r") as self:
    for line in self:
        lines_of_code.append(line)
with open("Main_program_text_ver.py", "w") as self:
    path_filename_index = chosen_file.rindex("\\")
    current_file_folder_path = chosen_file[0:path_filename_index]
    file_name = chosen_file[path_filename_index + 1:]
    lines_of_code[4] = f'current_file_folder_path = r"{current_file_folder_path}"\n'
    lines_of_code[5] = f'file_name = "{file_name}"\n'
    for line in lines_of_code:
        self.write(line)
