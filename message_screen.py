import pygame, sys, os


class TypingTextScreen:
    def __init__(self, width, height, text, font_size=24, color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.text_surface = pygame.Surface((self.width, self.height))
        self.text_rect = self.text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.timer = 0
        self.text_index = 0
        self.typing_complete = False  # New attribute to track typing completion
        self.play_music('./Assets/midi/Crazy-Train.mp3')

    def play_music(self, music_file):
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)
            
    def stop_music(self):
        pygame.mixer.music.stop()

    def run(self, screen, delta_time):
        screen.fill((0, 0, 0))  # Background color (black in this case)

        # Display the typed text with line breaks
        typed_lines = self.text[:self.text_index].split('\n')
        line_height = self.font_size + 2  # Adjust the line height as needed
        start_x, start_y = 20, 30

        for i, line in enumerate(typed_lines):
            text_render = self.font.render(line, True, self.color)
            text_rect = text_render.get_rect(topleft=(start_x, start_y + i * line_height))

            self.text_surface.blit(text_render, text_rect)

        screen.blit(self.text_surface, self.text_rect)

        # Update the text index based on time
        self.timer += delta_time
        if self.timer >= 0.05:  # Adjust the typing speed as needed
            self.timer = 0
            self.text_index += 1

        # Check if the text is fully typed
        if self.text_index >= len(self.text):
            self.typing_complete = True

    def is_typing_complete(self):
        return self.typing_complete

class GameOver:
    def __init__(self, width, height, font_size=36, color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.lines = ["Game Over", "Press 'A' to try again"]
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

class StartScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = pygame.image.load('./Assets/backgrounds/start.jpg').convert_alpha()
        self.image_rect = self.image.get_rect(center=(self.width // 2, self.height // 2))

        # Define vertical offset for text positions
        text_offset = 256

        # Define rectangles for the text with the offset
        self.game_start_rect = pygame.Rect(self.width // 2 - 100, self.height // 2 - 50 + text_offset, 200, 30)
        self.index_rect = pygame.Rect(self.width // 2 - 50, self.height // 2 + 20 + text_offset, 100, 30)

        # Define fonts and render text surfaces
        font = pygame.font.SysFont("Arial", 24)
        self.game_start_text = font.render("Game Start", True, (255, 255, 255))
        self.index_text = font.render("Index", True, (255, 255, 255))

        # Define images for the selected state
        self.game_start_image = pygame.image.load('./Assets/power_ups/back_up/3.png').convert_alpha()
        self.index_image = pygame.image.load('./Assets/power_ups/back_up/3.png').convert_alpha()

        # Selection state
        self.selected_option = "Game Start"

        # cooldown
        self.click_timer = 0
        self.click_cooldown = 1000

        # Load the index image
        self.index_image = pygame.image.load('./Assets/backgrounds/index.jpeg').convert_alpha()
        self.index_image = pygame.transform.scale(self.index_image, (width, height))

        # New attribute to track if the index image is currently displayed
        self.index_image_displayed = False

    def handle_input(self, level, typing_screen):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Change the selected option based on user input
        if keys[pygame.K_UP]:
            self.selected_option = "Game Start"
        elif keys[pygame.K_DOWN]:
            self.selected_option = "Index"

        # Trigger actions when a button is pressed
        if keys[pygame.K_RETURN]:
            if self.selected_option == "Game Start":
                if current_time - self.click_timer >= self.click_cooldown:
                    if not level.started and level.start_text:
                        level.started = True
                        level.start_text = False
                        typing_screen.stop_music()
                        level.play_music()
                    if not level.start_text and not level.started:
                        level.start_text = True
                    self.click_timer = current_time
            elif self.selected_option == "Index":
                if current_time - self.click_timer >= self.click_cooldown:
                    if not self.index_image_displayed:
                        # Display the full-screen image for "Index"
                        self.index_image_displayed = True
                    else:
                        # If the image is already displayed, go back to the start screen
                        self.index_image_displayed = False
                    self.click_timer = current_time

    def run(self, screen):
        screen.fill((0, 0, 0))  # Background color (black in this case)
        screen.blit(self.image, self.image_rect)

        # Blit the text for both options
        screen.blit(self.game_start_text, self.game_start_rect.topleft)
        screen.blit(self.index_text, self.index_rect.topleft)

        # Blit the image only for the selected option
        if self.selected_option == "Game Start":
            screen.blit(self.game_start_image, (self.game_start_rect.left - 52, self.game_start_rect.top))
        elif self.selected_option == "Index":
            if self.index_image_displayed:
                # Display the full-screen image for "Index"
                screen.blit(self.index_image, (0, 0))
            else:
                screen.blit(self.index_text, self.index_rect.topleft)
                screen.blit(self.game_start_image, (self.index_rect.left - 52, self.index_rect.top))

class PauseScreen:
    def __init__(self, screen_width, screen_height, overlay_alpha=3):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.overlay_alpha = overlay_alpha
        self.overlay_color = (0, 0, 0, self.overlay_alpha)  # Add alpha to the color for transparency

        self.paused_text = pygame.font.SysFont("Arial", 60).render("PAUSED", True, (255, 255, 255))
        self.fullscreen_image = pygame.image.load('./Assets/backgrounds/index.jpeg')  # Add the path to your image
        self.fullscreen_image = pygame.transform.scale(self.fullscreen_image, (self.screen_width, self.screen_height))
        self.additional_text = pygame.font.SysFont("Arial", 30).render("Press C for index.", True, (255, 255, 255))

    def display(self, screen, show_fullscreen_image=False):
        # Dim the screen with a semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill(self.overlay_color)
        screen.blit(overlay, (0, 0))

        # Display additional text during the fading process
        additional_text_rect = self.additional_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        screen.blit(self.additional_text, additional_text_rect)

        # Display the "PAUSED" text at the center of the screen
        text_rect = self.paused_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(self.paused_text, text_rect)

        # Check if the full-screen image should be displayed
        if show_fullscreen_image:
            # Display the resized full-screen image
            image_rect = self.fullscreen_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(self.fullscreen_image, image_rect)

