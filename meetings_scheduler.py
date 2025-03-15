# Application

from datetime import datetime, timedelta
import calendar

class SmartMeetingScheduler:
    def __init__(self):
        self.working_hours = (9, 17)  
        self.public_holidays = {"2025-01-01", "2025-12-25"}  
        self.meetings = {}  
    
    def is_working_day(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        return date_str not in self.public_holidays and date_obj.weekday() < 5
    
    def schedule_meeting(self, user, date_str, start_hour, end_hour):
        if not self.is_working_day(date_str):
            return "Cannot schedule on weekends or public holidays."
        if not (self.working_hours[0] <= start_hour < end_hour <= self.working_hours[1]):
            return "Meeting time out of working hours."
        
        start_time = datetime.strptime(f"{date_str} {start_hour}:00", "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(f"{date_str} {end_hour}:00", "%Y-%m-%d %H:%M")
        
        if user not in self.meetings:
            self.meetings[user] = []
        
        for meeting in self.meetings[user]:
            if not (end_time <= meeting[0] or start_time >= meeting[1]):
                return "Meeting overlaps with an existing one."
        
        self.meetings[user].append((start_time, end_time))
        self.meetings[user].sort()
        return "Meeting scheduled successfully."
    
    def check_available_slots(self, user, date_str):
        if not self.is_working_day(date_str):
            return "No available slots on weekends or public holidays."
        
        start_of_day = datetime.strptime(f"{date_str} {self.working_hours[0]}:00", "%Y-%m-%d %H:%M")
        end_of_day = datetime.strptime(f"{date_str} {self.working_hours[1]}:00", "%Y-%m-%d %H:%M")
        
        booked_slots = self.meetings.get(user, [])
        free_slots = []
        
        current_time = start_of_day
        for meeting in booked_slots:
            if current_time < meeting[0]:
                free_slots.append((current_time, meeting[0]))
            current_time = meeting[1]
        
        if current_time < end_of_day:
            free_slots.append((current_time, end_of_day))
        
        return [(slot[0].strftime('%H:%M'), slot[1].strftime('%H:%M')) for slot in free_slots]
    
    def view_meetings(self, user):
        if user not in self.meetings or not self.meetings[user]:
            return "No upcoming meetings."
        
        return [(m[0].strftime('%Y-%m-%d %H:%M'), m[1].strftime('%H:%M')) for m in self.meetings[user]]

scheduler = SmartMeetingScheduler()
print(scheduler.schedule_meeting("Alice", "2025-03-18", 10, 11))
print(scheduler.check_available_slots("Alice", "2025-03-18"))
print(scheduler.view_meetings("Alice"))