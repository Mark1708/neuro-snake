from component.button import Button
from component.input_block import Input
from component.text_block import Text
from config import COLORS


class ArduinoOptions:

    def __init__(self, last_screen, py_game, button_font, input_font, param_font):
        self.screen = last_screen

        self.BACK_BUTTON = Button(image=None, pos=(200, 460),
                                  text_input="BACK", font=button_font, base_color='Black',
                                  hovering_color=COLORS['HOVER'])

        self.button_font = button_font

        self.CONNECT_BUTTON = Button(image=None, pos=(500, 460),
                                     text_input="CONNECT", font=button_font, base_color='Black',
                                     hovering_color=COLORS['HOVER'])

        self.port = '/dev/cu.usbmodem142201'
        self.serial_speed = '115200'

        self.PORT_INPUT = Input(py_game=py_game, pos=(400, 330), text_input=self.port, font=input_font,
                                c_active='lightskyblue3', c_passive='lightgrey', default_width=200, height=32)
        self.SERIAL_SPEED_INPUT = Input(py_game=py_game, pos=(400, 375), text_input=self.serial_speed, font=input_font,
                                        c_active='lightskyblue3', c_passive='lightgrey', default_width=200, height=32)

        self.OPTIONS_TEXT = Text(pos=(400, 260), text_input="Set up your Arduino",
                                 font=button_font, base_color="Black")
        self.PORT_TEXT = Text(pos=(250, 350), text_input="Arduino port: ",
                              font=param_font, base_color="Black")
        self.SERIAL_SPEED_TEXT = Text(pos=(250, 390), text_input="Serial speed: ",
                                      font=param_font, base_color="Black")

    def draw(self, py_game):
        self.OPTIONS_TEXT.update(self.screen)
        self.PORT_TEXT.update(self.screen)
        self.SERIAL_SPEED_TEXT.update(self.screen)

        self.PORT_INPUT.update(py_game, self.screen)
        self.SERIAL_SPEED_INPUT.update(py_game, self.screen)

    def update_connect_button(self, is_connected):
        if is_connected:
            self.CONNECT_BUTTON = Button(image=None, pos=(500, 460),
                                         text_input="DISCONNECT", font=self.button_font, base_color='Black',
                                         hovering_color='Red')
        else:
            self.CONNECT_BUTTON = Button(image=None, pos=(500, 460),
                                         text_input="CONNECT", font=self.button_font, base_color='Black',
                                         hovering_color=COLORS['HOVER'])

