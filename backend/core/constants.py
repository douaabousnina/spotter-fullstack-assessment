WAYPOINT_TYPE_CHOICES = [
        ('current', 'Current Location'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff'),
        ('fuel', 'Fuel Stop'),
        ('rest', 'Rest Stop'),
]

DUTY_STATUS_CHOICES = [
        ('off_duty', 'Off Duty'),
        ('sleeper_berth', 'Sleeper Berth'),
        ('driving', 'Driving'),
        ('on_duty', 'On Duty'),
        ('rest', 'Rest'),
]

# HOS regulations
MAX_DRIVING_TIME_CYCLE = 70           # 70h
MAX_DRIVING_HOURS = 11                # 10h
MAX_DUTY_WINDOW_HOURS = 14            # 14h

MAX_FUEL_RANGE_MILES = 1000 

FUEL_STOP_TIME = 0.5                  # 30mn
PICKUP_DROPOFF_TIME = 1               # 1h
REQUIRED_BREAK_HOURS = 10             # 10h


