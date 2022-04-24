# GAME_SETUP
CELL_SIZE = 40
CELL_NUMBER = 20
WIDTH = CELL_SIZE * CELL_NUMBER
HEIGHT = CELL_SIZE * CELL_NUMBER
FPS = 144

CAPTION = 'NeuroSnake v2.100000'

# FONT
FONT_PATH = 'assets/font/Gogh-ExtraBoldItalic.otf'
COLORS = {
    'BASE': '#d7fcd4',
    'HOVER': '#93C54B'
}

# BACKGROUND
BG_MAIN_PATH = 'assets/graphics/main_bg.jpg'
BG_BUTTON_PATH = 'assets/graphics/button_bg.png'

# APPLE
APPLE_PATH = 'assets/graphics/apple.png'


# SNAKE
SNAKE_PATHS = {
    'HEAD': {
        'UP': 'assets/graphics/snake/head_up.png',
        'DOWN': 'assets/graphics/snake/head_down.png',
        'RIGHT': 'assets/graphics/snake/head_right.png',
        'LEFT': 'assets/graphics/snake/head_left.png',
    },
    'BODY': {
        'VERTICAL': 'assets/graphics/snake/body_vertical.png',
        'HORIZONTAL': 'assets/graphics/snake/body_horizontal.png',
        'TR': 'assets/graphics/snake/body_tr.png',
        'TL': 'assets/graphics/snake/body_tl.png',
        'BR': 'assets/graphics/snake/body_br.png',
        'BL': 'assets/graphics/snake/body_bl.png',
    },
    'TAIL': {
        'UP': 'assets/graphics/snake/tail_up.png',
        'DOWN': 'assets/graphics/snake/tail_down.png',
        'RIGHT': 'assets/graphics/snake/tail_right.png',
        'LEFT': 'assets/graphics/snake/tail_left.png',
    }
}

MAX_SPEED = 30

# SOUNDS
CRUNCH_SOUND_PATH = 'assets/sound/crunch.wav'

