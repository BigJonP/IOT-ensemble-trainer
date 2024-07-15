from collections import Counter
from typing import List

import numpy as np


def bagging_decision(predictions: List[List]) -> List:
    print(predictions)
    matrix = np.array([np.array(xi) for xi in predictions])
    final_predictions = []

    for i in range(len(matrix[0, :])):
        count = Counter(matrix[:, i])
        final_predictions.append(count.most_common(1)[0][0])
    return final_predictions
