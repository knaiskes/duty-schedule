# Basic encryption method of admin's password
# It is not super secure but it is good enough for our case
def encrypt_password(encrypt):
    import hashlib
    password = hashlib.sha256()
    password = hashlib.sha256(encrypt.encode("utf8")).hexdigest()
    return password

def calculateDateQuery(option):
    from datetime import timedelta
    from  datetime import date

    available_options = {
            "today": date.today(),
            "tomorrow": date.today() + timedelta(days=1),
            "week": date.today() + timedelta(days=7),
            "month": 30,
    }
    return available_options[option]

