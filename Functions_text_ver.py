import random
from random import randint
import ast


class WrongFile(FileNotFoundError):
    def __init__(self, message):
        self.message = message


def all_chars():
    alfa_chars = list("AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz ")
    digit_chars = list("1234567890")
    spec_symbols = list("`~!@#$%^&*()-_=+[{]}\\|;:',<.>/?" + '"')
    all_chars_ordered = alfa_chars + digit_chars + spec_symbols
    return alfa_chars, digit_chars, spec_symbols, all_chars_ordered


def creating_encryption_key():
    alfa_chars, digit_chars, spec_symbols, all_chars_ordered = all_chars()
    all_chars_random = alfa_chars + digit_chars + spec_symbols
    all_chars_order = all_chars_random.copy()
    random.shuffle(all_chars_random)
    single_chars,  double_chars, triple_chars = create_single_double_triple_chars()
    key_to_char = {}
    char_to_key = {}
    random_encrypted_codes = single_chars + double_chars + triple_chars
    random.shuffle(random_encrypted_codes)
    for char in all_chars_order:
        key_to_char[random_encrypted_codes.pop(randint(0, len(random_encrypted_codes) - 1))] = char
    for key, item in key_to_char.items():
        char_to_key[item] = key
    de_encryption_order = []
    de_encryption_keys = []
    for _ in range(0, randint(7, 11)):
        de_encryption_keys.append(triple_chars.pop(randint(0, len(triple_chars)-1)))
    for _ in range(0, len(char_to_key)):
        de_encryption_order.append(de_encryption_keys[randint(0, len(de_encryption_keys)-1)])
    return key_to_char, char_to_key, de_encryption_order, de_encryption_keys


def updating_passwords(passwords: dict, key_to_char, char_to_key, user_choice: str):
    # User decided to create new password
    if user_choice == "2":
        while True:
            need_password_for = input("What you need a password for?(0 to exit): ")
            if need_password_for == "0":
                return passwords
            while True:
                user_choice = input(
                    f"Are you sure you need a password for: '{need_password_for}' (yes or no): ").casefold()
                if user_choice == "yes":
                    if encrypting(need_password_for, char_to_key) in passwords:
                        print("You already have a password for this.")
                    else:
                        break
                elif user_choice == "no":
                    need_password_for = input("What you need a password for?(0 to exit): ")
                else:
                    print('check input')
            password = input("What is the password?(random for random password): ")
            if password == "random":
                password = generate_random_password()
            while True:
                user_choice = input(f'Do you want {password} to be your password?(yes or no): ').casefold()
                if user_choice == "yes":
                    passwords[encrypting(need_password_for, char_to_key)] = encrypting(password, char_to_key)
                    break
                elif user_choice == "no":
                    password = input("What is the password?(random for random password): ")
                else:
                    print('check input')
    # User decided to edit existing password
    elif user_choice == "3":
        while True:
            passwords_for = []
            for key in passwords.keys():
                passwords_for.append(de_encrypting(key, key_to_char))
            print("Input 0 to exit")
            print_passwords(passwords, key_to_char)
            user_input = input("Give the corresponding number: ")
            if user_input == "0":
                return passwords
            if user_input.isdigit():
                user_input = int(user_input)
                if user_input <= len(passwords_for):
                    password_needed_change = passwords_for[user_input-1]
                    password = input("What is the password?(random for random password): ")
                    if password == "random":
                        password = generate_random_password()
                    while True:
                        user_choice = input(f'Do you want {password} to be your password?(yes or no): ').casefold()
                        if user_choice == "yes":
                            break
                        elif user_choice == "no":
                            password = input("What is the password?(random for random password): ")
                        else:
                            print('check input')
                    passwords[(encrypting(password_needed_change, char_to_key))] = encrypting(password, char_to_key)
                else:
                    print("Check input")
            else:
                print("Check input")
    elif user_choice == "4":
        while True:
            passwords_for = []
            for key in passwords.keys():
                passwords_for.append(de_encrypting(key, key_to_char))
            print("Input 0 to exit")
            print_passwords(passwords, key_to_char)
            user_input = input("Give the corresponding number: ")
            if user_input == "0":
                return passwords
            if user_input.isdigit():
                user_input = int(user_input)
                if user_input <= len(passwords_for):
                    password_needed_deleted = passwords_for[user_input-1]
                    if password_needed_deleted == "Program Password":
                        print("you can not delete the password for this file")
                    else:
                        del passwords[encrypting(password_needed_deleted, char_to_key)]
                else:
                    print("Check input")
            else:
                print("Check input")


