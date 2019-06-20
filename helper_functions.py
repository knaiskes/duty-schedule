# Basic encryption method of admin's password
# It is not super secure but it is good enough for our case
def encrypt_password(encrypt):
    import hashlib
    password = hashlib.sha256()
    password = hashlib.sha256(encrypt.encode("utf8")).hexdigest()
    return password
