import sys
import random
import time

import pygame as pygame
from pygame.math import Vector2

from component.button import Button
from config import *


def get_font(size):
    return pygame.font.Font(FONT_PATH, size)


def is_left(event):
    return event.key == pygame.K_LEFT or event.key == pygame.K_a


def is_right(event):
    return event.key == pygame.K_RIGHT or event.key == pygame.K_d


def is_up(event):
    return event.key == pygame.K_UP or event.key == pygame.K_w


def is_down(event):
    return event.key == pygame.K_DOWN or event.key == pygame.K_s


class Main:
    def __init__(self, SCREEN):
        self.snake_record = 0
        self.prev_score = 0

        self.SCREEN = SCREEN
        self.BG = pygame.image.load(BG_MAIN_PATH)
        self.MENU_TEXT = get_font(100).render("NeuroSnake", True, "#d7fcd4")
        self.MENU_RECT = self.MENU_TEXT.get_rect(center=(400, 100))

        # if self.snake_record == 0:
        self.offset = 0
        # else:
        #     print(self.snake_record)
        #     self.RESULT_TEXT = get_font(50).render(str(self.snake_record), True, "#d7fcd4")
        #     self.offset = 150
        #     self.MENU_RECT = self.MENU_TEXT.get_rect(center=(400, 100 + self.offset))
        self.update_button()
        # self.PLAY_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 250 + self.offset),
        #                           text_input="PLAY", font=get_font(75), base_color=COLORS['BASE'],
        #                           hovering_color=COLORS['HOVER'])
        # self.OPTIONS_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 400 + self.offset),
        #                              text_input="OPTIONS", font=get_font(75), base_color=COLORS['BASE'],
        #                              hovering_color=COLORS['HOVER'])
        # self.QUIT_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 550 + self.offset),
        #                           text_input="QUIT", font=get_font(75), base_color=COLORS['BASE'],
        #                           hovering_color=COLORS['HOVER'])

    def update_button(self):
        self.PLAY_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 250 + self.offset),
                                  text_input="PLAY", font=get_font(75), base_color=COLORS['BASE'],
                                  hovering_color=COLORS['HOVER'])
        self.OPTIONS_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 400 + self.offset),
                                     text_input="OPTIONS", font=get_font(75), base_color=COLORS['BASE'],
                                     hovering_color=COLORS['HOVER'])
        self.QUIT_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 550 + self.offset),
                                  text_input="QUIT", font=get_font(75), base_color=COLORS['BASE'],
                                  hovering_color=COLORS['HOVER'])

    def draw(self):
        self.SCREEN.blit(self.BG, (0, 0))
        # self.MENU_TEXT = get_font(100).render("NeuroSnake", True, "#d7fcd4")
        # self.MENU_RECT = self.MENU_TEXT.get_rect(center=(400, 100))
        #
        # self.PLAY_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 250),
        #                           text_input="PLAY", font=get_font(75), base_color=COLORS['BASE'],
        #                           hovering_color=COLORS['HOVER'])
        # self.OPTIONS_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 400),
        #                              text_input="OPTIONS", font=get_font(75), base_color=COLORS['BASE'],
        #                              hovering_color=COLORS['HOVER'])
        # self.QUIT_BUTTON = Button(image=pygame.image.load(BG_BUTTON_PATH), pos=(400, 550),
        #                           text_input="QUIT", font=get_font(75), base_color=COLORS['BASE'],
        #                           hovering_color=COLORS['HOVER'])
        self.SCREEN.blit(self.MENU_TEXT, self.MENU_RECT)

        if self.snake_record == 0:
            self.offset = 0
        else:
            # print(self.snake_record)
            self.offset = 150
            self.text = f'Your record: {str(self.snake_record).center(3)}   Last result: {str(self.prev_score).center(3)}'
            self.RESULT_TEXT = get_font(40).render(self.text, True, "#d7fcd4")
            self.RESULT_RECT = self.MENU_TEXT.get_rect(center=(400, 100 + self.offset))
            self.SCREEN.blit(self.RESULT_TEXT, self.RESULT_RECT)
            # self.LAST_RESULT_TEXT = get_font(50).render(f'Last result: {str(self.prev_score)}', True, "#d7fcd4")
            # self.LAST_RESULT_RECT = self.MENU_TEXT.get_rect(center=(400, 150 + self.offset))
            # self.SCREEN.blit(self.LAST_RESULT_TEXT, self.LAST_RESULT_RECT)
            self.update_button()


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.change_move_time = 0

        # Голова
        self.head_up = pygame.image.load(SNAKE_PATHS['HEAD']['UP']).convert_alpha()
        self.head_down = pygame.image.load(SNAKE_PATHS['HEAD']['DOWN']).convert_alpha()
        self.head_right = pygame.image.load(SNAKE_PATHS['HEAD']['RIGHT']).convert_alpha()
        self.head_left = pygame.image.load(SNAKE_PATHS['HEAD']['LEFT']).convert_alpha()

        # Основные сегменты змейки
        self.body_vertical = pygame.image.load(SNAKE_PATHS['BODY']['VERTICAL']).convert_alpha()
        self.body_horizontal = pygame.image.load(SNAKE_PATHS['BODY']['HORIZONTAL']).convert_alpha()

        # Хвост
        self.tail_up = pygame.image.load(SNAKE_PATHS['TAIL']['UP']).convert_alpha()
        self.tail_down = pygame.image.load(SNAKE_PATHS['TAIL']['DOWN']).convert_alpha()
        self.tail_right = pygame.image.load(SNAKE_PATHS['TAIL']['RIGHT']).convert_alpha()
        self.tail_left = pygame.image.load(SNAKE_PATHS['TAIL']['LEFT']).convert_alpha()

        # Изгибы при повороте
        self.body_tr = pygame.image.load(SNAKE_PATHS['BODY']['TR']).convert_alpha()
        self.body_tl = pygame.image.load(SNAKE_PATHS['BODY']['TL']).convert_alpha()
        self.body_br = pygame.image.load(SNAKE_PATHS['BODY']['BR']).convert_alpha()
        self.body_bl = pygame.image.load(SNAKE_PATHS['BODY']['BL']).convert_alpha()

        # Звук поедания яблок
        self.crunch_sound = pygame.mixer.Sound(CRUNCH_SOUND_PATH)

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if index == 0:
                # Рисуем голову
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                # Рисуем хвост
                screen.blit(self.tail, block_rect)
            else:
                # Рисуем тело
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    # Вертикальное движение
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    # Горизонтальное движение
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        # Поворот вниз-влево
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        # Поворот вправо-вниз
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        # Поворот влево-вверх
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        # Поворот вверх-вправо
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]

        if head_relation == Vector2(1, 0):  # Влево
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):  # Впрво
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):  # Вверх
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):  # Вниз
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]

        if tail_relation == Vector2(1, 0):  # Впрво
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):  # Влево
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):  # Вниз
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):  # Вверх
            self.tail = self.tail_down

    def move_snake(self):
        self.current_speed = 20
        self.current_time = pygame.time.get_ticks()
        if self.current_time > self.change_move_time:
            self.change_move_time = self.current_time + 1000 / (MAX_SPEED - self.current_speed)
            if self.new_block == True:
                # Движение змейки со сдвигом при увеличении длины
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]
                self.new_block = False
            else:
                # Обычное движение змейки
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]

    # Добвляем блок для змейки
    def add_block(self):
        self.new_block = True

    # Звук во время поедания яблока
    def play_crunch_sound(self):
        self.crunch_sound.play()

    # Дефолтное положение
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class Fruit:
    def __init__(self):
        self.randomize()
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        # Рисуем фрукт
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        # Рандомное положение
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


