class Task:
    def __init__ (self, length, name, day_of_week=None, commute=0):
        # total time needed to complete the task
        self.time_needed = length
        # day and time the task must be completed by
        self.day_of_week = day_of_week
        # name of task that summarizes what must be done
        self.task_name = name
        # travel time if the task must be completed outside of home
        self.commute = commute
        # add a start and end time to use to input into the calender
        self.start_time = 0
        self.end_time = 0