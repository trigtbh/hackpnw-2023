import os
# disable pygame boot message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import settings


class MainWindow:
    def __init__(self):
        self.width = settings.WIDTH
        self.height = settings.HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.events = []

        self.y = 0
        self.drag = False

        while True:
            self.update()

    def draw_events(self):
        ...

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
        # draw the time labels on the left side of the grid
        # display text vertically in the space between the lines
        # start at midnight, end at midnight the next day
        # draw all the text on their own lines
        # center the text in the leftmost column
        for i in range(0, 48):
            text = settings.FONT.render(f"{i // 2}:{'00' if i % 2 == 0 else '30'}", True, settings.FONT_COLOR)
            self.window.blit(text, (self.width / 16 - text.get_width() / 2, self.height * settings.WHITE_SPACE + self.height * (1 - 2 * settings.WHITE_SPACE) * i / 12 - self.y - text.get_height() / 2))
        
    def draw_bars(self):
        # draw rectangles to cover up lines at top and bottom
        pygame.draw.rect(self.window, settings.BACKGROUND, (0, 0, self.width, self.height * settings.WHITE_SPACE))
        pygame.draw.rect(self.window, settings.BACKGROUND, (0, self.height * (1 - settings.WHITE_SPACE), self.width, self.height * settings.WHITE_SPACE))
        
        # draw lines at top and bottom to separate the grid from the rest of the window
        pygame.draw.line(self.window, settings.COLUMN_LINES, (0, self.height * settings.WHITE_SPACE), (self.width, self.height * settings.WHITE_SPACE), 1)
        pygame.draw.line(self.window, settings.COLUMN_LINES, (0, self.height * (1 - settings.WHITE_SPACE)), (self.width, self.height * (1 - settings.WHITE_SPACE)), 1)

    def draw_day_names(self):
        # draw names up at the top of the grid
        # center names in their respective columns
        # start on second column
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i in range(0, 7):
            text = settings.FONT.render(days[i], True, settings.FONT_COLOR)
            self.window.blit(text, (self.width * (i + 1) / 8 - text.get_width() / 2, self.height * settings.WHITE_SPACE / 2 - text.get_height() / 2))

    def update(self):
        self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.VIDEORESIZE:
                self.window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.width = event.w
                self.height = event.h

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

            
            
        self.window.fill(settings.BACKGROUND)
        self.draw_grid()
        self.draw_bars()
        self.draw_day_names()
        self.draw_time()
        pygame.display.update()


if __name__ == "__main__":
    MainWindow()
