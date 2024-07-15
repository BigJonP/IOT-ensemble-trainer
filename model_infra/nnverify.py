import pandas as pd
from z3 import *

from model_infra.model import Model
from sapphire.sapphire import *


def Between(lower, x, upper):
    return And([lower < x, x < upper])


def Verify(bounds: pd.DataFrame, model: Model) -> Solver:
    greater_than = bounds.iloc[0]["greater_than"]
    feature = model.df.columns.get_loc(bounds.iloc[0]["feature"])
    less_than = bounds.iloc[0]["less_than"]
    truth_category = bounds.iloc[0]["truth_category"]
    false_category_1 = bounds.iloc[0]["false_category_1"]
    false_category_2 = bounds.iloc[0]["false_category_2"]
    false_category_3 = bounds.iloc[0]["false_category_3"]

    mappings = dict(
        zip(
            model.encoder.classes_,
            model.encoder.transform(model.encoder.classes_),
        )
    )

    def IsTruth(Y):
        print(mappings)
        return And(
            Y[mappings[truth_category]] > Y[mappings[false_category_1]],
            Y[mappings[truth_category]] > Y[mappings[false_category_2]],
            Y[mappings[truth_category]] > Y[mappings[false_category_3]],
        )

    X, Y = NN(model.model)
    s = SolverFor("LRA")

    print(greater_than)
    print(X[feature])
    print(less_than)
    s.add(
        Implies(
            (
                And(
                    X[feature] < less_than,
                    X[feature] > greater_than,
                )
            ),
            (Not(IsTruth(Y))),
        )
    )

    return s
