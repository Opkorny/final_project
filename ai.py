import numpy as np
from tensorflow import keras
from random import randint

# Pole všech možných situací, které mohou nastat
training_inputs = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0],[0, 0, 0, 1, 1],[0, 0, 1, 0, 0],[0, 0, 1, 0, 1],[0, 0, 1, 1, 0],[0, 0, 1, 1, 1],[0, 1, 0, 0, 0],[0, 1, 0, 0, 1],[0, 1, 0, 1, 0],[0, 1, 0, 1, 1],[0, 1, 1, 0, 0],[0, 1, 1, 0, 1],[0, 1, 1, 1, 0],[0, 1, 1, 1, 1],[1, 0, 0, 0, 0],[1, 0, 0, 0, 1],[1, 0, 0, 1, 0],[1, 0, 0, 1, 1],[1, 0, 1, 0, 0],[1, 0, 1, 0, 1],[1, 0, 1, 1, 0],[1, 0, 1, 1, 1],[1, 1, 0, 0, 0],[1, 1, 0, 0, 1],[1, 1, 0, 1, 0],[1, 1, 0, 1, 1],[1, 1, 1, 0, 0],[1, 1, 1, 0, 1],[1, 1, 1, 1, 0],[1, 1, 1, 1, 1]]
# Pole všech výstupů, předpokládaných v daných situacích ↑
training_outputs = [[-1],[0],[1],[0],[-1],[0],[0],[0],[-1],[1],[1],[1],[-1],[-1],[-1],[1],[1],[0],[1],[0],[-1],[0],[0],[0],[1],[-1],[1],[1],[-1],[-1],[1],[-1]]

# Třída MyAI
class MyAI:
    # při vytvoření
    def __init__(self,data):
        # proměnná určující počet trénovacích dat
        self.COUNT = data

        # nastavení modelu
        self.model = self.create_model()

        # vytvoření vstupů a výstupů
        self.create_input()
        self.create_output()
        self.data = [self.input, self.output]

        #trénování modelu
        self.train_model(self.data)

    # náhodně vygenerované vstupy
    def create_input(self):
        self.input = []
        for i in range(self.COUNT):
            t = randint(0,1)
            f = randint(0,1)
            r = randint(0,1)
            l = randint(0,1)
            d = randint(0,1)
            self.input.append([t,f,r,l,d])
        self.input = np.array(self.input).reshape(self.COUNT,5)

    # k náhodně vygenerovaným vstupům přiřadí předpokládaný výstup
    def create_output(self):
        self.output = []
        for obj in self.input:
            for i in range(32):
                if obj[0] == training_inputs[i][0] and obj[1] == training_inputs[i][1] and obj[2] == training_inputs[i][2] and obj[3] == training_inputs[i][3] and obj[4] == training_inputs[i][4]:
                    # zatáčení doleva
                    if training_outputs[i][0] == -1:
                        self.output.append([1, 0, 0])
                    # Pokračování rovně
                    if training_outputs[i][0] == 0:
                        self.output.append([0, 1, 0])
                    # Zatáčení doprava
                    if training_outputs[i][0] == 1:
                        self.output.append([0, 0, 1])
        self.output = np.array(self.output).reshape(self.COUNT,3)

    # Vytvoří model neuronové sítě
    def create_model(self):
        model = keras.models.Sequential()
        # Vstupní vrstva
        model.add(keras.layers.Dense(128, activation="relu"))
        # Skryté vrstvy
        model.add(keras.layers.Dense(128, activation="relu"))
        model.add(keras.layers.Dense(128, activation="relu"))
        # Vrstva, která rozhoduje nad nejlepším výstupem
        model.add(keras.layers.Dense(3, activation="softmax"))
        # Kompilace modelu
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])
        return model

    # Natrénuje model pomocí vygenerovaných dat a jejich výstupů
    def train_model(self, data):
        self.model.fit(data[0], data[1], epochs=1, batch_size=32, shuffle=True)

    # Metoda, která určí předpokládaný výstup podle aktuálních dat z aplikace
    def predict(self, data):
        data = np.array(data).reshape(1, 5)
        prediction = self.model(data)
        return np.argmax(prediction[0])
