import numpy as np
from tensorflow import keras
from random import randint

training_inputs = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0],[0, 0, 0, 1, 1],[0, 0, 1, 0, 0],[0, 0, 1, 0, 1],[0, 0, 1, 1, 0],[0, 0, 1, 1, 1],[0, 1, 0, 0, 0],[0, 1, 0, 0, 1],[0, 1, 0, 1, 0],[0, 1, 0, 1, 1],[0, 1, 1, 0, 0],[0, 1, 1, 0, 1],[0, 1, 1, 1, 0],[0, 1, 1, 1, 1],[1, 0, 0, 0, 0],[1, 0, 0, 0, 1],[1, 0, 0, 1, 0],[1, 0, 0, 1, 1],[1, 0, 1, 0, 0],[1, 0, 1, 0, 1],[1, 0, 1, 1, 0],[1, 0, 1, 1, 1],[1, 1, 0, 0, 0],[1, 1, 0, 0, 1],[1, 1, 0, 1, 0],[1, 1, 0, 1, 1],[1, 1, 1, 0, 0],[1, 1, 1, 0, 1],[1, 1, 1, 1, 0],[1, 1, 1, 1, 1]]
training_outputs = [[1],[0],[1],[0],[-1],[0],[0],[0],[-1],[-1],[1],[1],[-1],[-1],[-1],[-1],[-1],[0],[1],[0],[-1],[0],[0],[0],[1],[1],[1],[1],[-1],[-1],[1],[1]]


class MyAI:
    def __init__(self):
        self.count = 2000
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
                    if training_outputs[i][0] == -1:
                        self.output.append([0, 0, 1])
                    if training_outputs[i][0] == 0:
                        self.output.append([0, 1, 0])
                    if training_outputs[i][0] == 1:
                        self.output.append([1, 0, 0])
        self.output = np.array(self.output).reshape(self.count,3)



    def create_model(self):
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(128, activation="relu"))
        model.add(keras.layers.Dense(128, activation="relu"))
        model.add(keras.layers.Dense(128, activation="relu"))
        model.add(keras.layers.Dense(3, activation="softmax"))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])
        return model

    def train_model(self, data):
        self.model.fit(data[0], data[1], epochs=2, batch_size=32, shuffle=True)

    def predict(self, data):
        data = np.array(data).reshape(1, 5)
        prediction = self.model(data)
        return np.argmax(prediction[0])
