import pygame
pygame.font.init()

WIDTH = 864
HEIGHT = 600

TITLE = "test"

WHITE_SPACE = 0.05

# open tt norms pro regular font and load it into pygame as a custom font
FONT_MEDIUM = pygame.font.Font("TT Norms Pro Regular.otf", 20)
FONT_A_BIT_SMALLER = pygame.font.Font("TT Norms Pro Regular.otf", 18)
FONT_LARGE = pygame.font.Font("TT Norms Pro Regular.otf", 30)
FONT_SMALL = pygame.font.Font("TT Norms Pro Regular.otf", 15)
FONT_TITLE = pygame.font.Font("TT Norms Pro Bold.otf", 50)
FONT = FONT_MEDIUM


# colors
BACKGROUND = (255, 255, 255)
COLUMN_LINES = (68, 73, 110)
ROW_LINES = (68, 73, 110)
FONT_COLOR = (240, 240, 240)

PINK = (232, 142, 237)
BLUE = (102, 199, 244)
ORANGE = (255, 151, 112)
DARK_BLUE = (45, 48, 71)
LIME = (144, 233, 58)
LIGHTER_DARK_BLUE = (55, 58, 87)

BACKGROUND = DARK_BLUE