from model_infra.model import Model
from model_infra.utils import data_split


class NNVerify:
    def __init__(self, model: Model) -> None:
        self.model = model
        self.precondition = data_split(model.data_dir, model.y_header)[0]
        self.postcondition = None

    def prepare_postcondition(self):
        self.postcondition = self.model.predict(self.precondition)
