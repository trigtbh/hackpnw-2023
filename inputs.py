from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import tkextrafont as tkef

import settings

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

# i'm sorry in advance
# :)

class MealsInput:

    def format_time(self, value):
        return f"{value:02}"

    def update_hours(self, *args):
        try:
            value = int(self.start_hours.get())
        except ValueError:
            value = 0
            self.start_hours_time.delete(0, END)
            self.start_hours_time.insert(0, self.format_time(value))
        if value > 23:
            value = 23
            self.start_hours_time.delete(0, END)
            self.start_hours_time.insert(0, self.format_time(value))

    def update_minutes(self, *args):
        try:
            value = int(self.start_minutes.get())
        except ValueError:
            value = 0
            self.start_minutes_time.delete(0, END)
            self.start_minutes_time.insert(0, self.format_time(value))
        if value > 59:
            value = 59
            self.start_minutes_time.delete(0, END)
            self.start_minutes_time.insert(0, self.format_time(value))


    def __init__(self, meals=[]):
        self.master = Tk()
        self.master.title("Add Meal Schedule")
        self.master.configure(background=rgb_to_hex(settings.LIME))
        
        font = tkef.Font(file="TT Norms Pro Regular.otf", size=20, family="TT Norms Pro")
        self.meals = meals
        self.meal = None
        # create a label and put it in the top left corner
        Label(self.master, text="Meal Name", font=font, background=rgb_to_hex(settings.LIME)).grid(row=0, column=0, sticky=W)
        # create a label for the meal name and save it as a variable
        self.meal_name_str = StringVar()
        self.meal_name = Entry(self.master, background=rgb_to_hex(tuple(min(255, x + 25) for x in settings.LIME)), width=8, textvariable=self.meal_name_str, font=font)
        self.meal_name.grid(row=0, column=1, sticky=W)
        Label(self.master, text="Meal Start (HHMM)", font=font, background=rgb_to_hex(settings.LIME)).grid(row=1, column=0, sticky=W)
        # create an entry for the meal time and save it as a variable
        self.meal_starttime_str = StringVar()
        self.meal_starttime = Entry(self.master, background=rgb_to_hex(tuple(min(255, x + 25) for x in settings.LIME)), width=8, textvariable=self.meal_starttime_str, font=font)
        self.meal_starttime.grid(row=1, column=1, sticky=W)
        Label(self.master, text="Meal End (HHMM)", font=font, background=rgb_to_hex(settings.LIME)).grid(row=2, column=0, sticky=W)
        # create an entry for the meal time and save it as a variable
        self.meal_endtime_str = StringVar()
        self.meal_endtime = Entry(self.master, background=rgb_to_hex(tuple(min(255, x + 25) for x in settings.LIME)), width=8, textvariable=self.meal_endtime_str, font=font)
        self.meal_endtime.grid(row=2, column=1, sticky=W)
        # create a multi select dropdown to allow the user to select multiple days of the week
        # create a button to add the meal to the list
        self.add_meal_btn = Button(self.master, width=8, background=rgb_to_hex(settings.LIME), activebackground=rgb_to_hex(tuple(min(255, x + 50) for x in settings.LIME)), text="Add Meal", font=font, command=self.add_meal)
        self.add_meal_btn.grid(row=4, column=0,  columnspan=2, sticky=W+E)
        

    def add_meal(self):
        meal_name = self.meal_name_str.get()
        meal_starttime = self.meal_starttime_str.get()
        meal_endtime = self.meal_endtime_str.get()
        # check if meal name is empty
        if meal_name == "":
            # alert user with messagebox
            messagebox.showerror("Error", "Please enter a meal name.")
            return
        # check if meal start time is empty or does not equal format HHMM
        if meal_starttime == "" or len(meal_starttime) != 4 or not meal_starttime.isdigit():
            # alert user with messagebox
            messagebox.showerror("Error", "Please enter a valid meal start time (HHMM).")
            return
        s_hours, s_minutes = meal_starttime[:2], meal_starttime[2:]
        if not(0 <= int(s_hours) <= 23) or not(0 <= int(s_minutes) <= 59):
            messagebox.showerror("Error", "Please enter a valid meal start time (HHMM).")
            return
        # do the same for end time
        if meal_endtime == "" or len(meal_endtime) != 4 or not meal_endtime.isdigit():
            # alert user with messagebox
            messagebox.showerror("Error", "Please enter a valid meal end time (HHMM).")
            return
        e_hours, e_minutes = meal_endtime[:2], meal_endtime[2:]
        if not(0 <= int(e_hours) <= 23) or not(0 <= int(e_minutes) <= 59):
            messagebox.showerror("Error", "Please enter a valid meal end time (HHMM).")
            return
        # check if meal start time is after meal end time
        if int(meal_starttime) > int(meal_endtime):
            messagebox.showerror("Error", "Please enter a valid meal start time (HHMM).")
            return

        
        self.meals.append({
            "name": meal_name,
            "start": meal_starttime,
            "end": meal_endtime
        })
        # end window
        self.master.destroy()



