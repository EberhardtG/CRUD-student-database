from datetime import datetime
import time


def log_activity(message: str):
    with open("activity_log.txt", "a") as f:
        f.write(
            f"{datetime.now()} - {message}\n"
        )


def send_notification(message: str):
    time.sleep(2)

    with open("notification_log.txt", "a") as f:
        f.write(
            f"{datetime.now()} - {message}\n"
        )