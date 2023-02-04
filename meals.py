class Meals:
    def __init__(self, start, end, name):
        # the following variables contain the start and end time for a meal
        # since meals should be taken at the same time every day for health reasons, only 1 start and end time for each meal is needed
        self.start_time = start
        self.end_time = end
        self.name = name
        self.day_of_week = None
