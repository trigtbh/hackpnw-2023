def draw_bars(self):
        # draw rectangles to cover up lines at top and bottom
        pygame.draw.rect(self.window, settings.BACKGROUND, (0, 0, self.width, self.height * settings.WHITE_SPACE))
        