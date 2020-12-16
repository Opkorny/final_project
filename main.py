from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.graphics import Color

import random
import math

class Boat(Widget):
    velocity_x = NumericProperty(2)
    velocity_y = NumericProperty(0)
    angle = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    def __init__(self, **kwargs):
        super(Boat, self).__init__(**kwargs)

    def move(self):
        self.pos = Vector(*self.velocity).rotate(self.angle) + self.pos

class Start(Widget):
    def __init__(self, **kwargs):
        super(Start, self).__init__(**kwargs)


class Checkpoint(Widget):
    def __init__(self, **kwargs):
        super(Checkpoint, self).__init__(**kwargs)


class PathFinder(FloatLayout):
    start = ObjectProperty(None)
    checkpoints = ListProperty(None)
    boats = ListProperty(None)
    pos_x = NumericProperty(0)
    pos_y = NumericProperty(0)
    checkpointCount = NumericProperty(3)
    boatCount = NumericProperty(100)
    def __init__(self, **kwargs):
        super(PathFinder, self).__init__(**kwargs)
        self.checkpoints = []
        self.boats = []
        self.add_checkpoint(self.checkpointCount)
        self.add_start()
        self.add_boat()

    def random_pos(self):
        self.pos_x = random.randint(50,Window.width-50)
        self.pos_y = random.randint(50,Window.height-50)

    def add_start(self):
        self.start = Start()
        self.random_pos()
        self.validPos()
        self.start.center_x = self.pos_x
        self.start.center_y = self.pos_y
        self.add_widget(self.start)

    def add_checkpoint(self, count):
        for i in range (0, count):
            checkpoint = Checkpoint()
            self.random_pos()
            self.validPos()
            checkpoint.center_x = self.pos_x
            checkpoint.center_y = self.pos_y
            self.checkpoints.append(checkpoint)
            self.add_widget(checkpoint)
            #print(f"Checkpoint {self.checkpoints[i].center_x},{self.checkpoints[i].center_y}")

    def add_boat(self):
        for i in range(0, self.boatCount):
            boat = Boat()
            boat.angle=random.randint(0,360)
            boat.center_x = self.start.center_x
            boat.center_y = self.start.center_y
            self.boats.append(boat)
            self.add_widget(boat)

    def validPos(self):
        if (self.pos_y<Window.height-100):
            for c in self.checkpoints:
                if (math.sqrt((self.pos_x-c.center_x)**2+(self.pos_y-c.center_y)**2)<50):
                    self.random_pos()
                    self.validPos()
                else:
                    pass
                #print(math.sqrt((self.pos_x-c.center_x)**2+(self.pos_y-c.center_y)**2)<50)
        else:
            self.random_pos()
            self.validPos()

    def draw(self):
        self.canvas.clear()
        if self.checkpointCount<len(self.checkpoints):
            for i in range(0,len(self.checkpoints)-self.checkpointCount):
                self.checkpoints.pop(-1)
        else:
            self.add_checkpoint(self.checkpointCount-len(self.checkpoints))
        for c in self.checkpoints:
            checkpoint = Checkpoint()
            checkpoint.center_x=c.center_x
            checkpoint.center_y=c.center_y
            self.add_widget(checkpoint)
        start_ = Start()
        start_.center_x=self.start.center_x
        start_.center_y=self.start.center_y
        self.add_widget(start_)
        self.boats=[]
        self.add_boat()

    def update(self, dt):
        for i in range(0, self.boatCount):
            self.boats[i].move()

class MainApp(App):
    def build(self):
        self.title = 'PathFinder'
        self.app = PathFinder()
        rootWindow = GridLayout(cols=6, row_force_default=True, row_default_height=40,spacing=10, padding=20)
        self.check_input = TextInput(text=f"{self.app.checkpointCount}",multiline=False,font_size=20,input_filter='int')
        check_label = Label(text="Checkpoints (1-5): ",font_size=20,color=(0,0,0,1))
        self.boat_input = TextInput(text=f"{self.app.boatCount}",multiline=False,font_size=20,input_filter='int')
        boat_label = Label(text="Boats (1+): ",font_size=20,color=(0,0,0,1))
        submitBtn = Button(text='submit',on_release=self.submit)
        self.resetBtn = Button(text='reset',on_release=self.reset)
        rootWindow.add_widget(check_label)
        rootWindow.add_widget(self.check_input)
        rootWindow.add_widget(boat_label)
        rootWindow.add_widget(self.boat_input)
        rootWindow.add_widget(submitBtn)
        rootWindow.add_widget(self.resetBtn)
        rootWindow.add_widget(self.app)
        Clock.schedule_interval(self.app.update, 1.0/60.0)
        return rootWindow

    def submit(self,obj):
        if (int(self.check_input.text) < 1):
            self.app.checkpointCount = 1
        elif (int(self.check_input.text) > 5):
            self.app.checkpointCount = 5
        else:
            self.app.checkpointCount = int(self.check_input.text)
        if (int(self.boat_input.text) < 1):
            self.app.boatCount = 1
        else:
            self.app.boatCount = int(self.boat_input.text)
        self.check_input.text = str(self.app.checkpointCount)
        self.boat_input.text = str(self.app.boatCount)
        self.app.draw()

    def reset(self,obj):
        self.app.canvas.clear()
        self.app.__init__()

if __name__ == "__main__":
    Window.clearcolor = (0, .8, 1, 1)
    Window.maximize()
    MainApp().run()
