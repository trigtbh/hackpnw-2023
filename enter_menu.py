import os
# disable pygame boot message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import settings

from tasks import Task
from meals import Meals
from sleep import Sleep
from immutable_events import ImmutableEvent


# create button class 
class Button:
    def __init__(self, x, y, width, height, color, text, text_color, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = font

    def draw(self, win):
        # create transparent surface
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.set_alpha(128)
        pygame.draw.rect(self.surface, self.color, (0, 0, self.width, self.height), border_radius=30)
        title = self.font.render(self.text, 1, self.text_color)
        # center surface on self.x and self.y
        win.blit(self.surface, (self.x - self.width / 2, self.y - self.height / 2))
        
        # draw at the top of the button
        win.blit(title, (self.x + (self.width / 2 - title.get_width() / 2), self.y))
        # draw a small line under the title
        pygame.draw.line(win, self.text_color, (self.x + (self.width / 2 - title.get_width() / 2), self.y + title.get_height()), (self.x + (self.width / 2 + title.get_width() / 2), self.y + title.get_height()), 2)

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
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
        self.sleep_button = Button(self.width / 4, self.height / 3, self.width / 3, self.height / 3, settings.PINK, "Sleep", settings.FONT_COLOR, settings.FONT_LARGE)
        self.meals_button = Button(self.width / 4, self.height / 2, self.width / 3, self.height / 3, settings.LIME, "Meals", settings.FONT_COLOR, settings.FONT_LARGE)
        self.tasks_button = Button(self.width / 4, self.height / 1.5, self.width / 3, self.height / 3, settings.ORANGE, "Tasks", settings.FONT_COLOR, settings.FONT_LARGE)
        self.events_button = Button(self.width / 4, self.height / 1.2, self.width / 3, self.height / 3, settings.BLUE, "Events", settings.FONT_COLOR, settings.FONT_LARGE)

        self.buttons = [self.sleep_button, self.meals_button, self.tasks_button, self.events_button]

        while True:
            self.update()

    def draw_text(self):
        title = settings.FONT_TITLE.render("Hello World", True, settings.FONT_COLOR)
        # render title to the top center of the screen
        self.screen.blit(title, (self.width / 2 - title.get_width() / 2, 0))
        # draw a small line under the title
        pygame.draw.line(self.screen, settings.FONT_COLOR, (self.width / 2 - title.get_width() / 2, title.get_height()), (self.width / 2 + title.get_width() / 2, title.get_height()), 2)
    
    def draw_boxes(self):
        # create transparent surf
        for button in self.buttons:
            button.draw(self.screen)
        surf = pygame.Surface((self.width / 3, self.height / 3), pygame.SRCALPHA)
        surf.set_alpha(128)
        pygame.draw.rect(surf, settings.PINK, (0, 0, self.width / 3, self.height // 3.5), border_radius=30)
        # add title to that rect
        title = settings.FONT_LARGE.render("Sleep", True, settings.FONT_COLOR)
        # center rect on the quarter line of the screen, and 1/3 of the way down
        self.screen.blit(surf, (self.width / 4 - surf.get_width() / 2, self.height / 3 - surf.get_height() / 2))
        # add title to the top of the rect
        self.screen.blit(title, (self.width / 4 - title.get_width() / 2, self.height / 3 - surf.get_height() / 2))
        # add a small line under the title
        pygame.draw.line(self.screen, settings.FONT_COLOR, (self.width / 4 - title.get_width() / 2, self.height / 3 - surf.get_height() / 2 + title.get_height()), (self.width / 4 + title.get_width() / 2, self.height / 3 - surf.get_height() / 2 + title.get_height()), 2)

        # repeat for the other boxes
        surf = pygame.Surface((self.width / 3, self.height / 3), pygame.SRCALPHA)
        surf.set_alpha(128)
        pygame.draw.rect(surf, settings.LIME, (0, 0, self.width / 3, self.height // 3.5), border_radius=30)
        title = settings.FONT_LARGE.render("Meals", True, settings.FONT_COLOR)
        self.screen.blit(surf, (self.width / 4 - surf.get_width() / 2, self.height / 3 * 2 - surf.get_height() / 2))
        self.screen.blit(title, (self.width / 4 - title.get_width() / 2, self.height / 3 * 2 - surf.get_height() / 2))
        pygame.draw.line(self.screen, settings.FONT_COLOR, (self.width / 4 - title.get_width() / 2, self.height / 3 * 2 - surf.get_height() / 2 + title.get_height()), (self.width / 4 + title.get_width() / 2, self.height / 3 * 2 - surf.get_height() / 2 + title.get_height()), 2)

        surf = pygame.Surface((self.width / 3, self.height / 3), pygame.SRCALPHA)
        surf.set_alpha(128)
        pygame.draw.rect(surf, settings.ORANGE, (0, 0, self.width / 3, self.height // 3.5), border_radius=30)
        title = settings.FONT_LARGE.render("Tasks", True, settings.FONT_COLOR)
        self.screen.blit(surf, (self.width / 4 * 3 - surf.get_width() / 2, self.height / 3 - surf.get_height() / 2))
        self.screen.blit(title, (self.width / 4 * 3 - title.get_width() / 2, self.height / 3 - surf.get_height() / 2))
        pygame.draw.line(self.screen, settings.FONT_COLOR, (self.width / 4 * 3 - title.get_width() / 2, self.height / 3 - surf.get_height() / 2 + title.get_height()), (self.width / 4 * 3 + title.get_width() / 2, self.height / 3 - surf.get_height() / 2 + title.get_height()), 2)

        surf = pygame.Surface((self.width / 3, self.height / 3), pygame.SRCALPHA)
        surf.set_alpha(128)
        pygame.draw.rect(surf, settings.BLUE, (0, 0, self.width / 3, self.height // 3.5), border_radius=30)
        title = settings.FONT_LARGE.render("Events", True, settings.FONT_COLOR)
        self.screen.blit(surf, (self.width / 4 * 3 - surf.get_width() / 2, self.height / 3 * 2 - surf.get_height() / 2))
        self.screen.blit(title, (self.width / 4 * 3 - title.get_width() / 2, self.height / 3 * 2 - surf.get_height() / 2))
        pygame.draw.line(self.screen, settings.FONT_COLOR, (self.width / 4 * 3 - title.get_width() / 2, self.height / 3 * 2 - surf.get_height() / 2 + title.get_height()), (self.width / 4 * 3 + title.get_width() / 2, self.height / 3 * 2 - surf.get_height() / 2 + title.get_height()), 2)

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

        self.screen.fill(settings.LIGHTER_DARK_BLUE)
        self.draw_text()
        self.draw_boxes()


        pygame.display.update()

if __name__ == "__main__":
    MainMenu()