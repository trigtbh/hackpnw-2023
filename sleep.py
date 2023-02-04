from immutable_events import ImmutableEvent
class Sleep:
    # def __init__(self, wd_wakeup_time, wd_sleep_time, we_wakeup_time, we_sleep_time):
    #     self.we_wakeup_time = we_wakeup_time # the wake up time for every week day (M, T, W, T, F)
    #     self.we_sleep_time = we_sleep_time # the sleep time for every week day (M, T, W, T, F)
    #     self.wd_wakeup_time = wd_wakeup_time # the wake up time for every day of the week end (S, S)
    #     self.wd_sleep_time = wd_sleep_time # the sleep time for every day of the week end (S, S)
    #     self.name = "Sleep"
    
    def __init__(self, day_of_week, start_time, end_time):
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
        self.name = "Sleep"
        self.commute = None

    
    # using wake up and sleep time data, creates 14 ImmutableEvent objects that represent all blocks of sleep
    # def return_sleep_events(self) -> list[ImmutableEvent]:
    #     sleep_event_list = []

    #     # creates ImmutableEvent objects for sleep during the week days
    #     for i in range(5):
    #         new_event1 = ImmutableEvent(i, 0000, self.wd_wakeup_time, "Sleep")
    #         new_event2 = ImmutableEvent(i, self.wd_sleep_time, 1440,  "Sleep")
    #         sleep_event_list.append(new_event1)
    #         sleep_event_list.append(new_event2)

    #     # creates ImmutableEvent objects for sleep during the week end
    #     for i in range(5, 7):
    #         new_event1 = ImmutableEvent(i, 0000, self.we_wakeup_time, "Sleep")
    #         new_event2 = ImmutableEvent(i, self.we_sleep_time, 1440, "Sleep")
    #         sleep_event_list.append(new_event1)
    #         sleep_event_list.append(new_event2)

    #     return sleep_event_list
