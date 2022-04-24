from component.button import Button
from component.text_block import Text
from config import BG_BUTTON_PATH, COLORS, BG_MAIN_PATH


class Main:
    def __init__(self, last_screen, pygame, menu_font, result_font, button_font):
        self.snake_record = 0
        self.prev_score = 0

        self.menu_font = menu_font
        self.result_font = result_font
        self.button_font = button_font

        self.screen = last_screen
        self.BG = pygame.image.load(BG_MAIN_PATH)

        self.MENU_TEXT = Text(pos=(400, 100), text_input="NeuroSnake",
                              font=self.menu_font, base_color="#d7fcd4")

        self.PLAY_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 250),
                                  text_input="PLAY", font=self.button_font, base_color=COLORS['BASE'],
                                  hovering_color=COLORS['HOVER'])
        self.OPTIONS_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 400),
                                     text_input="OPTIONS", font=self.button_font, base_color=COLORS['BASE'],
                                     hovering_color=COLORS['HOVER'])
        self.QUIT_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 550),
                                  text_input="QUIT", font=self.button_font, base_color=COLORS['BASE'],
                                  hovering_color=COLORS['HOVER'])
        self.offset = 0
        self.update_button()

        self.text = None
        self.RESULT_TEXT = None
        self.RESULT_RECT = None

    def update_button(self):
        self.PLAY_BUTTON.update(self.screen, self.offset)
        self.OPTIONS_BUTTON.update(self.screen, self.offset)
        self.QUIT_BUTTON.update(self.screen, self.offset)

    def draw(self):
        self.screen.blit(self.BG, (0, 0))
        self.MENU_TEXT.update(self.screen)
        if self.snake_record == 0:
            self.offset = 0
        else:
            self.offset = 140
            self.text = f'Your record: {str(self.snake_record).center(3)} Last result: {str(self.prev_score).center(3)}'

            self.RESULT_TEXT = Text(pos=(400, 100 + self.offset), text_input=self.text,
                                    font=self.result_font, base_color="#d7fcd4")
            self.RESULT_TEXT.update(self.screen)
            self.update_button()
        self.update_button()
