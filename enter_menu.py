import os
# disable pygame boot message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import settings

from tasks import Task
from meals import Meals
from sleep import Sleep
from immutable_events import ImmutableEvent


import threading
from inputs import SleepInput, MealsInput, TasksInput, EventsInput

# create button class 
class Button:
    def __init__(self, x, y, width, height, color, text, text_color, font, truecenter = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.lighter_color = tuple(min(255, i + 25) for i in color)
        self.text = text
        self.text_color = text_color
        self.font = font
        self.inner_text = None
        self.truecenter = truecenter

    def draw(self, win):
        # create transparent surface
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.set_alpha(128)
        
        # if mouse is hovering, draw a border around the button
        if self.is_over(pygame.mouse.get_pos()):
            pygame.draw.rect(win, self.text_color, (self.x - self.width / 2, self.y - self.height / 2, self.width, self.height), 2, border_radius=30)
            pygame.draw.rect(self.surface, self.lighter_color, (0, 0, self.width, self.height), border_radius=30)
    
        else:
            pygame.draw.rect(self.surface, self.color, (0, 0, self.width, self.height), border_radius=30)
    

        title = self.font.render(self.text, 1, self.text_color)
        # center surface on self.x and self.y
        win.blit(self.surface, (self.x - self.width / 2, self.y - self.height / 2))
        
        # draw at the top of the button
        if not self.truecenter:
            win.blit(title, (self.x - title.get_width() / 2, self.y - self.height / 2))
            # draw a small line under the title
            pygame.draw.line(win, self.text_color, (self.x - title.get_width() / 2, self.y - self.height / 2 + title.get_height()), (self.x + title.get_width() / 2, self.y - self.height / 2 + title.get_height()), 2)
        else:
            win.blit(title, (self.x - title.get_width() / 2, self.y - title.get_height() / 2))
    
        
    def is_over(self, pos):
        if pos[0] > self.x - self.width / 2  and pos[0] < self.x + self.width / 2:
            if pos[1] > self.y - self.height / 2 and pos[1] < self.y + self.height / 2:
                return True
        return False

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.is_over(event.pos):
                    return True
        return False

class MainMenu:
    def __init__(self):
        self.width = settings.WIDTH
        self.height = settings.HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(settings.TITLE)


        # create buttons for sleep, meals, tasks, events
        self.sleep_button = Button(self.width / 4, self.height / 3, self.width / 3, self.height // 3.5, settings.PINK, "Sleep", settings.FONT_COLOR, settings.FONT_LARGE)
        self.sleep_button.inner_text = "Click to set up sleep schedule"
        self.meals_button = Button(self.width / 4 * 3, self.height / 3, self.width / 3, self.height // 3.5, settings.LIME, "Meals", settings.FONT_COLOR, settings.FONT_LARGE)
        self.meals_button.inner_text = "Click to add meals"
        self.tasks_button = Button(self.width / 4, self.height / 3 * 2, self.width / 3, self.height // 3.5, settings.ORANGE, "Tasks", settings.FONT_COLOR, settings.FONT_LARGE)
        self.tasks_button.inner_text = "Click to add tasks"
        self.events_button = Button(self.width / 4 * 3, self.height / 3 * 2, self.width / 3, self.height // 3.5, settings.BLUE, "Events", settings.FONT_COLOR, settings.FONT_LARGE)
        self.events_button.inner_text = "Click to add events"

        self.submit_button = Button(self.width / 2, self.height - self.height / 10, self.width / 3, self.height / 10, settings.LIME, "Submit", settings.FONT_COLOR, settings.FONT_LARGE, truecenter=True)
        self.buttons = [self.sleep_button, self.meals_button, self.tasks_button, self.events_button, self.submit_button]


        self.sleeps = []
        self.meals = []
        self.tasks = []
        self.events = []

        while True:
            self.update()

    def draw_text(self):
        title = settings.FONT_TITLE.render(settings.TITLE.upper(), True, settings.FONT_COLOR)
        # render title to the top center of the screen
        self.screen.blit(title, (self.width / 2 - title.get_width() / 2, 0))
        # draw a small line under the title
        pygame.draw.line(self.screen, settings.FONT_COLOR, (self.width / 2 - title.get_width() / 2, title.get_height()), (self.width / 2 + title.get_width() / 2, title.get_height()), 2)
    
    def draw_boxes(self):
        # create transparent surf
        for button in self.buttons:
            button.draw(self.screen)
            if button.inner_text:
                # process new lines in inner_text
                inner_text = button.inner_text.split("\n")
                for i, line in enumerate(inner_text):
                    inner_text[i] = settings.FONT.render(line, True, settings.FONT_COLOR)
                # draw inner text
                for i, line in enumerate(inner_text):
                    self.screen.blit(line, (button.x - line.get_width() / 2, button.y - button.height / 2 + button.height / 4 + i * line.get_height()))


            
    def update(self):
        self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.VIDEORESIZE:
                self.window = pygame.display.set_mode((max(event.w, settings.WIDTH), max(event.h, settings.HEIGHT)), pygame.RESIZABLE)
                self.width = max(event.w, settings.WIDTH)
                self.height = max(event.h, settings.HEIGHT)
                self.sleep_button = Button(self.width / 4, self.height / 3, self.width / 3, self.height // 3.5, settings.PINK, "Sleep", settings.FONT_COLOR, settings.FONT_LARGE)
                self.meals_button = Button(self.width / 4 * 3, self.height / 3, self.width / 3, self.height // 3.5, settings.LIME, "Meals", settings.FONT_COLOR, settings.FONT_LARGE)
                self.tasks_button = Button(self.width / 4, self.height / 3 * 2, self.width / 3, self.height // 3.5, settings.ORANGE, "Tasks", settings.FONT_COLOR, settings.FONT_LARGE)
                self.events_button = Button(self.width / 4 * 3, self.height / 3 * 2, self.width / 3, self.height // 3.5, settings.BLUE, "Events", settings.FONT_COLOR, settings.FONT_LARGE)
                self.sleep_button.inner_text = "Click to set up sleep schedule"
                if len(self.sleeps) > 0:
                    # render number of schedules in sleep, then "click to edit schedules" on a new line
                    self.sleep_button.inner_text = f"{len(self.sleeps)} schedule{'s' if len(self.sleeps) != 1 else ''}\nClick to edit schedules"
                self.meals_button.inner_text = "Click to add meals"
                if len(self.meals) > 0:
                    # render number of meals in meals, then "click to edit meals" on a new line
                    self.meals_button.inner_text = f"{len(self.meals)} meal{'s' if len(self.meals) != 1 else ''}\nClick to edit meals"
                self.tasks_button.inner_text = "Click to add tasks"
                if len(self.tasks) > 0:
                    # render number of tasks in tasks, then "click to edit tasks" on a new line
                    self.tasks_button.inner_text = f"{len(self.tasks)} task{'s' if len(self.tasks) != 1 else ''}\nClick to edit tasks"
                self.events_button.inner_text = "Click to add events"
                if len(self.events) > 0:
                    # render number of events in events, then "click to edit events" on a new line
                    self.events_button.inner_text = f"{len(self.events)} event{'s' if len(self.events) != 1 else ''}\nClick to edit events"
                
                # create a submit button in the center bottom
                
                self.submit_button = Button(self.width / 2, self.height - self.height / 10, self.width / 3, self.height / 10, settings.LIME, "Submit", settings.FONT_COLOR, settings.FONT_LARGE, truecenter=True)
                self.buttons = [self.sleep_button, self.meals_button, self.tasks_button, self.events_button, self.submit_button]

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(event):
                        if button.text == "Sleep":
                            sm = SleepInput()
                            threading.Thread(target=sm.master.mainloop()).start()
                            if sm.sleep:
                                self.sleeps = [sm.sleep]
                                
                                self.sleep_button.inner_text = f"{len(self.sleeps)} schedule{'s' if len(self.sleeps) != 1 else ''}\nClick to edit schedules"
                        elif button.text == "Meals":
                            mm = MealsInput()
                            threading.Thread(target=mm.master.mainloop()).start()
                            self.meals = mm.meals
                            if len(self.meals) > 0:
                                self.meals_button.inner_text = f"{len(self.meals)} meal{'s' if len(self.meals) != 1 else ''}\nClick to edit meals"
                        elif button.text == "Tasks":
                            tm = TasksInput(self.tasks)
                            threading.Thread(target=tm.master.mainloop()).start()
                            self.tasks = tm.tasks
                            if len(self.tasks) > 0:
                                self.tasks_button.inner_text = f"{len(self.tasks)} task{'s' if len(self.tasks) != 1 else ''}\nClick to edit tasks"
                        elif button.text == "Events":
                            em = EventsInput(self.events)
                            threading.Thread(target=em.master.mainloop()).start()
                            self.events = em.events
                            if len(self.events) > 0:
                                self.events_button.inner_text = f"{len(self.events)} event{'s' if len(self.events) != 1 else ''}\nClick to edit events"
                        elif button.text == "Submit":
                            print(self.sleeps, self.meals, self.tasks, self.events)
                            

        self.screen.fill(settings.LIGHTER_DARK_BLUE)
        self.draw_text()
        self.draw_boxes()



        pygame.display.update()

if __name__ == "__main__":
    MainMenu()