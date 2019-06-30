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

def generateDuties(users_list):
    from itertools import cycle
    from datetime import datetime
    from datetime import timedelta

    days_list = []
    start = calculateDateQuery("today")
    end = calculateDateQuery("week")
    step = timedelta(days=1)

    while start <= end:
        days_list.append(start)
        start += step

    duties_list = list(zip(users_list, cycle(days_list)) if len(users_list) > len(days_list) else zip(cycle(users_list), days_list))

    return duties_list

