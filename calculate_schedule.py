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
        self.alerts = []
    

    def create_schedule(self):
        self.add_sleep()
        self.add_meals()
        for event in self.events:
            self.add_immutable_events(event)
        
        self.add_tasks()
    

    def add_immutable_events(self, event):
        if not(event in self.week):
            start_box = self.time_to_box_number(event.start_time, True)
            end_box = self.time_to_box_number(event.end_time) 
            # print("start box is " + str(start_box))
            # print("end box is " + str(end_box))
            if(type(event)!= Sleep):
                starting_break_box = self.time_to_box_number(event.start_time - 10, True)
                if(starting_break_box != start_box):
                    if(self.week[event.day_of_week][starting_break_box] == None):
                        self.week[event.day_of_week][starting_break_box] = "Break"
                    else:
                        if not(event in self.alerts):
                            self.alerts.append(event)
                
                ending_break_box = self.time_to_box_number(event.end_time + 10) 
                if(ending_break_box != end_box):
                    if(self.week[event.day_of_week][ending_break_box - 1] == None):
                        self.week[event.day_of_week][ending_break_box - 1] = "Break"
                    elif self.week[event.day_of_week][ending_break_box - 1] != "Break":
                        if not(event in self.alerts):
                            self.alerts.append(event)

            else:
                if(event.start_time == 0):
                    ending_break_box = self.time_to_box_number(event.end_time + 10) 
                    if(ending_break_box != end_box):
                        if(self.week[event.day_of_week][ending_break_box -1] == None):
                            self.week[event.day_of_week][ending_break_box -1] = "Break"
                        elif self.week[event.day_of_week][ending_break_box -1] != "Break":
                            if not(event in self.alerts):
                                self.alerts.append(event)
                else:
                    starting_break_box = self.time_to_box_number(event.start_time - 10, True)
                    if(starting_break_box != start_box):
                        if(self.week[event.day_of_week][starting_break_box] == None):
                            self.week[event.day_of_week][starting_break_box] = "Break"
                        else:
                            if not(event in self.alerts):
                                self.alerts.append(event)

            deal_with_meals = []

            for box in range(start_box, end_box): 
                if self.week[event.day_of_week][box] != None and type(self.week[event.day_of_week][box]) == Meals:
                    deal_with_meals.append(self.week[event.day_of_week][box])

            # print("THE DEAL WITH WITH MEALS IS: ")
            # for i in deal_with_meals:
            #     print(i.name)
            #     print(i.day_of_week)
            
            if(len(deal_with_meals) == 0):
                for box in range(start_box, end_box):
                    self.week[event.day_of_week][box] = event
            
            else:
                new_events = [event]
                for meal in deal_with_meals:
                    og_event = new_events[len(new_events)-1]
                    new_event = copy.deepcopy(og_event)
                    new_event2 = copy.deepcopy(og_event)
                    new_events.remove(og_event)
                    new_event.end_time = meal.start_time
                    new_events.append(new_event)
                    new_event2.start_time = meal.end_time
                    new_events.append(new_event2)
                # for e in new_events:
                #     print("DOW: " + str(e.day_of_week))
                #     print("name: " + e.name)
                #     print("time: " + str(e.start_time) + " to " + str(e.end_time))
                for e in new_events:
                    start_box = self.time_to_box_number(e.start_time, True)
                    end_box = self.time_to_box_number(e.end_time)
                    for box in range(start_box, end_box):
                        self.week[e.day_of_week][box] = e
                    
                    
                

    def add_sleep(self):
        for i in range(5):
            new_event1 = Sleep(i, 0000, self.sleep[0])
            new_event2 = Sleep(i, self.sleep[1], 1440)
            self.add_immutable_events(new_event1)
            self.add_immutable_events(new_event2)
        for i in range(5, 7):
            new_event1 = Sleep(i, 0000, self.sleep[2])
            new_event2 = Sleep(i, self.sleep[3], 1440)
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
            if t.deadline != None:
                tasks_with_deadline.append(t)
            else:
                tasks_without_deadline.append(t)
        # sort tasks_with_deadline by the deadline date
        for i in range(0, len(tasks_with_deadline)):
            earliest_deadline = i
            for t in range(i + 1, len(tasks_with_deadline)):
                if tasks_with_deadline[t].deadline < tasks_with_deadline[earliest_deadline].deadline:
                    earliest_deadline = t
            second_deadline = tasks_with_deadline[i]
            tasks_with_deadline[i] = tasks_with_deadline[earliest_deadline]
            tasks_with_deadline[earliest_deadline] = second_deadline
        # input the task into the weekly schedule based on deadline
        for t in range(0, len(tasks_with_deadline)):
            break_from_first = False
            break_from_second = False
            num_boxes = self.time_to_box_number(tasks_with_deadline[t].time_needed)
            if num_boxes == 0:
                num_boxes += 1
            for d in range(0, len(self.week)):
                num_boxes = self.time_to_box_number(tasks_with_deadline[t].time_needed)
                for time in range(0, len(self.week[d])):
                    run_tasks_deadline = True
                    initial_time = 0
                    if self.week[d][time] == None:
                        initial_time = time
                        time += 1
                        num_boxes -= 1
                        while(num_boxes != 0):
                            if self.week[d][time] == None:
                                time += 1
                                num_boxes -= 1
                            else:
                                num_boxes = 0
                                run_tasks_deadline = False
                    else:
                        run_tasks_deadline = False
                    if run_tasks_deadline:
                        tasks_with_deadline[t].start_time = initial_time * 30
                        tasks_with_deadline[t].end_time = tasks_with_deadline[t].start_time + tasks_with_deadline[t].time_needed
                        tasks_with_deadline[t].day_of_week = d
                        for j in range(initial_time, time):
                            self.week[d][j] = tasks_with_deadline[t]
                        box_num = self.time_to_box_number(tasks_with_deadline[t].end_time + 10) - 1
                        if self.week[d][box_num] == None:
                            self.week[d][box_num] = "Break"
                        break_from_first = True
                        break_from_second = True
                    if break_from_first == True:
                        break
                if break_from_second == True:
                    break
        # adding tasks without deadlines to the schedule
        for t in range(0, len(tasks_without_deadline)):
            break_from_first = False
            break_from_second = False
            num_boxes = self.time_to_box_number(tasks_without_deadline[t].time_needed)
            if num_boxes == 0:
                num_boxes += 1
            for d in range(0, len(self.week)):
                for time in range(0, len(self.week[d])):
                    num_boxes = self.time_to_box_number(tasks_without_deadline[t].time_needed)
                    run_tasks_deadline = True
                    initial_time = 0
                    if self.week[d][time] == None:
                        initial_time = time
                        time += 1
                        num_boxes -= 1
                        while(num_boxes != 0):
                            if self.week[d][time] == None:
                                time += 1
                                num_boxes -= 1
                            else:
                                num_boxes = 0
                                run_tasks_deadline = False
                    else:
                        run_tasks_deadline = False
                    if run_tasks_deadline:
                        tasks_without_deadline[t].start_time = initial_time * 30
                        tasks_without_deadline[t].end_time = tasks_without_deadline[t].start_time + tasks_without_deadline[t].time_needed
                        tasks_without_deadline[t].day_of_week = d
                        for j in range(initial_time, time):
                            self.week[d][j] = tasks_without_deadline[t]
                        box_num = self.time_to_box_number(tasks_without_deadline[t].end_time + 10) - 1
                        if self.week[d][box_num] == None:
                            self.week[d][box_num] = "Break"
                        break_from_first = True
                        break_from_second = True
                    if break_from_first == True:
                        break
                if break_from_second == True:
                    break
            

    def time_to_box_number(self, time, round_down=False):
        result = int(time / 30)
        if time % 30 != 0:
            if round_down:
                return result
            result += 1
        return result
    
    def output(self):
        answer_list = []
        for day in self.week:
            for time in day:
                if time != None and time != "Break":
                    answer_list.append(time)
        index = 1
        while(index < len(answer_list)):
            if answer_list[index].name == answer_list[index-1].name and answer_list[index].start_time == answer_list[index-1].start_time and answer_list[index].day_of_week == answer_list[index-1].day_of_week:
                answer_list.pop(index)
            else:
                index += 1
        return answer_list


