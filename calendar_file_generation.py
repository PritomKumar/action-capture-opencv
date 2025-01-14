from ics import Calendar, Event
from datetime import datetime, timedelta

# Define your routine data, excluding the Sleep event
routine = [
    ("6:30-7:00", "Wake up", ""),
    ("7:00-8:00", "Arrive in Kumpula Unisport", "Talk with parents."),
    ("8:00-9:30", "Gym", "Strength training, listening to audiobooks"),
    ("9:30-11:00", "Morning Work", "Check Emails, Set today’s agenda, and finish some work."),
    ("11:00-12:30", "Lunch", ""),
    ("12:30-15:00", "After Lunch Work", "Doing main work for the day."),
    ("15:00-15:30", "Break", "Rest, walk around, have some coffee or hot chocolate"),
    ("15:30-18:00", "Evening work", "Finish what I was doing."),
    ("18:00-19:00", "Gym", "Cardio"),
    ("19:00-20:00", "Return home", "Listen to Audiobooks, call friends."),
    ("20:00-21:00", "Before Sleep activities", "Using Reddit, Language Learning with Duolingo, manga, etc."),
    ("21:00-22:00", "Brush teeth, going to bed", ""),
]

# Create a calendar object
calendar = Calendar()

# Starting date (example: January 15, 2025, starting at 6:30 AM)
start_date = datetime(2025, 1, 15, 6, 30)

# Convert routine to events and add them to the calendar
for time_range, activity, notes in routine:
    start_time_str, end_time_str = time_range.split('-')
    
    # Parse start and end times
    start_hour, start_minute = map(int, start_time_str.split(':'))
    end_hour, end_minute = map(int, end_time_str.split(':'))
    
    # Create datetime objects for start time
    event_start = start_date.replace(hour=start_hour, minute=start_minute)
    
    # Adjust for end time if it's after midnight (e.g., 22:00-6:30)
    if end_hour < start_hour or (end_hour == start_hour and end_minute < start_minute):
        event_end = start_date.replace(hour=end_hour, minute=end_minute) + timedelta(days=1)  # Move to the next day
    else:
        event_end = start_date.replace(hour=end_hour, minute=end_minute)

    # Create an event
    event = Event(
        name=activity,
        begin=event_start,
        end=event_end,
        description=notes,
    )
    
    # Add event to calendar
    calendar.events.add(event)
    
# Save the calendar to a file
with open("daily_routine_one_day.ics", "w") as f:
    f.writelines(calendar)

print("ICS file for one day created successfully!")