def de_encrypting(encrypted_and_len_of_encryption, key_to_char):
    encrypted_password_, len_of_encryption_ = encrypted_and_len_of_encryption
    unencrypted_password_ = ""
    encrypted_password_index = 0
    for i in range(0, len(len_of_encryption_)):
        num_to_replace = int(len_of_encryption_[i])
        unencrypted_password_ += key_to_char[encrypted_password_[
                                             encrypted_password_index:encrypted_password_index + num_to_replace]]
        encrypted_password_index += num_to_replace
    return unencrypted_password_


def encrypting(str_to_encrypt, char_to_key):
    encrypted_str = ""
    len_of_encryption_str = []
    for char in str_to_encrypt:
        encrypted_str += char_to_key[char]
        len_of_encryption_str.append(len(char_to_key[char]))
    return encrypted_str, tuple(len_of_encryption_str)


def write_passwords(
        encrypted_passwords: dict, char_to_key: dict, key_to_char: dict, file_name: str,
        dictionary_key_order: list, key_for_dictionaries: list):
    # Makes sure file is a txt file
    if file_name[-4:] != ".txt":
        file_name += ".txt"
    single_chars,  double_chars, triple_chars = create_single_double_triple_chars()
    s_d_t_chars = single_chars + double_chars + triple_chars
    # The lists will hold the char to key translation. The index position will determine the corresponding pairs.
    char, key = [], []
    lists_of_scrambled_keys = []
    for _ in range(0, len(key_for_dictionaries)):
        lists_of_scrambled_keys.append([])
    for char_, key_ in char_to_key.items():
        char.append(char_)
        key.append(key_)
    # File will contain 5-10 lists of nested dictionaries.
    # The correct key will be in of the 5-10 lists
    for index, key_ in enumerate(dictionary_key_order):
        for i in range(0, len(lists_of_scrambled_keys)):
            if i == key_for_dictionaries.index(key_):
                lists_of_scrambled_keys[i].append({char[index]: key[index]})
            else:
                lists_of_scrambled_keys[i].append({char[index]: s_d_t_chars.pop(randint(0, len(s_d_t_chars)-1))})
    # Going to translate the encrypted passwords so that I can encrypt the dict with my passwords
    de_encrypted_passwords = {}
    for password_for, password in encrypted_passwords.items():
        de_encrypted_passwords[de_encrypting(password_for, key_to_char)] = de_encrypting(password, key_to_char)
    with open(file_name, "w") as file:
        # 07 indicates it's the right file
        print("07", file=file)
        print(dictionary_key_order, key_for_dictionaries, sep="\n", file=file)
        for encryption_list in lists_of_scrambled_keys:
            print(encryption_list, file=file)
        print("0111", file=file)
        for password_for in de_encrypted_passwords.keys():
            print(encrypting(password_for, char_to_key), file=file)
        print("0111", file=file)
        for _, passwords in de_encrypted_passwords.items():
            print(encrypting(passwords, char_to_key), file=file)
        print("0111", file=file)
    # Creating Second layer of encryption
    # Converting every character to the hexadecimal value
    # Saving each line to a list then convert each character in each line to a hexadecimal separated with a " | "
    lines_in_file = []
    with open(file_name, "r") as file:
        for line in file:
            lines_in_file.append(list(line.strip("\n")))
    for line in lines_in_file:
        for index, char in enumerate(line):
            line[index] = format(ord(char), "x")
            list_to_replace = list(line[index])
            for i, item in enumerate(list_to_replace):
                list_to_replace[i] = str(format(ord(list_to_replace[i]), "b"))
            line[index] = " | ".join(list_to_replace)
    with open(file_name, "w") as file:
        for line in lines_in_file:
            print(" : ".join(line), file=file)


