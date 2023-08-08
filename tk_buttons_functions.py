import tkinter as tk
from tkinter import ttk
from Functions_text_ver import *
from tkinter.filedialog import askopenfilename, askdirectory
from typing import List, Tuple
import os


class PasswordManager(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.passwords = {}
        self.key_to_char = {}
        self.char_to_key = {}
        self.de_encryption_order = []
        self.de_encryption_keys = []

        self.file_path = tk.StringVar()

        self.get_file = GetFileFrame(self)
        self.home = HomeFrame(self)
        self.passwords_window = PasswordFrame(self)
        self.path_change = ChangeFilePathFrame(self)
        self.save = SaveFrame(self)

    def start_program(self):
        self.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.get_file.grid(row=0, column=0, sticky="nesw")
        self.home.grid(row=0, column=0, sticky="nesw")
        self.passwords_window.grid(row=0, column=0, sticky="nesw")
        self.path_change.grid(row=0, column=0, sticky="nesw")
        self.save.grid(row=0, column=0, sticky="nesw")

        self.get_file.tkraise()

        self.mainloop()

    def frame_swap(self, frame: str):
        if frame == "Get File":
            self.get_file.tkraise()
        elif frame == "Home":
            self.home.destroy()
            self.home = HomeFrame(self)
            self.home.grid(row=0, column=0, sticky="NESW")
            self.home.tkraise()
        elif frame == "Passwords":
            self.passwords_window.destroy()
            self.passwords_window = PasswordFrame(self)
            self.passwords_window.grid(row=0, column=0, sticky="NESW")
            self.passwords_window.tkraise()
        elif frame == "Change Path":
            self.path_change.destroy()
            self.path_change = ChangeFilePathFrame(self)
            self.path_change.grid(row=0, column=0, sticky="nesw")
            self.path_change.tkraise()
        elif frame == "Save":
            self.save.destroy()
            self.save = SaveFrame(self)
            self.save.grid(row=0, column=0, sticky="nesw")
            self.save.tkraise()


class GetFileFrame(ttk.Frame):
    def __init__(self, container: PasswordManager, **kwargs):
        super().__init__(container, **kwargs)
        self.container = container
        self.text_box = tk.StringVar()
        self.file_password = tk.StringVar()
        self.file_password.set("")

        self.text_box.set("Input the file path to your save file")
        ttk.Label(self, textvariable=self.text_box).grid(row=0, column=1, sticky="nesw")
        ttk.Separator(self).grid(row=1, column=0, columnspan=3, sticky="ew")

        self.file_entry = ttk.Entry(self, textvariable=container.file_path)
        ttk.Label(self, text="File: ").grid(row=2, sticky="nes", column=0)
        self.file_entry.grid(row=2, column=1, columnspan=2, sticky="nesw")

        new_file_button = ttk.Button(self, text="New File", command=self.new_file)
        select_file_button = ttk.Button(self, text="Select File", command=self.select_file)
        open_file_button = ttk.Button(self, text="Open", command=self.open_file)

        new_file_button.grid(row=3, column=0, sticky="nesw")
        select_file_button.grid(row=3, column=2, sticky="nesw")

        self.file_password_entry = tk.Entry(self, textvariable=self.file_password)

        ttk.Label(self, text="File Password: ").grid(row=4, column=0, columnspan=1, sticky="nes")
        self.file_password_entry.grid(row=4, column=1, columnspan=2, sticky="nesw")
        open_file_button.grid(row=5, column=2, sticky="nesw")

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=3)

        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=5)
        self.rowconfigure(4, weight=5)
        self.rowconfigure(5, weight=5)

    def new_file(self):
        self.container.file_path.set(os.getcwd() + "\\hidden_file.txt")
        self.container.key_to_char, self.container.char_to_key, self.container.de_encryption_order, \
            self.container.de_encryption_keys = creating_encryption_key()

        self.container.passwords = {
            encrypting("Program Password", self.container.char_to_key): encrypting("12345", self.container.char_to_key)
        }
        self.container.frame_swap("Home")

    def select_file(self):
        file_path = askopenfilename(filetypes=(("txt files", "*.txt"), ("All files", "*.*")))
        self.container.file_path.set(file_path)

    def open_file(self):
        try:
            self.container.passwords, self.container.char_to_key, self.container.key_to_char, \
                self.container.de_encryption_order, self.container.de_encryption_keys = \
                read_passwords_file(self.container.file_path.get())
            program_password = ""
            for key, item in self.container.passwords.items():
                if de_encrypting(key, self.container.key_to_char) == "Program Password":
                    program_password = item
            if self.file_password.get() == de_encrypting(program_password, self.container.key_to_char):
                self.container.frame_swap("Home")
            else:
                self.text_box.set("Password incorrect")
        except WrongFile:
            self.text_box.set("Wrong type of file")
        except FileNotFoundError:
            self.text_box.set("File path does not exist")


