import os
# disable pygame boot message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import settings

from tasks import Task
from meals import Meals
from sleep import Sleep
from immutable_events import ImmutableEvent
from calculate_schedule import CalculateSchedule


class CalendarView:
    def __init__(self, events):
        self.width = settings.WIDTH
        self.height = settings.HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.events = events
        
        self.y = 0
        self.drag = False

        for item in self.events:
            item.day_of_week += 1
            
        while True:
            self.update()

    def draw_events(self):
        for event in self.events:
            
            if type(event) == ImmutableEvent:
                color = settings.BLUE
            elif type(event) == Task:
                color = settings.ORANGE
            elif type(event) == Meals:
                color = settings.LIME
            elif type(event) == Sleep:
                color = settings.PINK

            # lower opacity
            color = tuple(list(color) + [0.45])

            # convert the start and end times in minutes to a height in pixels
            start_height = settings.WHITE_SPACE + (1 - 2 * settings.WHITE_SPACE) * event.start_time / 1440 * 4
            end_height = settings.WHITE_SPACE + (1 - 2 * settings.WHITE_SPACE) * event.end_time / 1440 * 4

            # draw the event
            # use day of the week to determine column
            # limit left, right edges of box to edges of the column
            #pygame.draw.rect(self.window, color, (1 + event.day_of_week * self.width / 8, 1 + self.height * start_height - self.y, -1 + self.width / 8, self.height * (end_height - start_height)))
            
            # create surface for the event
            #event_surface = pygame.Surface((self.width / 8 - 2, self.height * (end_height - start_height) - 2), pygame.SRCALPHA)
            event_surface = pygame.Surface((self.width / 8 - 1, self.height * (end_height - start_height) - 1))
            event_surface.set_alpha(100)
            event_surface.fill(color)
            self.window.blit(event_surface, (1 + event.day_of_week * self.width / 8, 1 + self.height * start_height - self.y))
            


            
            # draw name of event, start time at the top of box, end time at the bottom
            # draw name in the center of the box
            # draw times within the box itself
            # use day of the week to determine column
            # process minutes to readable time
            # zero pad minutes
            start_time = str(event.start_time // 60) + ":" + str(event.start_time % 60).zfill(2)
            end_time = str(event.end_time // 60) + ":" + str(event.end_time % 60).zfill(2)
            
            # draw text in order as start first, then name, then end
            # start will be at the top of the box, name in the middle, end at the bottom
            # draw start time
            padding = 2.5
            text = settings.FONT_SMALL.render(start_time, True, settings.FONT_COLOR)
            #self.window.blit(text, (event.day_of_week * self.width / 8 + self.width / 16 - text.get_width() / 2, self.height * start_height - self.y + padding))
            
            text = event.name
            # word wrap text if it is too long

            if settings.FONT.size(text)[0] > self.width / 8 - 2 * padding:
                text = ""
                words = event.name.split()
                for word in words:
                    if settings.FONT.size(text + word)[0] < self.width / 8 - 2 * padding:
                        text += word + " "
                    else:
                        text += "\n" + word + " "
            
            text = text.strip()
            # for each line of text, draw it
            # center entire text block vertically
            # center each line horizontally
            lines = text.split("\n")
            for i in range(len(lines)):
                text = settings.FONT.render(lines[i], True, settings.FONT_COLOR)
                self.window.blit(text, (event.day_of_week * self.width / 8 + self.width / 16 - text.get_width() / 2, self.height * (start_height + end_height) / 2 - self.y - text.get_height() * len(lines) / 2 + text.get_height() * i))

            # if the center text isn't clipping into the time text, draw the time text
            #if self.height * (start_height + end_height) / 2 - self.y - text.get_height() * len(lines) / 2 > self.height * start_height - self.y + padding and self.height * (start_height + end_height) / 2 - self.y - text.get_height() * len(lines) / 2 < self.height * end_height - self.y - text.get_height() - padding:
            
            
            starttime = settings.FONT_SMALL.render(start_time, True, settings.FONT_COLOR)
            endtime = settings.FONT_SMALL.render(end_time, True, settings.FONT_COLOR)
            # if the center text won't clip into the time text, draw the time text
            if self.height * (start_height + end_height) / 2 - self.y - text.get_height() * len(lines) / 2 > self.height * start_height - self.y + padding + starttime.get_height() and self.height * (start_height + end_height) / 2 - self.y - text.get_height() * len(lines) / 2 < self.height * end_height - self.y - text.get_height() - padding - endtime.get_height():
                # draw start time
                self.window.blit(starttime, (event.day_of_week * self.width / 8 + self.width / 16 - starttime.get_width() / 2, self.height * start_height - self.y + padding))
                # draw end time
                self.window.blit(endtime, (event.day_of_week * self.width / 8 + self.width / 16 - endtime.get_width() / 2, self.height * end_height - self.y - endtime.get_height() - padding))
            
                # # draw end time
            text = settings.FONT_SMALL.render(end_time, True, settings.FONT_COLOR)
            #self.window.blit(text, (event.day_of_week * self.width / 8 + self.width / 16 - text.get_width() / 2, self.height * end_height - self.y - text.get_height() - padding))



    def draw_grid(self):
        # draw vertical lines that screen into 8 equal sized columns
        for i in range(1, 8):
            pygame.draw.line(self.window, settings.COLUMN_LINES, (self.width * i / 8, 0), (self.width * i / 8, self.height), 1)
        
        # draw horizontal lines - one section = 30 minutes
        # display 6 hours worth of time immediately, then allow user to scroll down and see more
        # take self.y into account to determine where to position the lines
        for i in range(1, 48):
            pygame.draw.line(self.window, settings.ROW_LINES, (0, self.height * settings.WHITE_SPACE + self.height * (1 - 2 * settings.WHITE_SPACE) * i / 12 - self.y), (self.width, self.height * settings.WHITE_SPACE + self.height * (1 - 2 * settings.WHITE_SPACE) * i / 12 - self.y), 1)
        # add the first horizontal line at the top of the grid
        pygame.draw.line(self.window, settings.ROW_LINES, (0, self.height * settings.WHITE_SPACE - self.y), (self.width, self.height * settings.WHITE_SPACE - self.y), 1)

    def draw_time(self):
        # add white rectangle to cover up the left side of the grid
        pygame.draw.rect(self.window, settings.BACKGROUND, (0, 0, self.width / 8, self.height))
        # redraw column, and rows lines
        # draw column top to bottom
        pygame.draw.line(self.window, settings.COLUMN_LINES, (self.width / 8, 0), (self.width / 8, self.height), 1)

        # draw the time labels on the left side of the grid
        # display text vertically in the space between the lines
        # start at midnight, end at midnight the next day
        # draw all the text on their own lines
        # center the text in the leftmost column
        for i in range(0, 49):
            text = settings.FONT_SMALL.render(f"{i // 2}:{'00' if i % 2 == 0 else '30'}", True, settings.FONT_COLOR)
            self.window.blit(text, (self.width / 16 - text.get_width() / 2, self.height * settings.WHITE_SPACE + self.height * (1 - 2 * settings.WHITE_SPACE) * i / 12 - self.y - text.get_height() / 2))
        
    def draw_bars(self):
        # draw rectangles to cover up lines at top and bottom
        # ignore first column
        pygame.draw.rect(self.window, settings.BACKGROUND, (1 + self.width / 8, 0, self.width * 7 / 8, self.height * settings.WHITE_SPACE))
        pygame.draw.rect(self.window, settings.BACKGROUND, (1 + self.width / 8, self.height * (1 - settings.WHITE_SPACE), self.width * 7 / 8, self.height * settings.WHITE_SPACE + 1))


        # draw lines at top and bottom to separate the grid from the rest of the window
        # ignore first column
        pygame.draw.line(self.window, settings.COLUMN_LINES, (self.width / 8, self.height * settings.WHITE_SPACE), (self.width, self.height * settings.WHITE_SPACE), 1)
        pygame.draw.line(self.window, settings.COLUMN_LINES, (self.width / 8, self.height * (1 - settings.WHITE_SPACE)), (self.width, self.height * (1 - settings.WHITE_SPACE)), 1)


    def draw_day_names(self):
        # draw names up at the top of the grid
        # center text on white space in between column lines, not on the lines themselves
        names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i in range(1, 8):
            text = settings.FONT_A_BIT_SMALLER.render(names[i - 1], True, settings.FONT_COLOR)
            self.window.blit(text, (self.width * (i + 0.5) / 8 - text.get_width() / 2, self.height * settings.WHITE_SPACE / 2 - text.get_height() / 2))
    
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
                # readjust self.y
                self.y = min(self.y, self.height * (1 - 2 * settings.WHITE_SPACE) * 48 / 12 - self.height * (1 - 2 * settings.WHITE_SPACE))


            # detect mouse drag events, update self.y to simulate scrolling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.drag = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.drag = False

            if event.type == pygame.MOUSEMOTION:
                if self.drag:
                    self.y -= event.rel[1]
                    # keep y within bounds
                    self.y = max(self.y, 0)
                    self.y = min(self.y, self.height * (1 - 2 * settings.WHITE_SPACE) * 48 / 12 - self.height * (1 - 2 * settings.WHITE_SPACE))

            # detect trackpad scroll or mouse scroll
            if event.type == pygame.MOUSEWHEEL:
                self.y -= event.y * 15
                self.y = max(self.y, 0)
                self.y = min(self.y, self.height * (1 - 2 * settings.WHITE_SPACE) * 48 / 12 - self.height * (1 - 2 * settings.WHITE_SPACE))
            
            
        self.window.fill(settings.LIGHTER_DARK_BLUE)
        self.draw_grid()
        self.draw_time()
        self.draw_events()
        self.draw_bars()
        
        self.draw_day_names()
        pygame.display.update()
