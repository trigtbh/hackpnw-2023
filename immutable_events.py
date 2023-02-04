# any event that will partake during the week which start time and end time cannot be changed
# this creates an immutable block in the schedule
# ex. school, a class, sports practice, meeting
class ImmutableEvent:
    def __init__(self, day_of_week, start_time, end_time, name, commute_time = 0 ) -> None:
        self.day_of_week = day_of_week # represents day of week event will take place
        # day_of_week key: 0 = Mon, 1 = Tues, 2 = Wed ... 
        self.start_time = start_time # start time of the event
        # times will be stored as a four-digit number, in which first two represent the hour (with military time), second two represent the minute
        self.end_time = end_time # end time of the event
        self.name = name # name of the event
        self.commute_time = commute_time # time taken from original destination to event (only represents one-way commute time)
        # commute time in minutes
        self.mutuable = False