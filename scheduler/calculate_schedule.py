from immutable_events import ImmutableEvent
from schedule import Schedule
from deadline import Deadline
from meals import Meals
from tasks import Task
from sleep import Sleep


class CalculateSchedule:
    def __init__(self, events:list[ImmutableEvent], tasks:list[Task], meals:Meals, sleep:Sleep):
        self.events = events
        self.tasks = tasks
        self.meals = meals
        self.schedule = Schedule()
        self.sleep = sleep
    
    def create_schedule(self):
        pass

    def sleep(self):
        sleep_times = self.sleep.return_sleep_events()
        for day in range(0, 7):
            start_box = self.time_to_box_number(sleep_times[day].start_time)
            end_box = self.time_to_box_number(sleep_times[day].end_time)
            for i in range(end_box - start_box):
                self.schedule[day][start_box + i] = "Sleep"

    def time_to_box_number(self, time):
        hours = time[0:2]
        hours = hours * 2
        minutes = time[2:4]
        minutes = minutes / 30
        return hours + minutes


    