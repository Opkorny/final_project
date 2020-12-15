import numpy as np
from tensorflow import keras
from random import randint

training_inputs = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0],[0, 0, 0, 1, 1],[0, 0, 1, 0, 0],[0, 0, 1, 0, 1],[0, 0, 1, 1, 0],[0, 0, 1, 1, 1],[0, 1, 0, 0, 0],[0, 1, 0, 0, 1],[0, 1, 0, 1, 0],[0, 1, 0, 1, 1],[0, 1, 1, 0, 0],[0, 1, 1, 0, 1],[0, 1, 1, 1, 0],[0, 1, 1, 1, 1],[1, 0, 0, 0, 0],[1, 0, 0, 0, 1],[1, 0, 0, 1, 0],[1, 0, 0, 1, 1],[1, 0, 1, 0, 0],[1, 0, 1, 0, 1],[1, 0, 1, 1, 0],[1, 0, 1, 1, 1],[1, 1, 0, 0, 0],[1, 1, 0, 0, 1],[1, 1, 0, 1, 0],[1, 1, 0, 1, 1],[1, 1, 1, 0, 0],[1, 1, 1, 0, 1],[1, 1, 1, 1, 0],[1, 1, 1, 1, 1]]
training_outputs = [[-1],[0],[1],[0],[-1],[0],[0],[0],[-1],[-1],[1],[1],[-1],[-1],[-1],[-1],[1],[0],[1],[0],[-1],[0],[0],[0],[1],[1],[1],[1],[-1],[-1],[1],[1]]


class MyAI:
    def __init__(self):
        self.count = 100000
        self.model = self.create_model()
        self.create_input()
        self.create_output()
        self.data = [self.input, self.output]
        self.train_model(self.data)

    def create_input(self):
        self.input = []
        for i in range(self.count):
            t = randint(0,1)
            f = randint(0,1)
            r = randint(0,1)
            l = randint(0,1)
            d = randint(0,1)
            self.input.append([t,f,r,l,d])
        self.input = np.array(self.input).reshape(self.count,5)

    def create_output(self):
        self.output = []
        for obj in self.input:
            for i in range(32):
                if obj[0] == training_inputs[i][0] and obj[1] == training_inputs[i][1] and obj[2] == training_inputs[i][2] and obj[3] == training_inputs[i][3] and obj[4] == training_inputs[i][4]:
                    self.output.append(training_outputs[i])
        self.output = np.array(self.output).reshape(self.count,1)



    def create_model(self):
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(128, activation="relu"))
        model.add(keras.layers.Dense(128, activation="relu"))
        model.add(keras.layers.Dense(128, activation="relu"))
        model.add(keras.layers.Dense(1, activation="tanh"))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=["accuracy"])
        return model

    def train_model(self, data):
        self.model.fit(data[0], data[1], epochs=3, batch_size=64, shuffle=True)

    def predict(self, data):
        data = np.array(data).reshape(1, 5)
        return self.model(data)
