from typing import Optional

import numpy as np
import pandas as pd
import tensorflow as tf
from keras.layers import Activation, Dense
from keras.models import Sequential
from keras.utils.np_utils import to_categorical
from sklearn.ensemble import RandomForestClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from utils import data_split


class Model:
    def __init__(
        self,
        params: dict,
        df: Optional[pd.DataFrame] = None,
        y_header: Optional[str] = None,
    ) -> None:
        self.df = df
        self.type = params["type"]
        if df is not None and y_header:
            self.X, self.y = data_split(df, y_header)
        self.model = (
            parse_mlp_arch(params, df, y_header)
            if params["type"] == "MLP"
            else parse_model_arch(params)
        )
        self.encoder = LabelEncoder()

    def train(self) -> None:

        if self.type == "MLP":
            self.X = tf.convert_to_tensor(self.X)
            self.encoder.fit(self.y)
            self.y = self.encoder.transform(self.y)
            self.y = to_categorical(self.y)
            self.model.fit(self.X, self.y, epochs=32)
        else:
            self.model.fit(self.X, self.y)

    def predict(self, X: list) -> list:
        if self.type == "MLP":
            predictions = self.model.predict(X)
            predictions = np.argmax(predictions, axis=1)
            return self.encoder.inverse_transform(predictions)

        return self.model.predict(X)


def parse_model_arch(params: list):
    if params["type"] == "LogisticRegression":
        return LogisticRegression(**params["params"])
    if params["type"] == "SVC":
        return SVC(**params["params"])
    if params["type"] == "RandomForestClassifier":
        return RandomForestClassifier(**params["params"])
    if params["type"] == "DecisionTreeClassifier":
        return DecisionTreeClassifier(**params["params"])
    if params["type"] == "KNeighborsClassifier":
        return KNeighborsClassifier(**params["params"])
    if params["type"] == "GaussianNB":
        return GaussianNB(**params["params"])
    if params["type"] == "GaussianProcessClassifier":
        return GaussianProcessClassifier(**params["params"])


def parse_mlp_arch(params: list, df: pd.DataFrame, y_header: str) -> Sequential:
    model = Sequential(
        [
            Dense(
                len(set(df[y_header])),
                activation="linear",
                input_shape=(df.shape[1] - 1,),
            ),
            Activation("softmax"),
        ]
    )

    for layer, activ in params.items():
        if layer == "dense":
            model.add(
                Dense(
                    len(set(df[y_header])),
                    activation=activ,
                    input_shape=(df.shape[1] - 1,),
                )
            )

        if layer == "activation":
            model.add(Activation(activ))
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    return model
