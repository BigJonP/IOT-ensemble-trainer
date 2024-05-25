from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from model_infra.utils import data_split


class Model:
    def __init__(self, config: dict) -> None:
        self.type: str = config["type"]
        self.params: dict = config["params"]
        self.data_dir: str = config["data"]["dir"]
        self.y_header: str = config["data"]["y_header"]
        self.scaler = None
        self.model = None
        self.accuracy = None

    def train_model(self):
        x_train, x_test, y_train, y_test = self.get_train_data()

        if self.type == "MLP":
            self.model = MLPClassifier(**self.params)
            self.model.fit(x_train, y_train)
            self.accuracy = self.model.score(x_test, y_test)

    def get_train_data(self) -> tuple:
        x, y = data_split(self.data_dir, self.y_header)

        self.scaler = StandardScaler()
        x = self.scaler.fit_transform(x)
        return train_test_split(x, y, test_size=0.2, random_state=42)

    def predict(self, raw_input) -> list:
        try:
            x = self.scaler.transform(raw_input)
        except AttributeError as e:
            raise AttributeError(
                "Model scaler has not been create please train the model first"
            ) from e
        return self.model.predict(x)
