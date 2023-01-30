import json
import tkinter
import random
import pyperclip
from tkinter import messagebox


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = letters + symbols + numbers

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, "end")
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    em_us = em_us_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": em_us,
            "password": password
        }
    }
    if website == "" or em_us == "" or password == "":
        tkinter.messagebox.showerror(title="Error", message="You shouldn't leave any empty field.")
    else:
        try:
            with open("passwords.json", mode="r") as pw_file:
                # Read old data
                data = json.load(pw_file)
        except FileNotFoundError:
            with open("passwords.json", mode="w") as pw_file:
                json.dump(new_data, pw_file, indent=4)
        else:
            with open("passwords.json", mode="w") as pw_file:
                # Updating old data with new data
                data.update(new_data)
                # Saving updated data
                json.dump(data, pw_file, indent=4)
        finally:
            website_entry.delete(0, 'end')
            password_entry.delete(0, 'end')


# ---------------------------- SEARCH USERNAME AND PASSWORD ------------------------------- #

def find_password():
    website = website_entry.get()
    try:
        with open("passwords.json", mode="r") as pw_file:
            json_passwords = json.load(pw_file)
    except FileNotFoundError:
        tkinter.messagebox.showwarning(title=website, message="No Data file Found.")
    else:
        try:
            result = json_passwords[website]
            em_us = result["email"]
            password = result["password"]
        except KeyError:
            tkinter.messagebox.showwarning(title="Error", message=f"No details for the {website} exists.")
        else:
            tkinter.messagebox.showinfo(title=website, message=f"Email/Username: {em_us} \nPassword: {password}")


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()

window.config(padx=50, pady=50)
window.title("Password Manager")

canvas = tkinter.Canvas(width=200, height=200)
logo = tkinter.PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# Labels
website_label = tkinter.Label(text="Website:")
em_us_label = tkinter.Label(text="Email/Username:")
password_label = tkinter.Label(text="Password:")
website_label.grid(row=1, column=0)
em_us_label.grid(row=2, column=0)
password_label.grid(row=3, column=0)

# Entries
website_entry = tkinter.Entry(width=33)
website_entry.focus()
em_us_entry = tkinter.Entry(width=52)
em_us_entry.insert(0, "user@gmail.com")
password_entry = tkinter.Entry(width=33)
website_entry.grid(row=1, column=1, columnspan=2, sticky="W")
em_us_entry.grid(row=2, column=1, columnspan=2, sticky="W")
password_entry.grid(row=3, column=1, sticky="W")

# Buttons
search_button = tkinter.Button(text="Search", width=14, command=find_password)
generate_pw_button = tkinter.Button(text="Generate Password", command=generate_password)
add_pw_button = tkinter.Button(text="Add", width=44, command=save)
search_button.grid(row=1, column=2, sticky="W")
generate_pw_button.grid(row=3, column=2, sticky="W")
add_pw_button.grid(row=4, column=1, columnspan=2, sticky="W")

window.mainloop()
