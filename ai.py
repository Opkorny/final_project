import numpy as np
import tensorflow as tf

training_inputs = np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0],[0, 0, 0, 1, 1],[0, 0, 1, 0, 0],[0, 0, 1, 0, 1],[0, 0, 1, 1, 0],[0, 0, 1, 1, 1],[0, 1, 0, 0, 0],[0, 1, 0, 0, 1],[0, 1, 0, 1, 0],[0, 1, 0, 1, 1],[0, 1, 1, 0, 0],[0, 1, 1, 0, 1],[0, 1, 1, 1, 0],[0, 1, 1, 1, 1],[1, 0, 0, 0, 0],[1, 0, 0, 0, 1],[1, 0, 0, 1, 0],[1, 0, 0, 1, 1],[1, 0, 1, 0, 0],[1, 0, 1, 0, 1],[1, 0, 1, 1, 0],[1, 0, 1, 1, 1],[1, 1, 0, 0, 0],[1, 1, 0, 0, 1],[1, 1, 0, 1, 0],[1, 1, 0, 1, 1],[1, 1, 1, 0, 0],[1, 1, 1, 0, 1],[1, 1, 1, 1, 0],[1, 1, 1, 1, 1]]).reshape(32, 5)
training_outputs = np.array([[-1],[0],[1],[0],[-1],[0],[0],[0],[-1],[-1],[1],[1],[-1],[-1],[-1],[-1],[1],[0],[1],[0],[-1],[0],[0],[0],[1],[1],[1],[1],[-1],[-1],[1],[1]]).reshape(32, 1)


class MyAI:
    def __init__(self):
        self.model = self.create_model()
        self.data = [training_inputs, training_outputs]
        self.train_model(self.data)

    def create_model(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(5, activation="relu"))
        model.add(tf.keras.layers.Dense(16, activation="relu"))
        model.add(tf.keras.layers.Dense(1, activation="tanh"))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=["accuracy"])
        return model

    def train_model(self, data):
        self.model.fit(data[0], data[1], epochs=3, batch_size=32, shuffle=True)

    def predict(self, data):
        data = np.array(data).reshape(1, 5)
        return self.model(data)
