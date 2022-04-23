class KeyboardEvent:
    def __init__(self, py_event, py_game):
        self.py_game = py_game
        self.py_event = py_event

    def is_left(self):
        return self.py_event.key == self.py_game.K_LEFT or self.py_event.key == self.py_game.K_a

    def is_right(self):
        return self.py_event.key == self.py_game.K_RIGHT or self.py_event.key == self.py_game.K_d

    def is_up(self):
        return self.py_event.key == self.py_game.K_UP or self.py_event.key == self.py_game.K_w

    def is_down(self):
        return self.py_event.key == self.py_game.K_DOWN or self.py_event.key == self.py_game.K_s