import bcrypt


def get_hashed_password(password):
    return bcrypt.hashpw(password, salt=bcrypt.gensalt())


def check_password(password, hashed_password):
    return bcrypt.checkpw(password, hashed_password)


def check_password_per_limitation(password):
    pass
