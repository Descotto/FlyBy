import pygame

class GameOver:
    def __init__(self, width, height, font_size=36, color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.lines = ["Game Over", "Press 'A' to restart"]
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(None, self.font_size)
        self.text_surfaces = [self.font.render(str(line), True, self.color) for line in self.lines]

        # Calculate the total height occupied by text surfaces
        total_text_height = sum(surface.get_height() for surface in self.text_surfaces)

        # Calculate the starting y-position to center the text vertically
        start_y = (self.height - total_text_height) // 2

        # Calculate the rect positions for each text surface
        self.text_rects = [surface.get_rect(center=(self.width // 2, start_y + sum(surface.get_height() for surface in self.text_surfaces[:i]))) for i, surface in enumerate(self.text_surfaces)]

    def run(self, screen):
        screen.fill((0, 0, 0))  # Background color (black in this case)
        for text_surface, text_rect in zip(self.text_surfaces, self.text_rects):
            screen.blit(text_surface, text_rect)