class Game:
    def __init__(self, screen):
        self.record = 0
        self.prev_score = 0
        self.SCREEN = screen
        self.snake = Snake()
        self.fruit = Fruit()
        self.GAME_STATE = 'WAIT'

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.GAME_STATE == 'PLAY':
            # Змея скушала яблоко
            if self.fruit.pos == self.snake.body[0]:
                self.fruit.randomize()
                self.snake.add_block()
                self.snake.play_crunch_sound()
            # Если фрукт сгенерировался в теле змейки, меняем положение
            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()

    def check_fail(self):
        # print(self.GAME_STATE)
        self.score = len(self.snake.body) - 3
        if self.GAME_STATE == 'PLAY':
            self.prev_score = self.score
            if self.record < self.score:
                self.record = self.score
            # Фейл если упираемся в границы карты
            if not (0 <= self.snake.body[0].x < CELL_NUMBER) or not (0 <= self.snake.body[0].y < CELL_NUMBER):
                print(f'0 <= {self.snake.body[0].x} < {CELL_NUMBER}')
                print(f'0 <= {self.snake.body[0].y} < {CELL_NUMBER}')
                self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                if self.GAME_STATE == 'PLAY':
                    print(f'fail2 {block} {self.snake.body[0]}')
                self.game_over()

    def game_over(self):
        # print('game_over')
        if self.GAME_STATE == 'PLAY' or self.GAME_STATE == 'GAME_OVER':
            # score_surface = game_font.render('Your score is ' + str(len(self.snake.body) - 3), True, (56, 74, 12))
            # score_rect = score_surface.get_rect(center=(400, 400))
            # self.SCREEN.blit(score_surface, score_rect)
            # time.sleep(4)
            self.GAME_STATE = 'GAME_OVER'
        self.snake.reset()

    def draw_grass(self):
        # Рисуем поле в клеточку
        grass_color = (167, 209, 61)
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.SCREEN, grass_color, grass_rect)
            else:
                for col in range(CELL_NUMBER):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.SCREEN, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(CELL_SIZE * CELL_NUMBER - 60)
        score_y = int(CELL_SIZE * CELL_NUMBER - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(self.SCREEN, (167, 209, 61), bg_rect)
        self.SCREEN.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)