def read_passwords_file(file_name):
    _, _, _, all_chars_ordered = all_chars()
    char_to_key = {}
    key_to_char = {}
    encrypted_passwords = {}
    # Checking if right file
    with open(file_name, "r") as file:
        first_line = file.readline().strip("\n")
        if first_line != "110011 | 110000 : 110011 | 110111":
            not_right_file = WrongFile("That is the wrong file")
            raise not_right_file
    if file_name[-3:] != "txt":
        raise not_right_file
    # Storing the lines of the txt file to a list
    lines_in_file = []
    with open(file_name, "r") as file:
        for lines in file:
            lines_in_file.append(lines.strip("\n"))
    # De-encrypting the first layer of encryption to write back into the file
    for line_index, line in enumerate(lines_in_file):
        holding_line = line.split(" : ")
        for index, item in enumerate(holding_line):
            bin_chars = item.split(" | ")
            for i, binary in enumerate(bin_chars):
                bin_chars[i] = chr(int(binary, 2))
            holding_line[index] = "".join(bin_chars)
        for index, item in enumerate(holding_line):
            hex_converted_int = int(item, 16)
            holding_line[index] = chr(hex_converted_int)
        lines_in_file[line_index] = "".join(holding_line)
    # Gathering the needed information
    current_line_index = 0
    _ = lines_in_file[current_line_index]
    current_line_index += 1
    de_encryption_order: list = ast.literal_eval(lines_in_file[current_line_index])
    current_line_index += 1
    de_encryption_keys: list = ast.literal_eval(lines_in_file[current_line_index])
    current_line_index += 1
    scrambled_lists = []
    while True:
        line = lines_in_file[current_line_index]
        current_line_index += 1
        # code 0111 is placed into my file to inform the code to STOP.
        if line == "0111":
            break
        else:
            scrambled_lists.append(ast.literal_eval(line))
    passwords_for = []
    passwords = []
    while True:
        line = lines_in_file[current_line_index]
        current_line_index += 1
        if line == "0111":
            break
        else:
            passwords_for.append(ast.literal_eval(line))
    while True:
        line = lines_in_file[current_line_index]
        current_line_index += 1
        if line == "0111":
            break
        else:
            passwords.append(ast.literal_eval(line))
    for i in range(0, len(passwords_for)):
        encrypted_passwords[passwords_for[i]] = passwords[i]
    for index, keys in enumerate(de_encryption_order):
        key_numeric_position = de_encryption_keys.index(keys)
        for ch, k in scrambled_lists[key_numeric_position][index].items():
            char_to_key[ch] = k
    for key, item in char_to_key.items():
        key_to_char[item] = key
    return encrypted_passwords, char_to_key, key_to_char, de_encryption_order, de_encryption_keys


def print_passwords(passwords: dict, key_to_char):
    for index, (password_for, password) in enumerate(passwords.items()):
        print(f'{index + 1}: \n'
              f'{de_encrypting(password_for, key_to_char)}: {de_encrypting(password, key_to_char)}')


def generate_random_password():
    alfa_chars, digit_chars, spec_symbols, all_chars_ordered = all_chars()
    password = ""
    alfa_used = []
    digit_used = []
    spec_symbols_used = []
    for _ in range(0, 12):
        alfa_used.append(alfa_chars[randint(0, len(alfa_chars)-1)])
    for _ in range(0, 6):
        digit_used.append(digit_chars[randint(0, len(digit_chars)-1)])
    for _ in range(0, 4):
        spec_symbols_used.append(spec_symbols[randint(0, len(spec_symbols)-1)])
    password_list = alfa_used + digit_used + spec_symbols_used
    random.shuffle(password_list)
    for char in password_list:
        password += char
    return password


def create_single_double_triple_chars():
    alfa_chars, digit_chars, spec_symbols, all_chars_ordered = all_chars()
    all_chars_random = all_chars_ordered.copy()
    random.shuffle(all_chars_random)
    single_chars = all_chars_random.copy()
    double_chars = []
    triple_chars = []
    for _ in range(0, 500):
        while True:
            char = all_chars_random[randint(0, len(all_chars_random) - 1)] + \
                   all_chars_random[randint(0, len(all_chars_random) - 1)]
            if char not in double_chars:
                double_chars.append(char)
                break
            else:
                pass

    for _ in range(0, 500):
        while True:
            char = all_chars_random[randint(0, len(all_chars_random) - 1)] + \
                   all_chars_random[randint(0, len(all_chars_random) - 1)] + \
                   all_chars_random[randint(0, len(all_chars_random) - 1)]
            if char not in triple_chars:
                triple_chars.append(char)
                break
            else:
                pass
    return single_chars.copy(), double_chars.copy(), triple_chars.copy()
