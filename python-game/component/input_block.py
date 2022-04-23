class Input:
    def __init__(self, py_game, pos, text_input, font, c_active, c_passive, default_width=100, height=40, font_color='Black'):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.color_active, self.color_passive = py_game.Color(c_active), py_game.Color(c_passive)
        self.color = self.color_passive
        self.active = False
        self.text_input = text_input
        self.input_rect = py_game.Rect(self.x_pos, self.y_pos, default_width, height)
        self.default_width = default_width
        self.height = height
        self.font_color = font_color

    def update(self, py_game, prev_screen):
        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_passive

        py_game.draw.rect(prev_screen, self.color, self.input_rect)

        surface = self.font.render(self.text_input, True, self.font_color)

        prev_screen.blit(surface, (self.input_rect.x + 5, self.input_rect.y + (self.height - self.font.get_height()) / 2))

        self.input_rect.w = max(self.default_width, surface.get_width() + 10)

    def change_color(self, position):
        if self.input_rect.collidepoint(position):
            self.active = True
        else:
            self.active = False

    def check_for_input(self, py_event,  py_game):
        if py_event.key == py_game.K_BACKSPACE:
            self.text_input = self.text_input[:-1]
        else:
            self.text_input += py_event.unicode
