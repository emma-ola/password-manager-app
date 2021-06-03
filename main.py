from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 12))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)
    password_input.delete(first=0, last=END)
    password_input.insert(index=0, string=password)
    pyperclip.copy(text=password)


def save_to_file():
    website = website_input.get()
    email = email_input.get()
    password_text = password_input.get()
    new_data = {
        website: {
            'email': email,
            'password': password_text,
        }
    }

    if len(website) == 0 or len(password_text) == 0:
        messagebox.showinfo(title='Oops', message="Please Don't leave any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f'These are the details Entered: \nEmail/Username: {email}'
                                                              f'\nPassword: {password_text}\nAre You Happy With This?')
        if is_ok:
            try:
                with open(file='password-data.json', mode='r') as data_file:
                    data = json.load(fp=data_file)
            except FileNotFoundError:
                with open(file='password-data.json', mode='w') as data_file:
                    json.dump(obj=new_data, fp=data_file, indent=4)
            else:
                data.update(new_data)
                with open(file='password-data.json', mode='w') as data_file:
                    json.dump(obj=data, fp=data_file, indent=4)
            finally:
                website_input.delete(first=0, last=END)
                password_input.delete(first=0, last=END)


def find_password():
    website = website_input.get()
    try:
        with open('password-data.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title='Error', message='No Data File Found.')
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f'Email/Username: {email}\nPassword: {password}')
        else:
            messagebox.showinfo(title='Error', message=f'No Website Matching {website}. Website name is Case Sensitive')


window = Tk()
window.title('Password Manager App')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
password_logo = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=password_logo)
canvas.grid(row=0, column=1)

# labels
website_label = Label(text='Website:')
website_label.grid(row=1, column=0)
email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0)
password_label = Label(text='Password:')
password_label.grid(row=3, column=0)

# Entries
website_input = Entry(width=23)
website_input.focus()
website_input.grid(row=1, column=1)
email_input = Entry(width=39)
email_input.insert(index=0, string='iam_newton@outlook.com')
email_input.grid(row=2, column=1, columnspan=2)
password_input = Entry(width=23)
password_input.grid(row=3, column=1)

# Buttons
generate_password_button = Button(text='Generate Password', command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text='Add', width=39, command=save_to_file)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text='Search', width=15, command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()
