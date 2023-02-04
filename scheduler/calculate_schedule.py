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
        self.add_sleep()
        for event in self.events:
            self.add_immutable_events(event)
        self.add_meals()
    
    def add_immutable_events(self, event:ImmutableEvent):
        start_box = self.time_to_box_number(event.start_time)
        end_box = self.time_to_box_number(event.end_time)
        
        for box in range(start_box, end_box):
            self.schedule[ImmutableEvent.day_of_week][box] = event
            

    def add_sleep(self):
        sleep_times = self.sleep.return_sleep_events()
        for sleep_event in sleep_times:
            self.add_immutable_events(sleep_event)
            
    
       
        
        # for day in range(0, 7):
        #     start_box = self.time_to_box_number(sleep_times[day].start_time)
        #     end_box = self.time_to_box_number(sleep_times[day].end_time)
        #     for i in range(start_box, 24 - start_box):
        #         self.schedule[day][start_box + i] = "Sleep"
        
    def add_meals(self):
        # calculate what slots in self.schedule each meal should go in
        breakfast_start = self.time_to_box_number(self.meals.b_start)
        breakfast_end = self.time_to_box_number(self.meals.b_end) - 1
        lunch_start = self.time_to_box_number(self.meals.l_start)
        lunch_end = self.time_to_box_number(self.meals.l_end) - 1
        dinner_start = self.time_to_box_number(self.meals.d_start)
        dinner_end = self.time_to_box_number(self.meals.d_end) - 1
        # add each meal into self.schedule
        for day in self.schedule:
            for i in range(0, breakfast_end - breakfast_start + 1):
                self.schedule[breakfast_start + i] = "Breakfast"
            for i in range(0, lunch_end - lunch_start + 1):
                self.schedule[lunch_start + i] = "Lunch"
            for i in range(0, dinner_end - dinner_start + 1):
                self.schedule[dinner_start + i] = "Dinner"
    
    def add_tasks():
        pass

    def time_to_box_number(self, time):
        hours = time[0:2]
        hours = hours * 2
        minutes = time[2:4]
        minutes = minutes / 30
        return hours + minutes


events = []
sleep = Sleep()    


test_schedule = CalculateSchedule()
test_schedule.create_schedule()
print(test_schedule.schedule)
