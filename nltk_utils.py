import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

import numpy as np
import json
import re

nltk.download('punkt')
nltk.download('stopwords')

stemmer = SnowballStemmer('spanish')
stop_words = set(stopwords.words('spanish'))


def tokenizer(text):
    """
    Tokeniza un texto, convirtiéndolo a minúsculas, eliminando puntuación, separando en palabras
    y eliminando las stop words.

    Args:
        text (str): El texto que se desea tokenizar.

    Returns:
        List[str]: Lista de tokens (palabras) sin stop words.
    """

    # Paso 1: Convertir el texto a minúsculas para normalizar
    text = text.lower()

    # Paso 2: Eliminar caracteres no alfabéticos (excepto los espacios)
    text = re.sub(r'[^a-záéíóúüñ\s]', '', text)  # Eliminar todo lo que no sea letras o espacios

    # Paso 3: Dividir el texto en palabras (tokens)
    tokens = text.split()

    # Paso 4: Eliminar stop words (palabras vacías) de los tokens
    # tokens_without_stop_word = [word for word in tokens if word not in stop_words]

    return tokens


def stem(word):
    """
    Aplica las reglas de stemming a una palabra (sufijos o prefijos).

    Args:
        word (str): La palabra a la que se le va a aplicar el stemming.

    Returns:
        worn (str): La palabra con el stemming aplicado.
    """

    return stemmer.stem(word)


def bag_of_words(tokenized_sentence, words):
    """
    Crea una representación de la bolsa de palabras (bag of words) de una oración tokenizada.

    Args:
        tokenized_sentence (list): Lista de palabras de la oración tokenizada.
        words (list): Lista de todas las palabras posibles (vocabulario).

    Returns:
        np.array: Vector binario que representa la presencia de palabras en la oración.
    """

    tokenized_sentence = [stem(word) for word in tokenized_sentence]

    # Inicializamos un vector de ceros con el tamaño de la lista de palabras
    bag = np.zeros(len(words), dtype=np.float32)

    # Recorremos las palabras del vocabulario
    for idx, word in enumerate(words):
        # Si la palabra del vocabulario está en la oración tokenizada, ponemos un 1 en su posición
        if word in tokenized_sentence:
            bag[idx] = 1.0

    return bag