class Options:

    def __init__(self, screen):
        self.screen = screen

        self.OPTIONS_TEXT = get_font(45).render("Set up your Arduino", True, "Black")
        self.OPTIONS_RECT = self.OPTIONS_TEXT.get_rect(center=(400, 260))
        self.BACK_BUTTON = Button(image=None, pos=(200, 460),
                                  text_input="BACK", font=get_font(45), base_color='Black',
                                  hovering_color=COLORS['HOVER'])

        self.CONNECT_BUTTON = Button(image=None, pos=(500, 460),
                                     text_input="CONNECT", font=get_font(45), base_color='Black',
                                     hovering_color=COLORS['HOVER'])
        # self.OPTIONS_BACK = Button(image=None, pos=(400, 460),
        #                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        self.port = '/dev/cu.usbmodem1431101'
        self.baudrate = '115200'

        # create rectangle
        self.port_rect = pygame.Rect(400, 330, 140, 32)
        self.baudrate_rect = pygame.Rect(400, 365, 140, 32)

        # color_active stores color(lightskyblue3) which
        # gets active when input box is clicked by user
        self.color_active = pygame.Color('lightskyblue3')

        # color_passive store color(chartreuse4) which is
        # color of input box.
        self.color_passive = pygame.Color('lightgrey')
        self.color_port = self.color_passive
        self.color_baudrate = self.color_passive

        self.active_port = False
        self.active_baudrate = False

        self.PORT_TEXT = get_font(35).render("Arduino port: ", True, "Black")
        self.PORT_RECT = self.OPTIONS_TEXT.get_rect(center=(350, 350))
        self.BAUDRATE_TEXT = get_font(35).render("Baudrate: ", True, "Black")
        self.BAUDRATE_RECT = self.OPTIONS_TEXT.get_rect(center=(350, 390))

    def draw(self):
        self.screen.blit(self.OPTIONS_TEXT, self.OPTIONS_RECT)
        self.screen.blit(self.PORT_TEXT, self.PORT_RECT)
        self.screen.blit(self.BAUDRATE_TEXT, self.BAUDRATE_RECT)

        if self.active_port:
            self.color_port = self.color_active
        else:
            self.color_port = self.color_passive

        if self.active_baudrate:
            self.color_baudrate = self.color_active
        else:
            self.color_baudrate = self.color_passive

            # draw rectangle and argument passed which should
            # be on screen
        pygame.draw.rect(self.screen, self.color_port, self.port_rect)
        pygame.draw.rect(self.screen, self.color_baudrate, self.baudrate_rect)

        self.text_surface = get_font(20).render(self.port, True, 'Black')
        self.text_surface_baudrate = get_font(20).render(self.baudrate, True, 'Black')

        # render at position stated in arguments
        self.screen.blit(self.text_surface, (self.port_rect.x + 5, self.port_rect.y + 5))
        self.screen.blit(self.text_surface_baudrate, (self.baudrate_rect.x + 5, self.baudrate_rect.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        self.port_rect.w = max(200, self.text_surface.get_width() + 10)
        self.baudrate_rect.w = max(200, self.text_surface_baudrate.get_width() + 10)


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
    GAME_SCREEN = Game(screen)
    OPTIONS_SCREEN = Options(screen)

    # snake_record = 0

    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        MAIN_SCREEN.snake_record = GAME_SCREEN.record
        MAIN_SCREEN.prev_score = GAME_SCREEN.prev_score
        if SCREEN_STATE == 'MENU':
            MAIN_SCREEN.draw()
            for button in [MAIN_SCREEN.PLAY_BUTTON, MAIN_SCREEN.OPTIONS_BUTTON, MAIN_SCREEN.QUIT_BUTTON]:
                button.change_color(MOUSE_POS)
                button.update(screen)

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
                    GAME_SCREEN.update()
                if event.type == pygame.KEYDOWN:
                    GAME_SCREEN.GAME_STATE = 'PLAY'
                    if is_up(event) and GAME_SCREEN.snake.direction.y != 1:
                        GAME_SCREEN.snake.direction = Vector2(0, -1)
                    if is_right(event) and GAME_SCREEN.snake.direction.x != -1:
                        GAME_SCREEN.snake.direction = Vector2(1, 0)
                    if is_down(event) and GAME_SCREEN.snake.direction.y != -1:
                        GAME_SCREEN.snake.direction = Vector2(0, 1)
                    if is_left(event) and GAME_SCREEN.snake.direction.x != 1:
                        GAME_SCREEN.snake.direction = Vector2(-1, 0)

            screen.fill((175, 215, 70))
            GAME_SCREEN.draw_elements()
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
                    if OPTIONS_SCREEN.port_rect.collidepoint(MOUSE_POS):
                        OPTIONS_SCREEN.active = True
                    else:
                        OPTIONS_SCREEN.active = False

                    if OPTIONS_SCREEN.BACK_BUTTON.check_for_input(MOUSE_POS):
                        SCREEN_STATE = 'MENU'
                    if OPTIONS_SCREEN.CONNECT_BUTTON.check_for_input(MOUSE_POS):
                        print('Connection')
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        OPTIONS_SCREEN.port = OPTIONS_SCREEN.port[:-1]
                    else:
                        OPTIONS_SCREEN.port += event.unicode

        pygame.display.update()
        clock.tick(FPS)
