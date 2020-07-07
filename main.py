import kivy
from kivy.app import App as app
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.graphics import *
from kivy.clock import Clock
import threading
import numpy as np
import math

Window.size = (800, 600)


class Bullet(Rectangle):
    def __init__(self):
        print("bullet fire")

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.a = 90

        with self.canvas:
            self.player = Rectangle(pos=(385, 20), size=(30, 30))
            piy = (500 * math.sin(math.radians(self.a))) + self.player.pos[1] + 30
            pix = (500 * math.cos(math.radians(self.a))) + (self.player.pos[0] + (self.player.size[0]/2) - 2)
            self.pointer = Rectangle(pos=(pix, piy), size=(4, 4))
            self.pline = Line(points=[self.pointer.pos[0],self.player.pos[1], self.pointer.pos[0], self.pointer.pos[1]])
        self.keysPressed = set()

        Clock.schedule_interval(self.move_step, 0)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if text == " ":
            self.fire(self)

        if text is not None:
            self.keysPressed.add(text)

        if text is None:
            self.keysPressed.add(keycode[1])

    def _on_keyboard_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

    def move_step(self, dt):
        print(self.player.pos[0])
        posx = self.player.pos[0]
        posy = self.player.pos[1]
        pointx = self.pointer.pos[0]
        pointy = self.pointer.pos[1]
        step_size = 200 * dt
        circ_size = 100 * dt

        if "a" in self.keysPressed:
            if self.pointer.pos[0] > 50:
                posx -= step_size
                pointx -= step_size

        if "d" in self.keysPressed:
            if self.pointer.pos[0] < 750:
                posx += step_size
                pointx += step_size

        if 'left' in self.keysPressed:
            #pointx -= step_size
            if self.pointer.pos[0] > 50 and self.a < 175:
                self.a += circ_size

            pointy = (500 * math.sin(math.radians(self.a))) + posy
            pointx = (500 * math.cos(math.radians(self.a))) + posx

        if 'right' in self.keysPressed:
            #pointx += step_size
            if self.pointer.pos[0] < 750 and self.a > 5:
                self.a -= circ_size

            pointy = (500 * math.sin(math.radians(self.a))) + posy
            pointx = (500 * math.cos(math.radians(self.a))) + posx

        self.player.pos = (posx, posy)
        #pointy = (self.player.pos[1] + 200) * math.sin(math.radians(self.a))
        #pointx = (self.player.pos[0] + 200) * math.cos(math.radians(self.a))
        self.pointer.pos = (pointx, pointy)
        self.pline.points =[self.player.pos[0] + (self.player.size[0]/2), self.player.pos[1]+30, self.pointer.pos[0], self.pointer.pos[1]]

    def fire(self, dt):
        print("Fire!")



class Main(app):
    def build(self):
        return GameWidget()


if __name__ == "__main__":
    Main().run()