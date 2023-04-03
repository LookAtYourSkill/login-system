import hashlib
import string


def getHashedPassword(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def checkPassword(password: str, hashedPassword: str):
    return getHashedPassword(password) == hashedPassword


def checkPasswordLimitation(password):
    # check if password is longer than 8 characters
    if len(password) < 8:
        # raise exception if password is shorter than 8 characters
        raise Exception("Password is too short")
    
    # check if password has any uppercase letters
    if not any(char in string.ascii_uppercase for char in password):
        # raise exception if password has no uppercase letters
        raise Exception("Password has no uppercase characters")
    
    # check if password has any lowercase letters
    if not any(char in string.ascii_lowercase for char in password):
        # raise exception if password has no lowercase letters
        raise Exception("Password has no lowercase characters")
    
    # check if password has any numbers
    if not any(char in string.digits for char in password):
        # raise exception if password has no numbers
        raise Exception("Password has no numbers")
    
    # check if password has any special characters
    if not any(char in string.punctuation for char in password):
        # raise exception if password has no special characters
        raise Exception("Password has no special characters")
    
    else:
        # return True if password is valid
        return True
