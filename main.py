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
import random
import math

from ai import MyAI

# třida Boat vytvoří objekt "lodě" 
class Boat(Widget):
    id = NumericProperty(0)
    t = NumericProperty(0)
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

# třída Rock (skála)
class Rock(Widget):
    def __init__(self, **kwargs):
        super(Rock, self).__init__(**kwargs)

# třída ve které jsou řešeny všechny logické operace
class PathFinder(FloatLayout):
    # vytvoření a nastavení typu proměnných
    pos_x = NumericProperty(0)
    pos_y = NumericProperty(0)
    start = ObjectProperty(None)
    finish = ObjectProperty(None)
    rocks = ListProperty(None)
    boats = ListProperty(None)
    # Proměnné s přednastaveným počtem lodí, skal a trénovacích dat
    rockCount = NumericProperty(30)
    boatCount = NumericProperty(10)
    data = NumericProperty(4000)
    # na začátku vytvoří určité objekty
    def __init__(self, **kwargs):
        super(PathFinder, self).__init__(**kwargs)
        # Vytvoří všechny objekty ve hře
        self.rocks = []
        self.boats = []
        self.add_rock(self.rockCount)
        self.add_start()
        self.add_finish()
        self.add_boat()
        # vytvoří a "natrénuje" AI
        self.ai = MyAI(self.data)

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

            # vygeneruje náhodnou velikost skály
            rSize = random.randint(30,100)
            rock.size= (rSize,rSize)

            self.validPos(0)
            rock.center_x = self.pos_x
            rock.center_y = self.pos_y
            self.rocks.append(rock)
            self.add_widget(rock)

    # vytvoří a umístí objekty Boat
    def add_boat(self):
        for i in range(0, self.boatCount):
            boat = Boat()
            boat.center_x = self.start.center_x
            boat.center_y = self.start.center_y

            # Náhodný směr ve kterém loď vypluje
            angle = random.randint(0, 360)
            boat.velocity = Vector(2,0).rotate(angle)

            # přiřadí k lodi id
            boat.id = i+1

            # náhodně vygeneruje preferovaný směr otáčení
            boat.t = random.randint(0,1)

            self.boats.append(boat)
            self.add_widget(boat)

    # ověří zda se na vygenerované pozici již nachází nějaký objekt,
    # když se na takové pozici nachází objekt, pozice se vygeneruje znovu a znovu se ověří
    def validPos(self, x):
        # podmínka, která zabraňuje vygenerování objektů na horní straně okna
        if (self.pos_y<Window.height-100):
            for c in self.rocks:
                # kontrola při generování nově přidaných skal
                if (self.finish and math.sqrt((self.pos_x-self.finish.center_x)**2+(self.pos_y-self.finish.center_y)**2)<self.finish.size[0]+10):
                    self.random_pos()
                    self.validPos(x)
                if (self.start and math.sqrt((self.pos_x-self.start.center_x)**2+(self.pos_y-self.start.center_y)**2)<self.start.size[0]+10):
                    self.random_pos()
                    self.validPos(x)

                # Kontroluje zda se na nové pozici nenachází skála
                if (math.sqrt((self.pos_x-c.center_x)**2+(self.pos_y-c.center_y)**2)<c.size[0]+15):
                    self.random_pos()
                    self.validPos(x)

                # při vytvoření finishe kontroluje zda se nachází minimálně o vzdálenost poloviny obrazovky daleko
                elif (x and math.sqrt((self.pos_x-self.start.center_x)**2+(self.pos_y-self.start.center_y)**2)<math.sqrt(Window.height**2+Window.width**2)/2):
                    self.random_pos()
                    self.validPos(x)
                else:
                    pass
        else:
            self.random_pos()
            self.validPos(x)

    # metoda, která bere aktuální data a posílá je do natrénovaného modelu
    # určuje chování lodě podle výstupu z tohoto modelu
    def ai_method(self,b):
        # směry na obě strany od lodě (o 30°)
        right = Vector(b.velocity_x, b.velocity_y).rotate(30)
        left = Vector(b.velocity_x, b.velocity_y).rotate(-30)
        #vytvoření proměných pro data posílané do modelu
        self.f, self.r, self.l, self.d = 0, 0, 0, 0
        # Nachází-li se nějaká skála před, napravo nebo nalevo od lodi,
        # nastaví se daná proměnná na 1 (True)
        for c in self.rocks:
            if (math.sqrt((b.center_x +b.velocity_x*10-c.center_x)**2+(b.center_y+b.velocity_y*10-c.center_y)**2)<(c.size[0]+5)/2):
                self.f = 1
            if (math.sqrt((b.center_x +right[0]*10-c.center_x)**2+(b.center_y+right[1]*10-c.center_y)**2)<(c.size[0]+5)/2):
                self.r = 1
            if (math.sqrt((b.center_x +left[0]*10-c.center_x)**2+ (b.center_y+left[1]*10-c.center_y)**2)<(c.size[0]+5)/2):
                self.l = 1
        # Zjištujě zda loď míří k cíli (min pod úhlem 25°)
        if abs(Vector(b.velocity).angle((self.finish.center_x - b.center_x,
                self.finish.center_y - b.center_y))) < 25:
            self.d = 1
        else: self.d = 0
        # vytvoření pole dat
        data=[b.t,self.f,self.r,self.l,self.d]
        # získá výstup z modelu na základě dat
        prediction = self.ai.predict(data)
        # Vyhodnotí-li model jako nejlepší výstup zatáčení doleva, nastaví se podle
        # toho promměná dir a nastaví se poslední směr ve kterém se loď otáčela
        if prediction == 0:
            dir = -1
            if self.d:
                b.t = 1
        # Vyhodnotí-li model jako nejlepší výstup zatáčení doprava, nastaví se podle
        # toho promměná dir a nastaví se poslední směr ve kterém se loď otáčela
        elif prediction == 2:
            dir = 1
            if self.d:
                b.t = 0
        # Loď pojede rovně
        else: dir = 0
        # Změna směru lodi podle výstupu z modelu
        b.velocity = Vector(b.velocity_x,b.velocity_y).rotate(10*dir)

    # zajišťuje překreslení canvasu při přidávání objektů
    def draw(self):
        self.canvas.clear()
        # je-li nový počet kamenů menší než ten předchozí, odstraní se poslední z vygenerovaných kamenů
        if self.rockCount<len(self.rocks):
            for i in range(0,len(self.rocks)-self.rockCount):
                self.rocks.pop(-1)
        # přidá nové kameny
        else:
            self.add_rock(self.rockCount-len(self.rocks))
        # Vykreslí všechny kameny
        for c in self.rocks:
            rock = Rock()
            rock.size=c.size
            rock.center_x=c.center_x
            rock.center_y=c.center_y
            self.add_widget(rock)
        # vykreslí všechny ostatní objekty
        start_ = Start()
        start_.center_x=self.start.center_x
        start_.center_y=self.start.center_y
        finish_ = Finish()
        finish_.center_x=self.finish.center_x
        finish_.center_y=self.finish.center_y
        self.add_widget(start_)
        self.add_widget(finish_)
        self.boats=[]
        # vygenerují se nové lodě
        self.add_boat()

    # zajišťuje pohyb lodí a zjišťuje zda nenarazila do skály
    def update(self, dt):
        for b in self.boats:
            # Zajistí zatáčení lodě
            self.ai_method(b)

            # zajistí pohyb lodě
            b.move()

            # Odražení od zdi
            if(b.x<0 or b.x>Window.width-5):
                b.velocity_x *= -1
            if(b.y<0 or b.y>Window.height-5):
                b.velocity_y *= -1

            # Když loď dorazí do cíle, přestane se pohybovat a vypíše se hláška do konzole
            if (math.sqrt((b.center_x-self.finish.center_x)**2+(b.center_y-self.finish.center_y)**2)<25):
                print(f"boat number {b.id} has finished!")
                self.boats.remove(b)

            # Když lod narazí do skály, je "zničena" a dále se nepohybuje
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
        # Popisky a uživatelské vstupy
        rootWindow = GridLayout(cols=8, row_force_default=True, row_default_height=40,spacing=10, padding=20)
        self.rock_input = TextInput(text=f"{self.app.rockCount}",multiline=False,font_size=20,input_filter='int')
        rock_label = Label(text="Rocks (1-50): ",font_size=20,color=(0,0,0,1))
        self.boat_input = TextInput(text=f"{self.app.boatCount}",multiline=False,font_size=20,input_filter='int')
        boat_label = Label(text="Boats (1-50): ",font_size=20,color=(0,0,0,1))
        submitBtn = Button(text='submit',on_release=self.submit)
        self.resetBtn = Button(text='reset',on_release=self.reset)
        self.data_input = TextInput(text=f"{self.app.data}",multiline=False,font_size=20,input_filter='int')
        data_label = Label(text="Data (1000-10000): ",font_size=20,color=(0,0,0,1))
        rootWindow.add_widget(rock_label)
        rootWindow.add_widget(self.rock_input)
        rootWindow.add_widget(boat_label)
        rootWindow.add_widget(self.boat_input)
        rootWindow.add_widget(submitBtn)
        rootWindow.add_widget(self.resetBtn)
        rootWindow.add_widget(data_label)
        rootWindow.add_widget(self.data_input)
        rootWindow.add_widget(self.app)
        # Aplikace se updatuje 60krát za sekundu
        Clock.schedule_interval(self.app.update, 1.0/60.0)
        return rootWindow
    
    # funkce vyvolaná tlačítkem submitBtn -> ubere/přídá objekty podle hodnot zadaných uživatelem
    def submit(self,obj):
        if (int(self.rock_input.text) < 1):
            self.app.rockCount = 1
        elif (int(self.rock_input.text) > 500):
            self.app.rockCount = 500
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
        self.submit(1)
        self.app.canvas.clear()
        if (int(self.data_input.text) < 1000):
            self.app.data = 1000
        elif (int(self.data_input.text) > 10000):
            self.app.data = 10000
        else:
            self.app.data = int(self.data_input.text)
        self.data_input.text = str(self.app.data)
        self.app.__init__()

# Nastavení okna a spuštění aplikace
if __name__ == "__main__":
    Window.clearcolor = (.4, .8, 1, 1)
    Config.set('graphics', 'width', 1280)
    Config.set('graphics', 'height', 720)
    Config.set('graphics', 'resizable', False)
    Config.write()
    MainApp().run()
