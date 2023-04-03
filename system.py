from utils.dbConnection import prepare
from utils.account import login, register, getUserById, getUserByUsername, changePermission

def run():
    print("Welcome to the Login System! (v1.0.0)")

    # print out checking database
    print("Checking database...")
    prepare()

    print("Login System is running...")

    while True:
        # print out the menu
        # options are: login, register, get users, change perms, exit
        print("1: Login\n2: Register\n3: Get Users\n4: Change User Permissions\n5: Exit")

        # ask for user input
        user_input: str = input("Please enter your choice: ")

        # check if user input is a number
        if user_input.isnumeric():
            # convert user input to int
            user_input = int(user_input)

            # check if user input is 1
            if user_input == 1:
                # call login function
                login()

            # check if user input is 2
            elif user_input == 2:
                # call register function
                register()

            # check if user input is 3
            elif user_input == 3:
                # ask for user id or username
                user_id_or_username = input("Please enter the user id or username: ")

                # check if user id or username is a number
                if user_id_or_username.isnumeric():
                    # convert user id or username to int
                    user_id_or_username = int(user_id_or_username)

                    # get user by id
                    user = getUserById(user_id_or_username)

                    # print out user
                    print(user)
                
                else:
                    # get user by username
                    user = getUserByUsername(user_id_or_username)

                    # print out user
                    print(user)

            # check if user input is 4
            elif user_input == 4:
                # ask for user id or username
                user_id_or_username = input("Please enter the user id or username: ")

                # ask what kind of permission the user should have
                # 0 = normal user
                # 1 = admin
                # 2 = super admin
                # 3 = owner

                permission: int = input("Please enter the permission: ")

                changePermission(user_id_or_username, permission)

            # check if user input is 5
            elif user_input == 5:
                # exit program
                exit()

            # check if user input is not 1, 2, 3, 4 or 5
            else:
                # raise exception
                raise Exception("Invalid input")
        
run()