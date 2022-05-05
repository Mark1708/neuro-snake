import sys

import pygame as pygame
from pygame.math import Vector2

import math
from config import *
from screen.game_screen import Game
from screen.menu_screen import Main
from screen.arduino_options_screen import ArduinoOptions
from service.com_listener import Listener
from service.keyboard_event import KeyboardEvent


def get_font(size):
    return pygame.font.Font(FONT_PATH, size)


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    screen = pygame.display.set_mode((HEIGHT, WIDTH))
    pygame.display.set_caption(CAPTION)

    clock = pygame.time.Clock()

    apple = pygame.image.load(APPLE_PATH).convert_alpha()
    brain = pygame.image.load(BRAIN_PATH).convert_alpha()
    connected = pygame.image.load(CONNECT_PATH).convert_alpha()
    disconnected = pygame.image.load(DISCONNECT_PATH).convert_alpha()

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, FPS)

    SCREEN_STATE = 'MENU'  # 'GAME' 'OPTIONS'

    MAIN_SCREEN = Main(screen, pygame, get_font(100), get_font(40), get_font(75))
    GAME_SCREEN = Game(screen, pygame, get_font(25), apple, brain, connected, disconnected)
    OPTIONS_SCREEN = ArduinoOptions(screen, pygame, get_font(45), get_font(20), get_font(35))

    LISTENER = Listener()

    while True:
        # print('RUNNING')
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
                        GAME_SCREEN.snake.data_service.state = 'CREATE'
                        GAME_SCREEN.snake.reset()
                        GAME_SCREEN.GAME_STATE = 'WAIT'
                    if MAIN_SCREEN.OPTIONS_BUTTON.check_for_input(MOUSE_POS):
                        SCREEN_STATE = 'OPTIONS'
                        OPTIONS_SCREEN.draw(pygame)
                    if MAIN_SCREEN.QUIT_BUTTON.check_for_input(MOUSE_POS):
                        pygame.quit()
                        sys.exit()
        elif SCREEN_STATE == 'GAME':
            for event in pygame.event.get():
                if event.type == pygame.QUIT or GAME_SCREEN.GAME_STATE == 'GAME_OVER':
                    SCREEN_STATE = 'MENU'
                    MAIN_SCREEN.draw()
                if event.type == SCREEN_UPDATE:
                    GAME_SCREEN.update(pygame, LISTENER)
                if event.type == pygame.KEYDOWN:
                    GAME_SCREEN.GAME_STATE = 'PLAY'
                    key_event = KeyboardEvent(event, pygame)
                    if event.type == pygame.KEYDOWN:
                        GAME_SCREEN.GAME_STATE = 'PLAY'
                        key_event = KeyboardEvent(event, pygame)
                        if key_event.is_up() and GAME_SCREEN.snake.direction.y != 1:
                            GAME_SCREEN.snake.direction = Vector2(0, -1)
                        elif key_event.is_right() and GAME_SCREEN.snake.direction.x != -1:
                            GAME_SCREEN.snake.direction = Vector2(1, 0)
                        elif key_event.is_down() and GAME_SCREEN.snake.direction.y != -1:
                            GAME_SCREEN.snake.direction = Vector2(0, 1)
                        elif key_event.is_left() and GAME_SCREEN.snake.direction.x != 1:
                            GAME_SCREEN.snake.direction = Vector2(-1, 0)
            screen.fill((175, 215, 70))
            GAME_SCREEN.draw_elements(pygame)
        elif SCREEN_STATE == 'OPTIONS':
            screen.fill("white")
            for button in [OPTIONS_SCREEN.CONNECT_BUTTON, OPTIONS_SCREEN.BACK_BUTTON]:
                button.change_color(MOUSE_POS)
                button.update(screen)

            OPTIONS_SCREEN.draw(pygame)
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
                        if LISTENER.is_connected:
                            LISTENER.is_connected = False
                        else:
                            LISTENER.connection(
                                OPTIONS_SCREEN.PORT_INPUT.text_input,
                                OPTIONS_SCREEN.SERIAL_SPEED_INPUT.text_input
                            )
                        OPTIONS_SCREEN.update_connect_button(LISTENER.is_connected)
                if event.type == pygame.KEYDOWN:
                    if OPTIONS_SCREEN.PORT_INPUT.active:
                        OPTIONS_SCREEN.PORT_INPUT.check_for_input(event, pygame)

                    if OPTIONS_SCREEN.SERIAL_SPEED_INPUT.active:
                        OPTIONS_SCREEN.SERIAL_SPEED_INPUT.check_for_input(event, pygame)

        pygame.display.update()
        clock.tick(FPS)
