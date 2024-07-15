config = {
    "file_path": "",
    "y_header": "label",
    "ensemble_method": "stacking",
    "models": [
        {
            "type": "LogisticRegression",
            "params": {
                "tol": 0.0001,
                "C": 1.0,
                "max_iter": 50,
            },
        },
        {
            "type": "LogisticRegression",
            "params": {
                "tol": 0.0001,
                "C": 5.0,
                "max_iter": 50,
            },
        },
    ],
    "final_estimator": {
        "type": "LogisticRegression",
        "params": {
            "tol": 0.001,
            "C": 2.0,
            "max_iter": 250,
        },
    },
    "random_state": 42,
}
