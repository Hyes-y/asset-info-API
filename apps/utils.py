import bcrypt

def check_pw(origin, hashed):
    salt = bcrypt.gensalt()
    origin_b = origin.encode('utf-8')
    hashed = hashed.encode('utf-8')

    origin_hashed = bcrypt.hashpw(origin_b, salt)

