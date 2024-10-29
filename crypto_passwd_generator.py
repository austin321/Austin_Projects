import string
import secrets

def password_generator(password_length):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for i in range(password_length))
    return password

def passwd():
    password_length = int(input("What do you want your password length to be? "))
    print("Password generated: ", password_generator(password_length))

passwd()