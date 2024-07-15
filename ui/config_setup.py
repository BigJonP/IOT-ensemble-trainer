import json
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from typing import Tuple

from model_infra.pipeline import run_pipeline
from utils import fetch_headers


def launch_ui_config(main: tk.Frame, config: dict):
    ttk.Label(
        main, text="Select Data File :", font=("Times New Roman", 12), justify="left"
    ).grid(column=0, row=0, padx=10, pady=5)
    y = tk.StringVar()
    y_hat_cc = ttk.Combobox(main, width=27, textvariable=y)
    y_hat_cc.grid(column=1, row=1)

    data_payload = (y_hat_cc, config)
    tk.Button(main, text="Browse", command=lambda: select_data(data_payload)).grid(
        column=1, row=0
    )

    ttk.Label(
        main, text="Select y-hat :", font=("Times New Roman", 12), justify="left"
    ).grid(column=0, row=1, padx=10, pady=5)

    ttk.Label(
        main,
        text="Choose Ensemble Method :",
        font=("Times New Roman", 12),
        justify="left",
    ).grid(column=0, row=2, padx=10, pady=5)
    ensemble_method = tk.StringVar()
    method_cc = ttk.Combobox(main, width=27, textvariable=ensemble_method)
    method_cc["values"] = ("Bagging", "Stacking", "Adaboosting")
    method_cc.grid(column=1, row=2)

    config_text = ttk.Label(
        main,
        text="Config: ",
        font=("Times New Roman", 12),
        justify="left",
    )
    config_text.grid(column=0, row=3, padx=10, pady=5)

    tk.Button(
        main,
        text="Upload Model Config",
        command=lambda: update_config((config, config_text)),
    ).grid(column=1, row=3)

    ttk.Label(
        main,
        text="Final Estimator Type:",
        font=("Times New Roman", 12),
        justify="left",
    ).grid(column=0, row=5, padx=10, pady=5)
    tk.Text(main, height=8, width=72).grid(column=1, row=5)

    ttk.Label(
        main,
        text="Boosting Algorithm:",
        font=("Times New Roman", 12),
        justify="left",
    ).grid(column=0, row=6, padx=10, pady=5)
    boosting_algo = tk.StringVar()
    boosting_algo_cc = ttk.Combobox(main, width=27, textvariable=boosting_algo)
    boosting_algo_cc["values"] = ("SAMME", "SAMME.R")
    boosting_algo_cc.grid(column=0, row=7)

    ttk.Label(
        main,
        text="Boosting Learning Rate:",
        font=("Times New Roman", 12),
        justify="left",
    ).grid(column=1, row=6, padx=10, pady=5)
    boosting_learning_rate = tk.StringVar()
    tk.Entry(main, width=27, textvariable=boosting_learning_rate).grid(column=1, row=7)

    ttk.Label(
        main,
        text="Boosting Number of Estimators:",
        font=("Times New Roman", 12),
        justify="left",
    ).grid(column=2, row=6, padx=10, pady=5)
    boosting_num_estimators = tk.StringVar()
    tk.Entry(main, width=27, textvariable=boosting_num_estimators).grid(column=2, row=7)

    tk.Button(
        main,
        text="Run",
        bd=3,
        bg="lightgray",
        disabledforeground="gray",
        fg="black",
        font=("Times New Roman", 12),
        command=lambda: run_pipeline(
            (
                config,
                ensemble_method.get(),
                boosting_params(
                    boosting_algo, boosting_learning_rate, boosting_num_estimators
                ),
                main,
            )
        ),
    ).grid(column=0, row=8, columnspan=2, padx=10, pady=5)


def select_data(data_payload: tuple[ttk.Combobox, dict]) -> None:
    path = askopenfilename()
    data_payload[1]["file_path"] = path
    data_payload[0]["values"] = fetch_headers(path)


def update_config(payload: Tuple[dict, tk.Frame]) -> None:
    config = payload[0]
    main = payload[-1]
    path = askopenfilename()
    with open(path, encoding="utf_8") as config_file:
        config["models"] = json.load(config_file)
    ttk.Label(
        main, text=json.dumps(config["models"], indent=4), font=("Times New Roman", 12)
    ).grid(column=0, row=4, columnspan=3)


def boosting_params(
    boosting_algo: tk.StringVar,
    boosting_learning_rate: tk.StringVar,
    boosting_n_estimators: tk.StringVar,
) -> dict:
    return {
        "algorithm": boosting_algo.get(),
        "learning_rate": float(
            boosting_learning_rate.get() if boosting_learning_rate.get() else 0.0
        ),
        "n_estimators": int(
            boosting_n_estimators.get() if boosting_n_estimators.get() else 0
        ),
    }
