from immutable_events import ImmutableEvent
from schedule import Schedule
from meals import Meals
from tasks import Task
from sleep import Sleep
import copy


class CalculateSchedule:
    def __init__(self, events:list[ImmutableEvent], tasks:list[Task], meals:list[Meals], sleep:list): # sleep list is wd_wakeup_time, wd_sleep_time, we_wakeup_time, we_sleep_time
        self.events = events
        self.tasks = tasks
        self.meals = meals
        self.schedule = Schedule()
        self.week = self.schedule.week
        self.sleep = sleep
    

    def create_schedule(self):
        self.add_sleep()
        for event in self.events:
            self.add_immutable_events(event)
        self.add_meals()
    

    def add_immutable_events(self, event):
        start_box = self.time_to_box_number(event.start_time)
        end_box = self.time_to_box_number(event.end_time)
        print("start box is " + str(start_box))
        print("end box is " + str(end_box))
        for box in range(start_box, end_box):
            self.week[event.day_of_week][box] = event
            

    def add_sleep(self):
        for i in range(5):
            new_event1 = Sleep(i, 0000, self.sleep.wd_wakeup_time)
            new_event2 = Sleep(i, self.sleep.wd_sleep_time, 1440)
            self.add_immutable_events(new_event1)
            self.add_immutable_events(new_event2)
        for i in range(5, 7):
            new_event1 = Sleep(i, 0000, self.sleep.we_wakeup_time)
            new_event2 = Sleep(i, self.sleep.we_sleep_time, 1440)
            self.add_immutable_events(new_event1)
            self.add_immutable_events(new_event2)

        
    def add_meals(self):
        for meal in self.meals:
        # calculate what slots in self.week each meal should go in
            meal_start = self.time_to_box_number(meal.start_time)
            meal_end = self.time_to_box_number(meal.end_time) - 1
            # add each meal into self.week
            for day_index in range(len(self.week)):
                for i in range(0, meal_end - meal_start + 1):
                    m = copy.deepcopy(meal)
                    m.day_of_week = day_index
                    self.week[day_index][meal_start + i] = m

    
    def add_tasks(self):
        # create separate lists for tasks that have a deadline and tasks that don't have a deadline
        tasks_with_deadline = []
        tasks_without_deadline = []
        for t in self.tasks:
            if t.day_of_week:
                tasks_with_deadline.append(t)
            else:
                tasks_without_deadline.append(t)
        # sort tasks_with_deadline by the deadline date
        for i in range(len(tasks_with_deadline)):
            earliest_deadline = i
            for t in range(i + 1, len(tasks_with_deadline)):
                if tasks_with_deadline[t].day_of_week < tasks_with_deadline[earliest_deadline].day_of_week:
                    earliest_deadline = t
            second_deadline = tasks_with_deadline[i]
            tasks_with_deadline[i] = tasks_with_deadline[earliest_deadline]
            tasks_with_deadline[earliest_deadline] = second_deadline
        # input the task into the weekly schedule based on deadline
        for t in range(len(tasks_with_deadline)):
            num_boxes = self.time_to_box_number(tasks_with_deadline[t].time_needed)
            for d in range(len(self.week)):
                for time in range(len(self.week[d])):
                    if self.week[d][time] == None:
                        initial_time = time
                        time += 1
                        num_boxes -= 1
                        while(num_boxes != 0):
                            if self.week[d][time] == None:
                                time += 1
                                num_boxes -= 1
                            else:
                                break
                    for j in range(initial_time, time + 1):
                        pass
            

    def time_to_box_number(self, time):
        return int(time / 30)
    
    def output(self):
        answer_list = []
        for day in self.weeks:
            for time in day:
                if time:
                    answer_list.append(time)
        index = 1
        while(index < len(answer_list)):
            if answer_list[index].name == answer_list[index-1].name:
                answer_list.pop(index)
            else:
                index += 1
        return answer_list


# events = [ImmutableEvent(0, 900, 1000, "work"), ImmutableEvent(5, 1250, 1300, "work again")]
# sleep = Sleep(540, 1320, 420, 1320)
# meals = [Meals(570, 600, "Breakfast"), Meals(780, 840, "Lunch"), Meals(1200, 1230, "Dinner")]    


# test_schedule = CalculateSchedule(events, None, meals, sleep)
# test_schedule.create_schedule()
# print(str(test_schedule.schedule))
