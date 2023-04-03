from getpass import getpass

from utils.dbConnection import Cursor
from utils.password import checkPasswordLimitation, getHashedPassword


def login():
    # ask for username and password
    user_data = input("Please enter your username: ")
    password = getpass("Please enter your password: ")

    # hash password
    password = getHashedPassword(password)

    with Cursor() as cursor:
        # check if username and password are correct
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user_data, password))
        user = cursor.fetchone()

        # check if user with given username and password exists
        if user:
            # print out success message
            print("Login successfully")
            # return success
            return "Login successfully"
        else:
            # raise exception if user doesn't exist
            raise Exception("Invalid username or password")

def register():
    # ask for username and password
    wish_name = input("Please enter your username: ")
    password = getpass("Please enter your password: ")
    security_password = getpass("Please enter your password again: ")
    
    if not checkPasswordLimitation(password):
        # raise exception if password doesn't match the requirements
        raise Exception("Password doesn't match the requirements")

    # hash password and security password
    password = getHashedPassword(password)
    security_password = getHashedPassword(security_password)

    # check if passwords match
    if password != security_password:
        # raise exception if passwords don't match
        raise Exception("Passwords don't match")
    
    elif len(wish_name) < 3:
        # raise exception if username is shorter than 3 characters
        raise Exception("Username is too short")
    
    else:
        # check if username is already taken
        with Cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (wish_name,))
            user = cursor.fetchone()
            
            # check if username is already taken
            if user:
                # raise exception if username is already taken
                raise Exception("Username already taken")
            
            else:
                # insert user into database
                cursor.execute("INSERT INTO users (username, password, permission) VALUES (%s, %s, %s)", (wish_name, password, 0))
                
                print("User successfully registered")
                # return True if user was successfully inserted
                return "User successfully registered"

def logout():
    pass

def getUserById(id: int):
    # get user by id
    with Cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()

        # check if user exists
        if user:
            # return user value
            return user
        else:
            # raise exception if user doesn't exist
            raise Exception("User not found")

def getUserByUsername(username: str):
    # get user by username
    with Cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        # check if user exists
        if user:
            # return user value
            return user
        else:
            # raise exception if user doesn't exist
            raise Exception("User not found")

def changePermission(user: str, permission: int):
    # check if user exists
    if user:
        # check if user is string or int
        if user.isalpha():
            # get user by username
            userData = getUserByUsername(user)

            if userData:
                with Cursor() as cursor:
                    # update permission
                    cursor.execute("UPDATE users SET permission = %s WHERE username = %s", (permission, userData['username']))
                    
                    print(f"Permission successfully updated to {permission}")
                    # return True if permission was successfully updated
                    return f"Permission successfully updated to {permission}"
            else:
                # raise exception if user doesn't exist
                raise Exception("Username not found")



        elif user.isdigit():
            user = int(user)
            # get user by id
            userData = getUserById(user)

            if userData:
                with Cursor() as cursor:
                    # update permission
                    cursor.execute("UPDATE users SET permission = %s WHERE id = %s", (permission, userData['id']))

                    print(f"Permission successfully updated to {permission}")
                    # return True if permission was successfully updated
                    return f"Permission successfully updated to {permission}"
            else:
                # raise exception if user doesn't exist
                raise Exception("User id not found")
