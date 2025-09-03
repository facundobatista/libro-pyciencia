#!/usr/bin/env python3

import abc
import argparse
import pickle
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from tqdm import trange

# predictibilidad durante el desarrollo
np.random.seed(216091)


def load_dataset(datasource_path):
    """Carga los datos de trabajo."""
    # Lectura de datos
    train_data = np.genfromtxt(datasource_path, delimiter=',', skip_header=1, dtype=float)
    Y_train = train_data[:, 0].astype(int)
    X_train = train_data[:, 1:]

    # Normalizamos X
    X_train = X_train / 255

    return X_train, Y_train


class Layer(abc.ABC):
    """Capa abstracta.

    Cada capa puede realizar dos tareas:

      - Procesar la entrada para generar la salida: output = layer.forward(inputdata)

      - Implementar backpropagation: grad_input = layer.backward(inputdata, grad_output)

    Algunas capas tienen parámetros que se actualizan durante backpropagation (w, b).
    """

    @abc.abstractmethod
    def forward(self, inputdata):
        """Realiza un paso de propagación para adelante.

        Recibe una entrada de shape [batch, input_nodes], y devuelve la salida con
        shape [batch, output_nodes].
        """

    @abc.abstractmethod
    def backward(self, inputdata, grad_output):
        """Realiza un paso de backpropagation a través de la capa, respecto de la entrada.

        Si la capa tiene parámetros (capa densa), se actualiza en este paso.
        """


class ReLU(Layer):
    """Capa ReLU que aplica una unidad lineal rectificada elemento por elemento."""

    def forward(self, inputdata):
        """Aplica ReLU elemento por elemento a la matriz [batch, input_nodes]."""
        relu_forward = np.maximum(0, inputdata)
        return relu_forward

    def backward(self, inputdata, grad_output):
        """Calcula el gradiente de la función de costo respecto de la entrada ReLU."""
        relu_grad = inputdata > 0
        return grad_output * relu_grad


class Dense(Layer):
    """Capa densa; la salida es W * x + b = z."""

    def __init__(self, input_nodes, output_nodes, learning_rate=0.1):
        self.learning_rate = learning_rate
        self.W = np.random.normal(
            loc=0.0,
            scale=np.sqrt(2 / (input_nodes + output_nodes)),
            size=(input_nodes, output_nodes))
        self.bias = np.zeros(output_nodes)

    def forward(self, inputdata):
        """Calcula el producto matricial entre la entrada y los pesos, más los bias."""
        return np.dot(inputdata, self.W) + self.bias

    def backward(self, inputdata, grad_output):
        """Calcula df / dx = df / d[capa] d[capa]/dx donde d[capa] / dx = W.T."""
        grad_input = np.dot(grad_output, self.W.T)
        # cálculo del gradiente respecto de W y b
        grad_W = np.dot(inputdata.T, grad_output)
        grad_b = grad_output.mean(axis=0) * inputdata.shape[0]
        assert grad_W.shape == self.W.shape and grad_b.shape == self.bias.shape
        # Actualización de W y b por medio del descenso del gradiente.
        self.W = self.W - self.learning_rate * grad_W
        self.bias = self.bias - self.learning_rate * grad_b
        return grad_input


def softmax_crossentropy_with_logits(logits, reference_labels):
    """Cálculo de crossentropy.

    Se realiza a partir de logits[batch, n_clases] y las etiquetas de los datos.
    """
    logits_for_labels = logits[np.arange(len(logits)), reference_labels]
    xentropy = - logits_for_labels + np.log(np.sum(np.exp(logits), axis=-1))
    return xentropy


def grad_softmax_crossentropy_with_logits(logits, reference_labels):
    """Cálculo del gradiente de crossentropy.

    Se realiza a partir de logits[batch, n_clases] y las etiquetas de los datos.
    """
    ones_for_labels = np.zeros_like(logits)
    ones_for_labels[np.arange(len(logits)), reference_labels] = 1
    softmax = np.exp(logits) / np.exp(logits).sum(axis=-1, keepdims=True)
    return (- ones_for_labels + softmax) / logits.shape[0]


