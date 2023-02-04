class Task:
    def __init__ (self, length, deadline, name, commute=0):
        # total time needed to complete the task
        self.time_needed = length
        # day and time the task must be completed by
        self.deadline = deadline
        # name of task that summarizes what must be done
        self.task_name = name
        # travel time if the task must be completed outside of home
        self.commute = commute