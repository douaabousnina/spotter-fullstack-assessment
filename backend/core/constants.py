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
MAX_DRIVING_HOURS = 11
MAX_DUTY_WINDOW_HOURS = 14
REQUIRED_BREAK_HOURS = 10

MAX_FUEL_RANGE_MILES = 1000 

FUEL_STOP_TIME = 30 * 60              # 30mn
PICKUP_DROPOFF_TIME = 1 * 60           # 1h


