import os
# disable pygame boot message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import settings

from tasks import Task
from meals import Meals
from sleep import Sleep
from immutable_events import ImmutableEvent

class MainMenu:
    def __init__(self):
        self.width = settings.WIDTH
        self.height = settings.HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(settings.TITLE)

        while True:
            self.update()

    def draw_text(self):
        title = settings.FONT_TITLE.render("Hello World", True, settings.FONT_COLOR)
        self.screen.blit(title, (self.width / 2 - title.get_width() / 2, self.height / 2 - title.get_height() / 2))

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


        pygame.display.update()

if __name__ == "__main__":
    MainMenu()