class HomeFrame(ttk.Frame):
    def __init__(self, container: PasswordManager, **kwargs):
        super().__init__(container, **kwargs)
        self.container = container

        tk_passwords_for = []
        tk_passwords = []
        for en_password_for, en_password in self.container.passwords.items():
            tk_passwords_for.append(de_encrypting(en_password_for, self.container.key_to_char))
            tk_passwords.append(de_encrypting(en_password, self.container.key_to_char))

        ttk.Label(self, text="Home Screen").grid(row=0, column=1, sticky="nesw")
        ttk.Separator(self).grid(row=1, column=0, columnspan=4, sticky="ew")

        edit_pass_button = ttk.Button(self,
                                      text="Edit Passwords",
                                      command=lambda: self.container.frame_swap("Passwords"))
        change_save_file = ttk.Button(self,
                                      text="Change File Location",
                                      command=lambda: self.container.frame_swap("Change Path"))
        save_passwords = ttk.Button(self,
                                    text="Save Passwords",
                                    command=lambda: self.container.frame_swap("Save"))
        select_file_button = ttk.Button(self,
                                        text="<- Back",
                                        command=lambda: self.container.frame_swap("Get File"))

        edit_pass_button.grid(row=2, columnspan=2, sticky="nesw", padx=10, pady=1)
        change_save_file.grid(row=3, columnspan=2, sticky="nesw", padx=10, pady=1)
        save_passwords.grid(row=4, columnspan=2, sticky="nesw", padx=10, pady=1)
        select_file_button.grid(row=5, sticky="nesw")

        pass_win = ttk.Frame(self)
        pass_win.grid(row=2, column=2, rowspan=4, sticky="nesw", padx=10, pady=5)

        self.columnconfigure(0, weight=2)
        self.columnconfigure(0, weight=5)
        self.columnconfigure(0, weight=5)

        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=5)
        self.rowconfigure(4, weight=5)
        self.rowconfigure(5, weight=5)

        width = 0
        for password in tk_passwords:
            if len(password) > width:
                width = len(password)

        for index, passwords_for in enumerate(tk_passwords_for):
            row_plot = index * 2
            ttk.Label(pass_win, text=passwords_for).grid(row=row_plot, column=0, sticky="nesw")
            ttk.Label(pass_win, text="Password: ").grid(row=row_plot, column=1, sticky="nes")
            password_text = tk.Text(pass_win, height=1, width=width+5)
            password_text.insert("1.0", tk_passwords[index])
            password_text["state"] = "disable"
            password_text.grid(row=row_plot, column=2, sticky="ew")
            ttk.Separator(pass_win).grid(row=row_plot+1, column=0, columnspan=3, sticky="ew")
            pass_win.rowconfigure(row_plot, weight=5)
            pass_win.rowconfigure(row_plot+1, weight=1)
        if not self.container.passwords:
            ttk.Label(pass_win, text="Passwords will be placed here").grid(sticky="new", pady=20)
            pass_win.columnconfigure(0, weight=1)
            pass_win.rowconfigure(0, weight=1)

        pass_win.columnconfigure(0, weight=1)
        pass_win.columnconfigure(1, weight=1)
        pass_win.columnconfigure(2, weight=1)


