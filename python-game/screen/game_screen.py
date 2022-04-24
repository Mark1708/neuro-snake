from config import CELL_NUMBER, CELL_SIZE
from snake_game.fruit import Fruit
from snake_game.snake import Snake


class Game:
    def __init__(self, last_screen, pygame, game_font, apple, brain, connected, disconnected):
        self.screen = last_screen
        self.snake = Snake(pygame)
        self.fruit = Fruit()

        self.is_connected = False
        self.GAME_STATE = 'WAIT'

        self.game_font = game_font
        self.apple = apple
        self.brain = brain
        self.connected = connected
        self.disconnected = disconnected

        self.record = 0
        self.prev_score = 0
        self.score = len(self.snake.body) - 3

    def update(self, pygame, LISTENER):
        self.is_connected = LISTENER.is_connected
        self.snake.move_snake(pygame, LISTENER)
        self.check_collision()
        self.check_fail()

    def draw_elements(self, pygame):
        self.draw_grass(pygame)
        self.fruit.draw_fruit(pygame, self.screen, self.apple)
        self.snake.draw_snake(pygame, self.screen)
        self.draw_score(pygame)
        self.draw_speed(pygame)
        self.draw_is_connected(pygame)

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
        self.score = len(self.snake.body) - 3
        if self.GAME_STATE == 'PLAY':
            self.prev_score = self.score
            if self.record < self.score:
                self.record = self.score
            # Фейл если упираемся в границы карты
            if not (0 <= self.snake.body[0].x < CELL_NUMBER) or not (0 <= self.snake.body[0].y < CELL_NUMBER):
                self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        if self.GAME_STATE == 'PLAY' or self.GAME_STATE == 'GAME_OVER':
            self.GAME_STATE = 'GAME_OVER'
        self.snake.reset()

    def draw_grass(self, pygame):
        # Рисуем поле в клеточку
        grass_color = (167, 209, 61)
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, grass_color, grass_rect)
            else:
                for col in range(CELL_NUMBER):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, grass_color, grass_rect)

    def draw_score(self, pygame):
        score_text = str(len(self.snake.body) - 3)
        score_surface = self.game_font.render(score_text, True, (56, 74, 12))
        score_x = int(CELL_SIZE * CELL_NUMBER - 60)
        score_y = int(CELL_SIZE * CELL_NUMBER - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = self.apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(self.screen, (167, 209, 61), bg_rect)
        self.screen.blit(score_surface, score_rect)
        self.screen.blit(self.apple, apple_rect)
        pygame.draw.rect(self.screen, (56, 74, 12), bg_rect, 2)

    def draw_speed(self, pygame):
        speed_text = str(self.snake.current_speed)
        speed_surface = self.game_font.render(speed_text, True, (56, 74, 12))
        speed_x = int(CELL_SIZE + 60)
        speed_y = int(CELL_SIZE * CELL_NUMBER - 40)
        speed_rect = speed_surface.get_rect(center=(speed_x, speed_y))
        brain_rect = self.brain.get_rect(midright=(speed_rect.left, speed_rect.centery))
        bg_rect = pygame.Rect(brain_rect.left, brain_rect.top, brain_rect.width + speed_rect.width + 6,
                              brain_rect.height)

        pygame.draw.rect(self.screen, (167, 209, 61), bg_rect)
        self.screen.blit(speed_surface, speed_rect)
        self.screen.blit(self.brain, brain_rect)
        pygame.draw.rect(self.screen, (56, 74, 12), bg_rect, 2)

    def draw_is_connected(self, pygame):
        speed_text = 'Connected' if self.is_connected else 'Disconnect'
        speed_surface = self.game_font.render(speed_text, True, (56, 74, 12))
        speed_x = int(CELL_SIZE * CELL_NUMBER / 2)
        speed_y = int(CELL_SIZE * CELL_NUMBER - 40)
        speed_rect = speed_surface.get_rect(center=(speed_x, speed_y))
        if self.is_connected:
            rect = self.connected.get_rect(midright=(speed_rect.left, speed_rect.centery))
            bg_rect = pygame.Rect(rect.left, rect.top, rect.width + speed_rect.width + 6,
                                  rect.height)

            pygame.draw.rect(self.screen, (167, 209, 61), bg_rect)
            self.screen.blit(speed_surface, speed_rect)
            self.screen.blit(self.connected, rect)
            pygame.draw.rect(self.screen, (56, 74, 12), bg_rect, 2)
        else:
            rect = self.disconnected.get_rect(midright=(speed_rect.left, speed_rect.centery))
            bg_rect = pygame.Rect(rect.left, rect.top, rect.width + speed_rect.width + 6,
                                  rect.height)

            pygame.draw.rect(self.screen, (167, 209, 61), bg_rect)
            self.screen.blit(speed_surface, speed_rect)
            self.screen.blit(self.disconnected, rect)
            pygame.draw.rect(self.screen, (56, 74, 12), bg_rect, 2)