class SleepInput:

    def format_time(self, value):
        return f"{value:02}"

    def update_hours(self, *args):
        try:
            value = int(self.start_hours.get())
        except ValueError:
            value = 0
            self.start_hours_time.delete(0, END)
            self.start_hours_time.insert(0, self.format_time(value))
        if value > 23:
            value = 23
            self.start_hours_time.delete(0, END)
            self.start_hours_time.insert(0, self.format_time(value))

    def update_minutes(self, *args):
        try:
            value = int(self.start_minutes.get())
        except ValueError:
            value = 0
            self.start_minutes_time.delete(0, END)
            self.start_minutes_time.insert(0, self.format_time(value))
        if value > 59:
            value = 59
            self.start_minutes_time.delete(0, END)
            self.start_minutes_time.insert(0, self.format_time(value))


    def __init__(self, sleep={}):
        self.master = Tk()
        self.master.title("Set Up Sleep Schedule")
        self.master.configure(background=rgb_to_hex(settings.PINK))
        
        font = tkef.Font(file="TT Norms Pro Regular.otf", size=20, family="TT Norms Pro")
        self.sleep = {}
        self.meal = None
        # create a label and put it in the top left corner
        Label(self.master, text="Weekday Wake Up Time", font=font, background=rgb_to_hex(settings.PINK)).grid(row=0, column=0, sticky=W)
        # create an entry for the meal time and save it as a variable
        self.wd_start_hours = StringVar()
        self.wd_start_hours_time = Entry(self.master, background=rgb_to_hex(tuple(min(255, x + 25) for x in settings.PINK)), width=4, textvariable=self.wd_start_hours, font=font)
        self.wd_start_hours_time.grid(row=0, column=1, sticky=W)
        
        Label(self.master, text="Weekday Sleep Time", font=font, background=rgb_to_hex(settings.PINK)).grid(row=1, column=0, sticky=W)
        # create an entry for the meal time and save it as a variable
        self.wd_end_hours = StringVar()
        self.wd_end_hours_time = Entry(self.master, background=rgb_to_hex(tuple(min(255, x + 25) for x in settings.PINK)), width=4, textvariable=self.wd_end_hours, font=font)
        self.wd_end_hours_time.grid(row=1, column=1, sticky=W)

        Label(self.master, text="Weekend Wake Up Time", font=font, background=rgb_to_hex(settings.PINK)).grid(row=2, column=0, sticky=W)
        # create an entry for the meal time and save it as a variable
        self.we_start_hours = StringVar()
        self.we_start_hours_time = Entry(self.master, background=rgb_to_hex(tuple(min(255, x + 25) for x in settings.PINK)), width=4, textvariable=self.we_start_hours, font=font)
        self.we_start_hours_time.grid(row=2, column=1, sticky=W)

        Label(self.master, text="Weekend Sleep Time", font=font, background=rgb_to_hex(settings.PINK)).grid(row=3, column=0, sticky=W)
        # create an entry for the meal time and save it as a variable
        self.we_end_hours = StringVar()
        self.we_end_hours_time = Entry(self.master, background=rgb_to_hex(tuple(min(255, x + 25) for x in settings.PINK)), width=4, textvariable=self.we_end_hours, font=font)
        self.we_end_hours_time.grid(row=3, column=1, sticky=W)

        # create a button to update the schedule
        Button(self.master, text="Update Schedule", font=font, background=rgb_to_hex(settings.PINK), activebackground=rgb_to_hex(tuple(min(255, x + 50) for x in settings.PINK)), command=self.update_schedule).grid(row=4, column=0, columnspan=2, sticky=W+E)
        

    def update_schedule(self):
        wd_start_time = self.wd_start_hours.get()
        wd_end_time = self.wd_end_hours.get()
        we_start_time = self.we_start_hours.get()
        we_end_time = self.we_end_hours.get()
        
        if not wd_start_time.isdigit() or not wd_end_time.isdigit() or not we_start_time.isdigit() or not we_end_time.isdigit():
            messagebox.showerror("Error", "Please enter a valid time (HHMM).")
            return

        wd_start_hh, wd_start_mm = wd_start_time[:2], wd_start_time[2:]
        wd_end_hh, wd_end_mm = wd_end_time[:2], wd_end_time[2:]
        we_start_hh, we_start_mm = we_start_time[:2], we_start_time[2:]
        we_end_hh, we_end_mm = we_end_time[:2], we_end_time[2:]

        if any([not(0 <= int(x) <= 23) for x in [wd_start_hh, wd_end_hh, we_start_hh, we_end_hh]]):
            messagebox.showerror("Error", "Please enter a valid time (HHMM).")
            return

        if any([not(0 <= int(x) <= 59) for x in [wd_start_mm, wd_end_mm, we_start_mm, we_end_mm]]):
            messagebox.showerror("Error", "Please enter a valid time (HHMM).")
            return

        # check that the start times are after the end times
        if wd_start_time >= wd_end_time:
            messagebox.showerror("Error", "Please enter a valid time (HHMM).")
            return
        
        if we_start_time >= we_end_time:
            messagebox.showerror("Error", "Please enter a valid time (HHMM).")
            return

        self.sleep = {
            "wd_start": wd_start_time,
            "wd_end": wd_end_time,
            "we_start": we_start_time,
            "we_end": we_end_time
        }
        # end window
        self.master.destroy()

