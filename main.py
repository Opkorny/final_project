# Importovani
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

# třida Boat vytvoří objekt "lodě" 
class Boat(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    def __init__(self, **kwargs):
        super(Boat, self).__init__(**kwargs)

# metoda pohybu lodě
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

# třída Finish 
class Finish(Widget):
    def __init__(self, **kwargs):
        super(Finish, self).__init__(**kwargs)

# třída Start
class Start(Widget):
    def __init__(self, **kwargs):
        super(Start, self).__init__(**kwargs)

# třída Rock
class Rock(Widget):
    def __init__(self, **kwargs):
        super(Rock, self).__init__(**kwargs)

# třída ve které jsou řešeny všechny logické operace
class PathFinder(FloatLayout):
    # vytvoření proměnných
    start = ObjectProperty(None)
    finish = ObjectProperty(None)
    rocks = ListProperty(None)
    boats = ListProperty(None)
    pos_x = NumericProperty(0)
    pos_y = NumericProperty(0)
    rockCount = NumericProperty(10)
    boatCount = NumericProperty(100)
    # na začátku vytvoří určité objekty
    def __init__(self, **kwargs):
        super(PathFinder, self).__init__(**kwargs)
        self.rocks = []
        self.boats = []
        self.add_rock(self.rockCount)
        self.add_start()
        self.add_finish()
        self.add_boat()
    # vygeneruje náhodnou pozici
    def random_pos(self):
        self.pos_x = random.randint(50,Window.width-50)
        self.pos_y = random.randint(50,Window.height-50)
    # vytvoří a umístí objekt Start
    def add_start(self):
        self.start = Start()
        self.random_pos()
        self.validPos(0)
        self.start.center_x = self.pos_x
        self.start.center_y = self.pos_y
        self.add_widget(self.start)

    # vytvoří a umístí objekt Finish
    def add_finish(self):
        self.finish = Finish()
        self.random_pos()
        self.validPos(1)
        self.finish.center_x = self.pos_x
        self.finish.center_y = self.pos_y
        self.add_widget(self.finish)

    # vytvoří a umístí objekty Rock
    def add_rock(self, count):
        for i in range (0, count):
            rock = Rock()
            self.random_pos()
            chSize = random.randint(30,100)
            rock.size= (chSize,chSize)
            self.validPos(0)
            rock.center_x = self.pos_x
            rock.center_y = self.pos_y
            self.rocks.append(rock)
            self.add_widget(rock)
            #print(f"Rock {self.rocks[i].center_x},{self.rocks[i].center_y}")

    # vytvoří a umístí objekty Boat
    def add_boat(self):
        for i in range(0, self.boatCount):
            boat = Boat()
            boat.center_x = self.start.center_x
            boat.center_y = self.start.center_y
            angle = random.randint(0, 360)
            boat.velocity = Vector(2,0).rotate(angle)
            self.boats.append(boat)
            self.add_widget(boat)


    # ověří zda se na vygenerované pozici již nachází nějaký objekt
    def validPos(self, x):
        if (self.pos_y<Window.height-100):
            for c in self.rocks:
                if (math.sqrt((self.pos_x-c.center_x)**2+(self.pos_y-c.center_y)**2)<c.size[0]):
                    self.random_pos()
                    self.validPos(x)
                elif (x and math.sqrt((self.pos_x-self.start.center_x)**2+(self.pos_y-self.start.center_y)**2)<math.sqrt(Window.height**2+Window.width**2)/3):
                    self.random_pos()
                    self.validPos(x)
                else:
                    pass
                #print(math.sqrt((self.pos_x-c.center_x)**2+(self.pos_y-c.center_y)**2)<50)
        else:
            self.random_pos()
            self.validPos(x)

    # zajišťuje překreslení canvasu při přidávání objektů
    def draw(self):
        self.canvas.clear()
        if self.rockCount<len(self.rocks):
            for i in range(0,len(self.rocks)-self.rockCount):
                self.rocks.pop(-1)
        else:
            self.add_rock(self.rockCount-len(self.rocks))
        for c in self.rocks:
            rock = Rock()
            rock.size=c.size
            rock.center_x=c.center_x
            rock.center_y=c.center_y
            self.add_widget(rock)
        start_ = Start()
        start_.center_x=self.start.center_x
        start_.center_y=self.start.center_y
        self.add_widget(start_)
        self.boats=[]
        self.add_boat()

    # zajišťuje pohyb lodí a zjišťuje zda nenarazila do skály
    def update(self, dt):
        for b in self.boats:
            b.move()
            if(b.x<0 or b.x>Window.width-5):
                b.velocity_x *= -1
            if(b.y<0 or b.y>Window.height-5):
                b.velocity_y *= -1
                pass
            for c in self.rocks:
                if (math.sqrt((b.center_x-c.center_x)**2+(b.center_y-c.center_y)**2)<(c.size[0]+5)/2):
                    self.boats.remove(b)
                else:
                    pass

# samotná aplikace
class MainApp(App):
    def build(self):
        self.title = 'PathFinder'
        self.app = PathFinder()
        rootWindow = GridLayout(cols=6, row_force_default=True, row_default_height=40,spacing=10, padding=20)
        self.check_input = TextInput(text=f"{self.app.rockCount}",multiline=False,font_size=20,input_filter='int')
        check_label = Label(text="Rocks (1-20): ",font_size=20,color=(0,0,0,1))
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
    
    # funkce vyvolaná tlačítkem submitBtn -> ubere/přídá objekty podle hodnot zadaných uživatelem
    def submit(self,obj):
        if (int(self.check_input.text) < 1):
            self.app.rockCount = 1
        elif (int(self.check_input.text) > 20):
            self.app.rockCount = 20
        else:
            self.app.rockCount = int(self.check_input.text)
        if (int(self.boat_input.text) < 1):
            self.app.boatCount = 1
        else:
            self.app.boatCount = int(self.boat_input.text)
        self.check_input.text = str(self.app.rockCount)
        self.boat_input.text = str(self.app.boatCount)
        self.app.draw()

    # vyresetuje celou aplikaci a vygeneruje znovu nové pozice
    def reset(self,obj):
        self.app.canvas.clear()
        self.app.__init__()

# spuštění
if __name__ == "__main__":
    Window.clearcolor = (0, .8, 1, 1)
    Window.maximize()
    MainApp().run()
