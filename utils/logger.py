import datetime

def log_event(user, action, filename):
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {user} - {action} - {filename}\n")