class PasswordFrame(ttk.Frame):
    def __init__(self, container: PasswordManager, **kwargs):
        super().__init__(container, **kwargs)
        self.container = container
        self.tk_passwords_for: List[tk.StringVar] = []
        self.tk_passwords: List[tk.StringVar] = []
        self.widget_groups: List[Tuple[ttk.Entry, ttk.Label, ttk.Entry, ttk.Button, ttk.Button, ttk.Separator]] = []
        self.bottom_buttons:  List[ttk.Button] = [ttk.Button(), ttk.Button(), ttk.Button(), ttk.Button()]

        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=10)
        self.columnconfigure(2, weight=10)
        self.columnconfigure(3, weight=10)
        self.columnconfigure(4, weight=10)
        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=10)

        ttk.Label(self, text="Here you can add new passwords or edit old ones. Click 'Save' to save "
                             "changes and 'reset' to revert them.").grid(row=0, column=0, columnspan=5, sticky="nesw")

        ttk.Separator(self).grid(row=1, column=0, columnspan=5, sticky="ew")

        self.tk_passwords_for = []
        self.tk_passwords = []
        self.widget_groups = []

        index = 0
        for index, (en_password_for, en_password) in enumerate(self.container.passwords.items()):
            self.tk_passwords_for.append(tk.StringVar())
            self.tk_passwords_for[index].set(de_encrypting(en_password_for, self.container.key_to_char))
            self.tk_passwords.append(tk.StringVar())
            self.tk_passwords[index].set(de_encrypting(en_password, self.container.key_to_char))

            if self.tk_passwords_for[index].get() == "Program Password":
                password_for_entry = ttk.Entry(self, textvariable=self.tk_passwords_for[index])
                password_for_entry.configure(state="disabled")
                password_for_entry.grid(row=(index * 3) + 2, column=0, columnspan=2, sticky="nesw")
            else:
                password_for_entry = ttk.Entry(self, textvariable=self.tk_passwords_for[index])
                password_for_entry.grid(row=(index * 3) + 2, column=0, columnspan=2, sticky="nesw")
            password_label = ttk.Label(self, text="Password: ")
            password_label.grid(row=(index*3)+2, column=2, sticky="e")
            password_entry = ttk.Entry(self, textvariable=self.tk_passwords[index])
            password_entry.grid(row=(index*3)+2, column=3, columnspan=2, sticky="nesw")
            if self.tk_passwords_for[index].get() == "Program Password":
                delete_button = ttk.Button(self, text="Delete", command=self.delete_command(index))
            else:
                delete_button = ttk.Button(self, text="Delete", command=self.delete_command(index))
                delete_button.grid(row=(index * 3) + 3, column=0, sticky="nesw")
            random_button = ttk.Button(self, text="Random", command=self.random_command(index))
            random_button.grid(row=(index * 3) + 3, column=4, sticky="nesw")

            group_seperator = ttk.Separator(self)
            group_seperator.grid(row=(index*3)+4, column=0, columnspan=5, sticky="ew")

            self.rowconfigure((index * 3) + 2, weight=10)
            self.rowconfigure((index * 3) + 3, weight=10)
            self.rowconfigure((index * 3) + 4, weight=10)

            self.widget_groups.append(
                (password_for_entry, password_label, password_entry, delete_button, random_button, group_seperator))

        newest_row = (index*3)+5
        last_row = newest_row + 1
        self.bottom_buttons = [ttk.Button(), ttk.Button(), ttk.Button(), ttk.Button()]

        add_row = ttk.Button(self, text="New Password", command=self.new_command)
        add_row.grid(row=newest_row, column=0, sticky="nesw")
        self.rowconfigure(newest_row, weight=10)

        back_butt = ttk.Button(self, text="<- Back", command=lambda: self.container.frame_swap("Home"))
        back_butt.grid(row=last_row, column=0, sticky="nesw")

        save_butt = ttk.Button(self, text="Save", command=self.save_command)
        save_butt.grid(row=last_row, column=3, sticky="nesw")

        reset_butt = ttk.Button(self, text="Reset", command=self.reset_command)
        reset_butt.grid(row=last_row, column=4, sticky="nesw")

        self.rowconfigure(newest_row, weight=10)
        self.rowconfigure(last_row, weight=10)

        self.bottom_buttons[0] = add_row
        self.bottom_buttons[1] = back_butt
        self.bottom_buttons[2] = save_butt
        self.bottom_buttons[3] = reset_butt

    def delete_command(self, destroy: int):
        def return_function():
            x = set(self.widget_groups[destroy])
            for index, item in enumerate(self.widget_groups[destroy]):
                item.destroy()
                self.widget_groups[destroy] += (None,)
            y = set(self.widget_groups[destroy])
            self.widget_groups[destroy] = tuple(y - x)
            self.tk_passwords_for[destroy].set("<<__Deleted__>>")
            self.tk_passwords[destroy].set("<<__Deleted__>>")
        return return_function

    def random_command(self, group_place: int):
        def return_function():
            self.tk_passwords[group_place].set(generate_random_password())
        return return_function

    def new_command(self):
        for i in self.bottom_buttons:
            i.destroy()
        index = len(self.widget_groups)
        self.tk_passwords_for.append(tk.StringVar())
        self.tk_passwords_for[index].set("Enter password")
        self.tk_passwords.append(tk.StringVar())
        self.tk_passwords[index].set("Enter password")

        password_for_entry = ttk.Entry(self, textvariable=self.tk_passwords_for[index])
        password_for_entry.grid(row=(index * 3) + 2, column=0, columnspan=2, sticky="nesw")
        password_label = ttk.Label(self, text="Password: ")
        password_label.grid(row=(index*3) + 2, column=2, sticky="e")
        password_entry = ttk.Entry(self, textvariable=self.tk_passwords[index])
        password_entry.grid(row=(index*3) + 2, column=3, columnspan=2, sticky="nesw")

        delete_button = ttk.Button(self, text="Delete", command=self.delete_command(index))
        delete_button.grid(row=(index * 3) + 3, column=0, sticky="nesw")
        random_button = ttk.Button(self, text="Random", command=self.random_command(index))
        random_button.grid(row=(index * 3) + 3, column=4, sticky="nesw")

        group_seperator = ttk.Separator(self)
        group_seperator.grid(row=(index*3) + 4, column=0, columnspan=5, sticky="ew")

        self.rowconfigure((index * 3) + 2, weight=10)
        self.rowconfigure((index * 3) + 3, weight=10)
        self.rowconfigure((index * 3) + 4, weight=10)

        self.widget_groups.append(
            (password_for_entry, password_label, password_entry, delete_button, random_button, group_seperator))
        newest_row = (index*3)+5
        for item in self.widget_groups:
            if not(None in item):
                newest_row += 3
        last_row = newest_row + 1
        add_row = ttk.Button(self, text="New Password", command=self.new_command)
        add_row.grid(row=newest_row, column=0, sticky="nesw")
        self.rowconfigure(newest_row, weight=10)

        back_butt = ttk.Button(self, text="<- Back", command=lambda: self.container.frame_swap("Home"))
        back_butt.grid(row=last_row, column=0, sticky="nesw")

        save_butt = ttk.Button(self, text="Save", command=self.save_command)
        save_butt.grid(row=last_row, column=3, sticky="nesw")

        reset_butt = ttk.Button(self, text="Reset", command=self.reset_command)
        reset_butt.grid(row=last_row, column=4, sticky="nesw")

        self.rowconfigure(newest_row, weight=10)
        self.rowconfigure(last_row, weight=10)
        self.rowconfigure(newest_row - 1, weight=10)

        self.bottom_buttons[0] = add_row
        self.bottom_buttons[1] = back_butt
        self.bottom_buttons[2] = save_butt
        self.bottom_buttons[3] = reset_butt

    def save_command(self):
        self.container.passwords = {}
        for index, password_for in enumerate(self.tk_passwords_for):
            if password_for.get() == "<<__Deleted__>>":
                continue
            else:
                self.container.passwords[encrypting(password_for.get(), self.container.char_to_key)] = \
                    encrypting(self.tk_passwords[index].get(), self.container.char_to_key)
        write_passwords(
            self.container.passwords, self.container.char_to_key, self.container.key_to_char,
            self.container.file_path.get(), self.container.de_encryption_order, self.container.de_encryption_keys)
        self.container.frame_swap("Home")

    def reset_command(self):
        self.container.frame_swap("Passwords")


