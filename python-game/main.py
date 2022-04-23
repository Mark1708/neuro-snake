import sys

import pygame as pygame
from pygame.math import Vector2

from component.button import Button
from component.input_block import Input
from component.text_block import Text
from config import *
from game_screen import Game
from snake_game.keyboard_event import KeyboardEvent


def get_font(size):
    return pygame.font.Font(FONT_PATH, size)


class Main:
    def __init__(self, last_screen):
        self.snake_record = 0
        self.prev_score = 0

        self.screen = last_screen
        self.BG = pygame.image.load(BG_MAIN_PATH)

        self.MENU_TEXT = Text(pos=(400, 100), text_input="NeuroSnake",
                              font=get_font(100), base_color="#d7fcd4")

        self.PLAY_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 250),
                                  text_input="PLAY", font=get_font(75), base_color=COLORS['BASE'],
                                  hovering_color=COLORS['HOVER'])
        self.OPTIONS_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 400),
                                     text_input="OPTIONS", font=get_font(75), base_color=COLORS['BASE'],
                                     hovering_color=COLORS['HOVER'])
        self.QUIT_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 550),
                                  text_input="QUIT", font=get_font(75), base_color=COLORS['BASE'],
                                  hovering_color=COLORS['HOVER'])
        self.offset = 0
        self.update_button()

        self.text = None
        self.RESULT_TEXT = None
        self.RESULT_RECT = None

    def update_button(self):
        self.PLAY_BUTTON.update(screen, self.offset)
        self.OPTIONS_BUTTON.update(screen, self.offset)
        self.QUIT_BUTTON.update(screen, self.offset)

    def draw(self):
        self.screen.blit(self.BG, (0, 0))
        self.MENU_TEXT.update(screen)
        if self.snake_record == 0:
            self.offset = 0
        else:
            self.offset = 140
            self.text = f'Your record: {str(self.snake_record).center(3)} Last result: {str(self.prev_score).center(3)}'

            self.RESULT_TEXT = Text(pos=(400, 100 + self.offset), text_input=self.text,
                                    font=get_font(40), base_color="#d7fcd4")
            self.RESULT_TEXT.update(screen)
            self.update_button()
        self.update_button()


