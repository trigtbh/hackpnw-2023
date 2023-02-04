class Deadline:
    def __init__ (self, day_of_week, time):
        # store both the day and the time that a task must be completed by
        self.day_of_week = day_of_week
        self.time = time