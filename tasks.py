class Task:
    def __init__ (self, length, name, deadline=None, commute=0):
        # total time needed to complete the task
        self.time_needed = length
        # day and time the task must be completed by
        self.deadline = deadline
        # day the task will be completed
        self.day_of_week = None
        # name of task that summarizes what must be done
        self.name = name
        # travel time if the task must be completed outside of home
        self.commute = commute
        # add a start and end time to use to input into the calender
        self.start_time = 0
        self.end_time = 0