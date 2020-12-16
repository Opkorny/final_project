# Importovani
from kivy.app import App
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
import random
import math

from ai import MyAI

# třida Boat vytvoří objekt "lodě" 
class Boat(Widget):
    id = NumericProperty(0)
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
    rockCount = NumericProperty(20)
    boatCount = NumericProperty(5)
    # na začátku vytvoří určité objekty
    def __init__(self, **kwargs):
        super(PathFinder, self).__init__(**kwargs)
        self.rocks = []
        self.boats = []
        self.add_rock(self.rockCount)
        self.add_start()
        self.add_finish()
        self.add_boat()
        self.ai = MyAI()
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
            boat.id = i+1
            self.boats.append(boat)
            self.add_widget(boat)


    # ověří zda se na vygenerované pozici již nachází nějaký objekt
    def validPos(self, x):
        if (self.pos_y<Window.height-100):
            for c in self.rocks:
                if (math.sqrt((self.pos_x-c.center_x)**2+(self.pos_y-c.center_y)**2)<c.size[0]+10):
                    self.random_pos()
                    self.validPos(x)
                elif (x and math.sqrt((self.pos_x-self.start.center_x)**2+(self.pos_y-self.start.center_y)**2)<math.sqrt(Window.height**2+Window.width**2)/2):
                    self.random_pos()
                    self.validPos(x)
                else:
                    pass
                #print(math.sqrt((self.pos_x-c.center_x)**2+(self.pos_y-c.center_y)**2)<50)
        else:
            self.random_pos()
            self.validPos(x)

    def ai_method(self,b):
        n = math.sqrt((b.center_x-self.finish.center_x)**2+(b.center_y-self.finish.center_y)**2)/2
        right = Vector(b.velocity_x, b.velocity_y).rotate(30)
        left = Vector(b.velocity_x, b.velocity_y).rotate(-30)
        self.f = 0
        self.r = 0
        self.l = 0
        self.d = 0
        self.t = 0
        self.direction = 0
        for c in self.rocks:
            if (math.sqrt((b.center_x +b.velocity_x*10-c.center_x)**2+(b.center_y+b.velocity_y*10-c.center_y)**2)<(c.size[0]+5)/2):
                self.f = 1
                break
            else: self.f = 0
        for c in self.rocks:
            if (math.sqrt((b.center_x +right[0]*8-c.center_x)**2+(b.center_y+right[1]*8-c.center_y)**2)<(c.size[0]+5)/2):
                self.r = 1
                break
            else: self.r = 0
        for c in self.rocks:
            if (math.sqrt((b.center_x +left[0]*8-c.center_x)**2+(b.center_y+left[1]*8-c.center_y)**2)<(c.size[0]+5)/2):
                self.l = 1
                break
            else: self.l = 0
        # if math.sqrt((self.finish.center_x -(b.center_x+b.velocity_x))**2+(self.finish.center_y-(b.center_y+b.velocity_x))**2)<math.sqrt((self.finish.center_x-b.center_x)**2+(self.finish.center_y-b.center_y)**2):
        if abs(Vector(b.velocity).angle((self.finish.center_x - b.center_x, self.finish.center_y - b.center_y))) < 20:
            self.d = 1
        else: self.d = 0
        print(math.sqrt((self.finish.center_x -(b.center_x+b.velocity_x))**2+(self.finish.center_y-(b.center_y+b.velocity_y))**2)-math.sqrt((self.finish.center_x-b.center_x)**2+(self.finish.center_y-b.center_y)**2))
        data=[self.t,self.f,self.r,self.l,self.d]
        print(data)
        prediction = self.ai.predict(data)
        if prediction == 0:
            self.t = 0
            self.dir = 1
        elif prediction == 2:
            self.t = 1
            self.dir = -1
        else:
            self.dir = 0
        print(prediction)
        b.velocity = Vector(b.velocity_x,b.velocity_y).rotate(15*self.dir)


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
        finish_ = Finish()
        finish_.center_x=self.finish.center_x
        finish_.center_y=self.finish.center_y
        self.add_widget(start_)
        self.add_widget(finish_)
        self.boats=[]
        self.add_boat()

    # zajišťuje pohyb lodí a zjišťuje zda nenarazila do skály
    def update(self, dt):
        for b in self.boats:
            self.ai_method(b)
            #print(b.velocity[0])
            b.move()
            if(b.x<0 or b.x>Window.width-5):
                b.velocity_x *= -1
            if(b.y<0 or b.y>Window.height-5):
                b.velocity_y *= -1
            if (math.sqrt((b.center_x-self.finish.center_x)**2+(b.center_y-self.finish.center_y)**2)<25):
                print(f"boat number {b.id} has finished!")
                self.boats.remove(b)
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
        self.rock_input = TextInput(text=f"{self.app.rockCount}",multiline=False,font_size=20,input_filter='int')
        rock_label = Label(text="Rocks (1-50): ",font_size=20,color=(0,0,0,1))
        self.boat_input = TextInput(text=f"{self.app.boatCount}",multiline=False,font_size=20,input_filter='int')
        boat_label = Label(text="Boats (1-100): ",font_size=20,color=(0,0,0,1))
        submitBtn = Button(text='submit',on_release=self.submit)
        self.resetBtn = Button(text='reset',on_release=self.reset)
        rootWindow.add_widget(rock_label)
        rootWindow.add_widget(self.rock_input)
        rootWindow.add_widget(boat_label)
        rootWindow.add_widget(self.boat_input)
        rootWindow.add_widget(submitBtn)
        rootWindow.add_widget(self.resetBtn)
        rootWindow.add_widget(self.app)
        Clock.schedule_interval(self.app.update, 1.0/60.0)
        return rootWindow
    
    # funkce vyvolaná tlačítkem submitBtn -> ubere/přídá objekty podle hodnot zadaných uživatelem
    def submit(self,obj):
        if (int(self.rock_input.text) < 1):
            self.app.rockCount = 1
        elif (int(self.rock_input.text) > 100):
            self.app.rockCount = 100
        else:
            self.app.rockCount = int(self.rock_input.text)
        if (int(self.boat_input.text) < 1):
            self.app.boatCount = 1
        elif (int(self.boat_input.text) > 50):
            self.app.boatCount = 50
        else:
            self.app.boatCount = int(self.boat_input.text)
        self.rock_input.text = str(self.app.rockCount)
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
