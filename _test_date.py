from datetime import date, datetime
import time


now = time.localtime()
print(f"time.localtime() = {now}")

now = date.today()
print(f"date.today() = {now}")

now1 = date.isoformat(now)
print(f"date.isoformat(now) = {now1}")

date_time = datetime(2022, 10, 27, 11, 30, 0, 0)
print(f"datetime(2022, 10, 27, 11, 30, 0, 0) = {date_time}")

ts = time.time()
print(f"time.time() = {ts}")

date_time_iso = datetime.fromtimestamp(ts).isoformat()
print(f"datetime.fromtimestamp(ts).isoformat() = {date_time_iso}")

date_obj = datetime.fromisoformat(date_time_iso)
print(f"date.fromisoformat(date_time_iso) = {type(date_obj)}")

print(f"{date_obj.day}/{date_obj.month}/{date_obj.year}")
print(f"{date_obj.hour}:{date_obj.minute}")
