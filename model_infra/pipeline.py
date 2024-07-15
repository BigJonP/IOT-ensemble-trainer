import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from typing import Tuple

import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, StackingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from model_infra.ensemble_helpers import bagging_decision
from model_infra.model import Model
from model_infra.nnverify import Verify
from utils import data_split, load_data


def run_pipeline(payload: Tuple[dict, str, tk.Frame]):
    main = payload[-1]
    config = payload[0]
    config["ensemble_method"] = payload[1]
    config["boosting_params"] = payload[2]

    df = load_data(config["file_path"])
    train, test = train_test_split(df, test_size=0.2)
    y_header = config["y_header"]
    X_test, y_test = data_split(test, y_header)
    if config["ensemble_method"] == "Bagging":
        num_samples = round(train.shape[0] * 0.7)
        training_samples = [train.sample(num_samples) for _ in config["models"]]

        models = [
            Model(model, df, y_header)
            for model, df in zip(config["models"], training_samples)
        ]

        for model in models:
            model.train()
            print("Finished training %s", model.model.__class__)

        predictions = bagging_decision([model.predict(X_test) for model in models])

    if config["ensemble_method"] == "Stacking":
        X_train, y_train = data_split(train, y_header)
        models = [
            (str(i), Model(model).model) for i, model in enumerate(config["models"])
        ]
        clf = StackingClassifier(
            estimators=models, final_estimator=Model(config["final_estimator"]).model
        )
        clf.fit(X_train, y_train)
        print("Finished training %s", clf.__class__)
        predictions = clf.predict(X_test)

    if config["ensemble_method"] == "Adaboosting":
        X_train, y_train = data_split(train, y_header)
        clf = AdaBoostClassifier(**config["boosting_params"])
        clf.fit(X_train, y_train)
        print("Finished training %s", clf.__class__)
        predictions = clf.predict(X_test)

    accuracy = accuracy_score(predictions, y_test)
    print(f"Accuracy: {accuracy}")
    ttk.Label(main, text=f"Accuracy: {accuracy}", font=("Times New Roman", 14)).grid(
        column=1, row=9
    )

    if config["ensemble_method"] != "Adaboosting":
        verify_payload = (models, main)
        if [model for model in models if model.type == "MLP"]:
            tk.Button(
                main,
                text="Verify MLPs",
                bd=3,
                bg="lightgray",
                disabledforeground="gray",
                fg="black",
                font=("Times New Roman", 12),
                command=lambda: verify_mlps(verify_payload),
            ).grid(column=1, row=8, columnspan=2, padx=10, pady=5)


def verify_mlps(payload: Tuple[list, tk.Frame]) -> None:
    path = askopenfilename()
    bounds = pd.read_csv(path)
    models = payload[0]
    main = payload[-1]
    for model in models:
        if model.type == "MLP":
            solver = Verify(bounds, model)
            short_summary_list = [f"{solver.check()} verification"]
            model.model.summary(print_fn=lambda x: short_summary_list.append(x))
            short_summary_str = "\n".join(short_summary_list)
            ttk.Label(
                main,
                text=short_summary_str,
                font=("Times New Roman", 12),
            ).grid(column=1, row=11)