class Network:
    """Opera sobre una secuencia de capas."""

    def __init__(self, layers):
        self.layers = layers

    def _forward(self, inputdata):
        """Calcula las activaciones de todas las capas, secuencialmente.

        La salida de una capa es la entrada de la próxima. Devuelve una lista con
        las activaciones de cada capa.
        """
        activations = []
        for layer in self.layers:
            inputdata = layer.forward(inputdata)
            activations.append(inputdata)

        return activations

    def predict(self, X):
        """Calcula la predicción de la red.

        Devuelve el índice del mayor valor de probabilidad en logits.
        """
        layer_activations = self._forward(X)
        logits = layer_activations[-1]
        return logits.argmax(axis=-1)

    def train(self, X, y):
        """Entrena a la red con X e y."""
        # Etapa de avance de activaciones (forward)
        layer_activations = self._forward(X)

        # Agregamos al principio la entrada original para tener la entrada de cada capa
        # y separamos las últimas activaciones como logits
        *layer_inputs, logits = [X] + layer_activations

        # Cálculo de la función de pérdida (indicativo de lo bien entrenado)
        # para devolver al final
        loss = softmax_crossentropy_with_logits(logits, y)

        # Comenzamos la propagación de gradientes para atrás en la red (backpropagation)
        # por la última capa especial de entropía cruzada
        loss_grad = grad_softmax_crossentropy_with_logits(logits, y)

        # Seguimos la propagación para atrás por cada capa
        for layer, originalinput in reversed(list(zip(self.layers, layer_inputs))):
            loss_grad = layer.backward(originalinput, loss_grad)

        return np.mean(loss)

    def dump(self, filepath):
        """Guarda la red actual en un archivo."""
        with open(filepath, "wb") as fh:
            pickle.dump(self, fh)

    @classmethod
    def load(cls, filepath):
        """Recupera de disco una instancia de la red."""
        with open(filepath, "rb") as fh:
            return pickle.load(fh)


def get_minibatches(inputs, targets, batchsize, shuffle=False):
    assert len(inputs) == len(targets)
    if shuffle:
        indices = np.random.permutation(len(inputs))
    for start_idx in trange(0, len(inputs) - batchsize + 1, batchsize):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batchsize]
        else:
            excerpt = slice(start_idx, start_idx + batchsize)
        yield inputs[excerpt], targets[excerpt]


def train(datasource_path):
    # Cargamos los datos y reservamos los últimos ejemplos de entrenamiento para validación
    X_train, Y_train = load_dataset(datasource_path)
    limit = len(X_train) // 6
    X_train, X_val = X_train[:-limit], X_train[-limit:]
    Y_train, y_val = Y_train[:-limit], Y_train[-limit:]

    network = Network([
        Dense(X_train.shape[1], 100),
        ReLU(),
        Dense(100, 200),
        ReLU(),
        Dense(200, 10),
    ])

    train_log = []
    val_log = []

    for epoch in range(25):
        total_loss = 0
        for x_batch, y_batch in get_minibatches(X_train, Y_train, batchsize=32, shuffle=True):
            loss = network.train(x_batch, y_batch)
            total_loss += loss

        train_log.append(np.mean(network.predict(X_train) == Y_train))
        val_log.append(np.mean(network.predict(X_val) == y_val))

        print(f"Época {epoch}")
        print(f"Precisión de entrenamiento: {train_log[-1]:8.4f}")
        print(f"   Precisión de validación: {val_log[-1]:8.4f}")
        print(f"             Total pérdida: {total_loss:8.4f}")

    # guardar la red con su estado actual entrenado
    network.dump("trained.pkl")

    plt.plot(train_log, label='Precisión de entrenamiento')
    plt.plot(val_log, label='Precisión de validación')
    plt.xlabel("Época")
    plt.legend(loc='best')
    plt.grid()
    plt.show()


def show_images(datasource_path):
    """Muestra un ejemplo de las imágenes usadas como datos fuente."""
    X_train, Y_train = load_dataset(datasource_path)

    # reshape the sequence of bits so each 784 chunk is 28x28 (square image)
    X_train = X_train.reshape(-1, 28, 28)

    plt.figure(figsize=[6, 6])
    for i in range(4):
        plt.subplot(2, 2, i + 1)
        plt.title(f"Label: {Y_train[i]}")
        plt.imshow(X_train[i].reshape([28, 28]), cmap='gray')
    plt.show()


def evaluate(datasource_path):
    """Evalúa una red entrenada sobre un conjunto de datos de prueba."""
    print("Cargando red")
    network = Network.load("trained.pkl")
    print("Cargando dataset de prueba")
    X_test, Y_test = load_dataset(datasource_path)
    print("Prediciendo")
    predicted = network.predict(X_test)
    print("Listo")

    cnt = Counter(zip(Y_test, predicted == Y_test))

    digits = []
    pred_perc = []
    for digit in range(10):
        digits.append(digit)
        quant_ok = cnt[(digit, True)]
        quant_bad = cnt[(digit, False)]
        pred_perc.append(100 * quant_ok / (quant_ok + quant_bad))

    fig, ax = plt.subplots()
    ax.bar(digits, pred_perc, 0.7)
    ax.set_title("Precisión de las predicciones")
    ax.set_xticks(digits)
    ax.set_ylim([90, 100])
    ax.set_yticks(ticks=range(90, 101), labels=[f"{n}%" for n in range(90, 101)])
    plt.show()


_actions = {
    "devtrain": [train, "mnist_train_dev.csv"],
    "train": [train, "mnist_train.csv"],
    "show": [show_images, "mnist_train_dev.csv"],
    "eval": [evaluate, "mnist_test.csv"],
}
parser = argparse.ArgumentParser()
parser.add_argument("action", choices=_actions.keys(), help="Qué acción realizar")
args = parser.parse_args()
func, *params = _actions[args.action]
func(*params)

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
