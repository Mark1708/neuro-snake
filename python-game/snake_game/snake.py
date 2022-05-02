from pygame.math import Vector2

from config import MAX_SPEED, SNAKE_PATHS, CRUNCH_SOUND_PATH, CELL_SIZE
from service.data_service import DataService


class Snake:
    def __init__(self, pygame):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.change_move_time = 0

        self.current_speed = 161
        self.current_time = 0

        self.data_service = DataService()

        self.head = None
        self.tail = None

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

    def draw_snake(self, pygame, screen):
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

    def move_snake(self, pygame, LISTENER):
        self.current_speed = LISTENER.read_data()
        if LISTENER.is_connected:
            if self.data_service.state == 'CREATE':
                self.data_service.start_writing(self.current_speed)
            else:
                self.data_service.write_data(self.current_speed)

        self.current_time = pygame.time.get_ticks()
        if self.current_time > self.change_move_time:
            self.change_move_time = self.current_time + 10000 / (MAX_SPEED - self.current_speed)
            if self.new_block:
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