class Options:

    def __init__(self, last_screen):
        self.screen = last_screen

        self.BACK_BUTTON = Button(image=None, pos=(200, 460),
                                  text_input="BACK", font=get_font(45), base_color='Black',
                                  hovering_color=COLORS['HOVER'])

        self.CONNECT_BUTTON = Button(image=None, pos=(500, 460),
                                     text_input="CONNECT", font=get_font(45), base_color='Black',
                                     hovering_color=COLORS['HOVER'])

        self.port = '/dev/cu.usbmodem1431101'
        self.serial_speed = '115200'

        self.PORT_INPUT = Input(py_game=pygame, pos=(400, 330), text_input=self.port, font=get_font(20),
                                c_active='lightskyblue3', c_passive='lightgrey', default_width=200, height=32)
        self.SERIAL_SPEED_INPUT = Input(py_game=pygame, pos=(400, 375), text_input=self.serial_speed, font=get_font(20),
                                        c_active='lightskyblue3', c_passive='lightgrey', default_width=200, height=32)

        self.OPTIONS_TEXT = Text(pos=(400, 260), text_input="Set up your Arduino",
                                 font=get_font(45), base_color="Black")
        self.PORT_TEXT = Text(pos=(250, 350), text_input="Arduino port: ",
                              font=get_font(35), base_color="Black")
        self.SERIAL_SPEED_TEXT = Text(pos=(250, 390), text_input="Serial speed: ",
                                      font=get_font(35), base_color="Black")

    def draw(self):
        self.OPTIONS_TEXT.update(self.screen)
        self.PORT_TEXT.update(self.screen)
        self.SERIAL_SPEED_TEXT.update(self.screen)

        self.PORT_INPUT.update(pygame, self.screen)
        self.SERIAL_SPEED_INPUT.update(pygame, self.screen)


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    screen = pygame.display.set_mode((HEIGHT, WIDTH))
    pygame.display.set_caption(CAPTION)

    clock = pygame.time.Clock()

    apple = pygame.image.load(APPLE_PATH).convert_alpha()
    game_font = get_font(25)

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, FPS)

    SCREEN_STATE = 'MENU'  # 'GAME' 'OPTIONS'

    MAIN_SCREEN = Main(screen)
    GAME_SCREEN = Game(screen, pygame, game_font, apple)
    OPTIONS_SCREEN = Options(screen)

    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        MAIN_SCREEN.snake_record = GAME_SCREEN.record
        MAIN_SCREEN.prev_score = GAME_SCREEN.prev_score
        if SCREEN_STATE == 'MENU':
            MAIN_SCREEN.draw()
            for button in [MAIN_SCREEN.PLAY_BUTTON, MAIN_SCREEN.OPTIONS_BUTTON, MAIN_SCREEN.QUIT_BUTTON]:
                button.change_color(MOUSE_POS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MAIN_SCREEN.PLAY_BUTTON.check_for_input(MOUSE_POS):
                        SCREEN_STATE = 'GAME'
                        GAME_SCREEN.snake.reset()
                        GAME_SCREEN.GAME_STATE = 'WAIT'
                    if MAIN_SCREEN.OPTIONS_BUTTON.check_for_input(MOUSE_POS):
                        SCREEN_STATE = 'OPTIONS'
                        OPTIONS_SCREEN.draw()
                    if MAIN_SCREEN.QUIT_BUTTON.check_for_input(MOUSE_POS):
                        pygame.quit()
                        sys.exit()
        elif SCREEN_STATE == 'GAME':
            for event in pygame.event.get():
                if event.type == pygame.QUIT or GAME_SCREEN.GAME_STATE == 'GAME_OVER':
                    SCREEN_STATE = 'MENU'
                    MAIN_SCREEN.draw()
                if event.type == SCREEN_UPDATE:
                    GAME_SCREEN.update(pygame)
                if event.type == pygame.KEYDOWN:
                    GAME_SCREEN.GAME_STATE = 'PLAY'
                    key_event = KeyboardEvent(event, pygame)
                    if key_event.is_up() and GAME_SCREEN.snake.direction.y != 1:
                        GAME_SCREEN.snake.direction = Vector2(0, -1)
                    if key_event.is_right() and GAME_SCREEN.snake.direction.x != -1:
                        GAME_SCREEN.snake.direction = Vector2(1, 0)
                    if key_event.is_down() and GAME_SCREEN.snake.direction.y != -1:
                        GAME_SCREEN.snake.direction = Vector2(0, 1)
                    if key_event.is_left() and GAME_SCREEN.snake.direction.x != 1:
                        GAME_SCREEN.snake.direction = Vector2(-1, 0)

            screen.fill((175, 215, 70))
            GAME_SCREEN.draw_elements(pygame)
        elif SCREEN_STATE == 'OPTIONS':
            screen.fill("white")
            for button in [OPTIONS_SCREEN.CONNECT_BUTTON, OPTIONS_SCREEN.BACK_BUTTON]:
                button.change_color(MOUSE_POS)
                button.update(screen)

            OPTIONS_SCREEN.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    OPTIONS_SCREEN.PORT_INPUT.change_color(MOUSE_POS)
                    OPTIONS_SCREEN.SERIAL_SPEED_INPUT.change_color(MOUSE_POS)

                    if OPTIONS_SCREEN.BACK_BUTTON.check_for_input(MOUSE_POS):
                        SCREEN_STATE = 'MENU'
                    if OPTIONS_SCREEN.CONNECT_BUTTON.check_for_input(MOUSE_POS):
                        print('Connection')
                if event.type == pygame.KEYDOWN:
                    OPTIONS_SCREEN.PORT_INPUT.check_for_input(event, pygame)
                    OPTIONS_SCREEN.SERIAL_SPEED_INPUT.check_for_input(event, pygame)

        pygame.display.update()
        clock.tick(FPS)