class EventsInput:

    def format_time(self, value):
        return f"{value:02}"

    def update_hours(self, *args):
        try:
            value = int(self.start_hours.get())
        except ValueError:
            value = 0
            self.start_hours_time.delete(0, END)
            self.start_hours_time.insert(0, self.format_time(value))
        if value > 23:
            value = 23
            self.start_hours_time.delete(0, END)
            self.start_hours_time.insert(0, self.format_time(value))

    def update_minutes(self, *args):
        try:
            value = int(self.start_minutes.get())
        except ValueError:
            value = 0
            self.start_minutes_time.delete(0, END)
            self.start_minutes_time.insert(0, self.format_time(value))
        if value > 59:
            value = 59
            self.start_minutes_time.delete(0, END)
            self.start_minutes_time.insert(0, self.format_time(value))


    def __init__(self, events=[]):
        self.master = Tk()
        self.master.title("Add Event")
        self.master.configure(background=rgb_to_hex(settings.BLUE))
        
        font = tkef.Font(file="TT Norms Pro Regular.otf", size=20, family="TT Norms Pro")
        self.events = events
        # create a label and put it in the top left corner
        Label(self.master, text="Event Name", font=font, background=rgb_to_hex(settings.BLUE)).grid(row=0, column=0, sticky=W)
        # create a label for the meal name and save it as a variable
        self.event_name_str = StringVar()
        self.event_name = Entry(self.master, background=rgb_to_hex(tuple(min(255, x + 25) for x in settings.BLUE)), width=8, textvariable=self.event_name_str, font=font)
        self.event_name.grid(row=0, column=1, sticky=W)
        Label(self.master, text="Event Start (HHMM)", font=font, background=rgb_to_hex(settings.BLUE)).grid(row=1, column=0, sticky=W)
        # create an entry for the meal time and save it as a variable
        self.event_starttime_str = StringVar()
        self.event_starttime = Entry(self.master, background=rgb_to_hex(tuple(min(255, x + 25) for x in settings.BLUE)), width=8, textvariable=self.event_starttime_str, font=font)
        self.event_starttime.grid(row=1, column=1, sticky=W)
        Label(self.master, text="Event End (HHMM)", font=font, background=rgb_to_hex(settings.BLUE)).grid(row=2, column=0, sticky=W)
        # create an entry for the meal time and save it as a variable
        self.event_endtime_str = StringVar()
        self.event_endtime = Entry(self.master, background=rgb_to_hex(tuple(min(255, x + 25) for x in settings.BLUE)), width=8, textvariable=self.event_endtime_str, font=font)
        self.event_endtime.grid(row=2, column=1, sticky=W)

        # add a label for day of the week
        Label(self.master, text="Day of the Week (1-7)", font=font, background=rgb_to_hex(settings.BLUE)).grid(row=3, column=0, sticky=W)
        self.day_of_week_str = StringVar()
        self.day_of_week = Entry(self.master, background=rgb_to_hex(tuple(min(255, x + 25) for x in settings.BLUE)), width=8, textvariable=self.day_of_week_str, font=font)
        self.day_of_week.grid(row=3, column=1, sticky=W)

        # create a multi select dropdown to allow the user to select multiple days of the week
        # create a button to add the meal to the list
        self.add_event_btn = Button(self.master, width=8, background=rgb_to_hex(settings.BLUE), activebackground=rgb_to_hex(tuple(min(255, x + 50) for x in settings.BLUE)), text="Add Event", font=font, command=self.add_event)
        self.add_event_btn.grid(row=4, column=0, columnspan=2, sticky=W+E)
        

    def add_event(self):
        # get all vars
        event_name = self.event_name_str.get()
        event_starttime = self.event_starttime_str.get()
        event_endtime = self.event_endtime_str.get()
        day_of_week = self.day_of_week_str.get()

        # check if all vars are filled
        if event_name == "":
            messagebox.showerror("Error", "Please enter a valid event name.")
            return
        
        # check if start time and end time are valid
        if len(event_starttime) != 4 or len(event_endtime) != 4:
            messagebox.showerror("Error", "Please enter a valid time (HHMM).")
            return
        sh, sm = event_starttime[:2], event_starttime[2:]
        eh, em = event_endtime[:2], event_endtime[2:]
        if not sh.isdigit() or not sm.isdigit() or not eh.isdigit() or not em.isdigit():
            messagebox.showerror("Error", "Please enter a valid time (HHMM).")
            return
        sh, sm, eh, em = int(sh), int(sm), int(eh), int(em)
        if not(0 <= sh <= 23 and 0 <= sm <= 59 and 0 <= eh <= 23 and 0 <= em <= 59):
            messagebox.showerror("Error", "Please enter a valid time (HHMM).")
            return

        # check if day of week is valid
        if not day_of_week.isdigit():
            messagebox.showerror("Error", "Please enter a valid day of the week (1-7).")
            return
        day_of_week = int(day_of_week)
        if not(1 <= day_of_week <= 7):
            messagebox.showerror("Error", "Please enter a valid day of the week (1-7).")
            return

        day_of_week -= 1
        
        self.events.append({"name": event_name, "start": event_starttime, "end": event_endtime, "day": day_of_week})
        # end window
        self.master.destroy()

