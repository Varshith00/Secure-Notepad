import os
import sys
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import json

class AuthenticationWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("Login - Notepad")

        self.accounts_file = "store3.json"
        self.accounts_created = False

        if not os.path.exists(self.accounts_file):
            self.create_account()
        else:
            self.login_interface()

    def create_account(self):
        if not self.accounts_created:
            self.username_label = Label(self.root, text="Create Username:")
            self.username_label.pack()

            self.username_entry = Entry(self.root)
            self.username_entry.pack()

            self.password_label = Label(self.root, text="Create Password:")
            self.password_label.pack()

            self.password_entry = Entry(self.root, show="*")
            self.password_entry.pack()

            self.create_button = Button(self.root, text="Create Account", command=self.save_account)
            self.create_button.pack()
        else:
            self.login_interface()

    def save_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        accounts = {username: password}

        with open(self.accounts_file, "w") as file:
            json.dump(accounts, file)

        self.accounts_created = True
        showinfo("Account Created", "Your account has been created successfully.")
        self.root.destroy()
        notepad = Notepad(width=600, height=400)
        notepad.run()

    def login_interface(self):
        self.username_label = Label(self.root, text="Username:")
        self.username_label.pack()

        self.username_entry = Entry(self.root)
        self.username_entry.pack()

        self.password_label = Label(self.root, text="Password:")
        self.password_label.pack()

        self.password_entry = Entry(self.root, show="*")
        self.password_entry.pack()

        self.login_button = Button(self.root, text="Login", command=self.authenticate)
        self.login_button.pack()

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        accounts = {}

        with open(self.accounts_file, "r") as file:
            accounts = json.load(file)

        if username in accounts and accounts[username] == password:
            self.root.destroy()
            notepad = Notepad(width=600, height=400)
            notepad.run()
        else:
            showerror("Authentication Failed", "Invalid username or password.")

class Notepad:

    def __init__(self, **kwargs):
        self.__root = Tk()

        self.__thisWidth = 300
        self.__thisHeight = 300
        self.__thisTextArea = Text(self.__root)
        self.__thisMenuBar = Menu(self.__root)
        self.__thisFileMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__thisEditMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__thisHelpMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__thisScrollBar = Scrollbar(self.__thisTextArea)
        self.__file = None

        try:
            self.__root.wm_iconbitmap("Notepad.ico")
        except:
            pass

        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        self.__root.title("Untitled - Notepad")

        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        left = (screenWidth / 2) - (self.__thisWidth / 2)
        top = (screenHeight / 2) - (self.__thisHeight / 2)

        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth,
                                              self.__thisHeight,
                                              left, top))

        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        self.__thisTextArea.grid(sticky=N + E + S + W)

        self.__thisFileMenu.add_command(label="New", command=self.__newFile)
        self.__thisFileMenu.add_command(label="Open", command=self.__openFile)
        self.__thisFileMenu.add_command(label="Save", command=self.__saveFile)
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit", command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)

        self.__thisEditMenu.add_command(label="Cut", command=self.__cut)
        self.__thisEditMenu.add_command(label="Copy", command=self.__copy)
        self.__thisEditMenu.add_command(label="Paste", command=self.__paste)
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)

        self.__thisHelpMenu.add_command(label="About Notepad", command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help", menu=self.__thisHelpMenu)

        self.__root.config(menu=self.__thisMenuBar)

        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __quitApplication(self):
        self.__root.destroy()

    def __showAbout(self):
        showinfo("Notepad", "Mrinal Verma")

    def __encrypt(self, text, key):
        encrypted_text = ""
        for char in text:
            if char.isalpha():
                ascii_offset = ord('a') if char.islower() else ord('A')
                encrypted_char = chr((ord(char) - ascii_offset + key) % 26 + ascii_offset)
                encrypted_text += encrypted_char
            else:
                encrypted_text += char
        return encrypted_text

    def __decrypt(self, encrypted_text, key):
        decrypted_text = ""
        for char in encrypted_text:
            if char.isalpha():
                ascii_offset = ord('a') if char.islower() else ord('A')
                decrypted_char = chr((ord(char) - ascii_offset - key) % 26 + ascii_offset)
                decrypted_text += decrypted_char
            else:
                decrypted_text += char
        return decrypted_text

    def __saveFile(self):
        if self.__file is None:
            self.__file = asksaveasfilename(initialfile='Untitled.notepad',
                                            defaultextension=".notepad",
                                            filetypes=[("Notepad Files", "*.notepad")])

            if self.__file == "":
                self.__file = None
            else:
                # Encrypt the text
                encrypted_text = self.__encrypt(self.__thisTextArea.get(1.0, END), 3)  # Use a key (shift) value of your choice

                # Save the encrypted text to the file
                with open(self.__file, "w") as file:
                    file.write(encrypted_text)

                self.__root.title(os.path.basename(self.__file) + " - Notepad")

                # Change the file association to open your application
                os.system(f'assoc .notepad=NotepadFile')
                os.system(f'ftype NotepadFile="{sys.executable}" "{os.path.abspath(__file__)}" "%1"')

    def __openFile(self):
        self.__file = askopenfilename(defaultextension=".notepad",
                                      filetypes=[("Notepad Files", "*.notepad")])

        if self.__file == "":
            self.__file = None
        else:
            self.__root.title(os.path.basename(self.__file) + " - Notepad")

            # Read the encrypted text from the file
            with open(self.__file, "r") as file:
                encrypted_text = file.read()

            decrypted_text = self.__decrypt(encrypted_text, 3)  # Use the same key value
            self.__thisTextArea.insert(1.0, decrypted_text)

    def __newFile(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)
    
    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def run(self):
        self.__root.mainloop()

# Create an instance of the authentication window and run it
root = Tk()
auth_window = AuthenticationWindow(root)
root.mainloop()
