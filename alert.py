class Alert:
    def __init__(self, event, place):
        # the event that doesn't have a break either before or after it
        self.event = event
        # -1 represents no break before the event while 1 represents no break after the event
        self.place = place