class ChangeFilePathFrame(ttk.Frame):
    def __init__(self, container: PasswordManager, **kwargs):
        super().__init__(container, **kwargs)
        self.container = container
        self.text_box = tk.StringVar(
            value="Select the folder you want to save your passwords and the name you want to give it")

        top_text = ttk.Label(self, textvariable=self.text_box)
        top_text.grid(columnspan=3, sticky="nesw")
        ttk.Separator(self).grid(row=1, columnspan=3, sticky="ew", pady=5)

        ttk.Label(self, text="Current Path: ").grid(row=2, column=0, sticky="nes")
        ttk.Label(self, text=self.container.file_path.get()).grid(row=2, column=1, columnspan=2, pady=5)

        self.folder_path = tk.StringVar()
        self.file_name = tk.StringVar()

        folder_path_entry = ttk.Entry(self, textvariable=self.folder_path)
        file_name_entry = ttk.Entry(self, textvariable=self.file_name)

        ttk.Label(self, text="New File Name: ").grid(row=3, sticky="nes")
        file_name_entry.grid(row=3, column=1, columnspan=2, sticky='nesw')
        ttk.Label(self, text="Select Folder: ").grid(row=4, sticky="nes")
        folder_path_entry.grid(row=4, column=1, columnspan=2, sticky="nesw")

        select_folder_button = ttk.Button(self, text="Select Folder", command=self.select_folder)
        home_button = ttk.Button(self, text="<- Back", command=lambda: self.container.frame_swap("Home"))
        do_change_button = ttk.Button(self, text="Commit Change", command=self.change_location)

        select_folder_button.grid(row=5, column=2, sticky="nesw", padx=10, pady=10)
        home_button.grid(row=6, column=0, sticky="nesw")
        do_change_button.grid(row=5, column=0, sticky="nesw", pady=10, padx=10)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=5)
        self.rowconfigure(4, weight=5)
        self.rowconfigure(5, weight=5)
        self.rowconfigure(6, weight=5)

    def select_folder(self):
        folder_path = askdirectory()
        self.folder_path.set(folder_path)

    def change_location(self):
        try:
            if self.file_name.get() == "":
                raise FileNotFoundError
            elif len(self.file_name.get()) < 3:
                self.file_name.set(self.file_name.get()[-3:] + '.txt')
            elif self.file_name.get() != "txt":
                self.file_name.set(self.file_name.get() + '.txt')
            new_file_path = self.folder_path.get() + '\\' + self.file_name.get()
            lines_to_write = []
            with open(self.container.file_path.get(), "r") as old_file:
                for line in old_file:
                    lines_to_write.append(line.strip("\n"))
            with open(new_file_path, "w") as other_location:
                for line in lines_to_write:
                    print(line, file=other_location)
            os.remove(self.container.file_path.get())
            self.container.file_path.set(new_file_path)
            ttk.Label(self, text=self.container.file_path.get()).grid(row=2, column=1, columnspan=2, sticky="nesw")
        except FileNotFoundError:
            self.text_box.set("That did not work. Check you are allowed to do this")


class SaveFrame(ttk.Frame):
    def __init__(self, container: PasswordManager, **kwargs):
        super().__init__(container, **kwargs)
        self.container = container

        ttk.Label(self, text="Hit 'Save' to save your changes and close the application") \
            .grid(row=0, column=1, sticky="nesw")
        ttk.Separator(self).grid(row=1, column=0, columnspan=3)

        ttk.Label(self, text="Current File Path: ").grid(row=2, column=0, sticky="nes")
        ttk.Label(self, text=self.container.file_path.get()).grid(row=2, column=1, columnspan=2, sticky="nesw")

        save_changes_button = ttk.Button(self, text="Save", command=self.save_file)
        go_back_button = ttk.Button(self, text="<- Back", command=lambda: self.container.frame_swap("Home"))

        save_changes_button.grid(row=3, column=1)
        go_back_button.grid(row=4, sticky="news")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=5)
        self.rowconfigure(4, weight=5)

    def save_file(self):
        write_passwords(
            self.container.passwords, self.container.char_to_key, self.container.key_to_char,
            self.container.file_path.get(), self.container.de_encryption_order, self.container.de_encryption_keys)
        self.container.destroy()
