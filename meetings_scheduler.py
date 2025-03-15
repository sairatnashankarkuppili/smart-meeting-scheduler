from datetime import datetime

class SmartMeetingScheduler:
    def __init__(self):
        self.working_hours = (10, 22)
        self.holidays = {"2025-01-01", "2025-12-25"}
        self.meetings = {}

    def is_working_day(self, date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return date_str not in self.holidays and date.weekday() < 5

    def schedule_meeting(self, user, date_str, start, end):
        if not self.is_working_day(date_str) or not (self.working_hours[0] <= start < end <= self.working_hours[1]):
            return "Meetings can't be scheduled on public holidays and weekends."

        start_time, end_time = datetime.strptime(f"{date_str} {start}:00", "%Y-%m-%d %H:%M"), datetime.strptime(f"{date_str} {end}:00", "%Y-%m-%d %H:%M")
        self.meetings.setdefault(user, [])

        if any(not (end_time <= m[0] or start_time >= m[1]) for m in self.meetings[user]):
            return "Meeting overlaps with an existing one."

        self.meetings[user].append((start_time, end_time))
        return "Meeting scheduled successfully."

    def check_slots(self, user, date_str):
        if not self.is_working_day(date_str):
            return "No slots available on weekends or holidays."

        slots, current = [], datetime.strptime(f"{date_str} {self.working_hours[0]}:00", "%Y-%m-%d %H:%M")
        meetings = sorted(self.meetings.get(user, [])) + [(datetime.strptime(f"{date_str} {self.working_hours[1]}:00", "%Y-%m-%d %H:%M"), None)]

        for start, end in meetings:
            if current < start:
                slots.append((current.strftime('%H:%M'), start.strftime('%H:%M')))
            current = end or start
        return slots or "No free slots available."

scheduler = SmartMeetingScheduler()
user = input("Enter your name: ")

while True:
    choice = input("\n1. Schedule Meeting\n2. Check Available Slots\n3. Exit\nChoose an option: ")

    if choice == "1":
        date, start, end = input("Enter Date (YYYY-MM-DD): "), int(input("Start Hour (24h format): ")), int(input("End Hour (24h format): "))
        print(scheduler.schedule_meeting(user, date, start, end))

    elif choice == "2":
        date = input("Enter Date (YYYY-MM-DD): ")
        print("Available slots:", scheduler.check_slots(user, date))

    elif choice == "3":
        print("Exiting scheduler.")
        break

    else:
        print("Invalid choice. Try again.")