class TasksInput:

    def format_time(self, value):
        return f"{value:02}"

    def update_hours(self, *args):
        try:
            value = int(self.start_hours.get())
        except ValueError:
            value = 0
            self.start_hours_time.delete(0, END)
            self.start_hours_time.insert(0, self.format_time(value))
        if value > 23:
            value = 23
            self.start_hours_time.delete(0, END)
            self.start_hours_time.insert(0, self.format_time(value))

    def update_minutes(self, *args):
        try:
            value = int(self.start_minutes.get())
        except ValueError:
            value = 0
            self.start_minutes_time.delete(0, END)
            self.start_minutes_time.insert(0, self.format_time(value))
        if value > 59:
            value = 59
            self.start_minutes_time.delete(0, END)
            self.start_minutes_time.insert(0, self.format_time(value))


    def __init__(self, tasks=[]):
        self.master = Tk()
        self.master.title("Add Task")
        self.master.configure(background=rgb_to_hex(settings.ORANGE))
        
        self.tasks = tasks
        font = tkef.Font(file="TT Norms Pro Regular.otf", size=20, family="TT Norms Pro")
        # create a label and put it in the top left corner
        Label(self.master, text="Task Name", font=font, background=rgb_to_hex(settings.ORANGE)).grid(row=0, column=0, sticky=W)
        # create a label for the meal name and save it as a variable
        self.event_name_str = StringVar()
        self.event_name = Entry(self.master, background=rgb_to_hex(tuple(min(255, x + 25) for x in settings.ORANGE)), width=8, textvariable=self.event_name_str, font=font)
        self.event_name.grid(row=0, column=1, sticky=W)
        Label(self.master, text="Task Length (Minutes)", font=font, background=rgb_to_hex(settings.ORANGE)).grid(row=1, column=0, sticky=W)
        # create an entry for the meal time and save it as a variable
        self.event_duration_str = StringVar()
        self.event_duration = Entry(self.master, background=rgb_to_hex(tuple(min(255, x + 25) for x in settings.ORANGE)), width=8, textvariable=self.event_duration_str, font=font)
        self.event_duration.grid(row=1, column=1, sticky=W)
        
        Label(self.master, text="Deadline Day (1-7)", font=font, background=rgb_to_hex(settings.ORANGE)).grid(row=2, column=0, sticky=W)
        self.day_of_week_str = StringVar()
        self.day_of_week = Entry(self.master, background=rgb_to_hex(tuple(min(255, x + 25) for x in settings.ORANGE)), width=8, textvariable=self.day_of_week_str, font=font)
        self.day_of_week.grid(row=2, column=1, sticky=W)

        self.add_task_button = Button(self.master, text="Add Task", font=font, background=rgb_to_hex(settings.ORANGE), activebackground=rgb_to_hex(tuple(min(255, x + 25) for x in settings.ORANGE)), command=self.add_task)
        self.add_task_button.grid(row=3, column=0, columnspan=2, sticky=W+E)
        

    def add_task(self):
        # get all vars
        task_name = self.event_name_str.get()
        task_duration = self.event_duration_str.get()

        # check if all vars are filled
        if task_name == "":
            messagebox.showerror("Error", "Please enter a task name.")
            return
        
        # check if duration is valid
        if not task_duration.isdigit():
            messagebox.showerror("Error", "Please enter a valid duration (in minutes).")
            return
        task_duration = int(task_duration)
        if task_duration <= 0:
            messagebox.showerror("Error", "Please enter a valid duration (in minutes).")
            return

        # check if day of week is valid
        day_of_week = self.day_of_week_str.get()
        if day_of_week != "":
            if not self.day_of_week_str.get().isdigit():
                messagebox.showerror("Error", "Please enter a valid day of the week (1-7).")
                return
            day_of_week = int(self.day_of_week_str.get())
            if not(1 <= day_of_week <= 7):
                messagebox.showerror("Error", "Please enter a valid day of the week (1-7).")
                return
            day_of_week -= 1
        else:
            day_of_week = None
        
        self.tasks.append({"name": task_name, "duration": task_duration, "day": day_of_week})
        # end window
        self.master.destroy()

