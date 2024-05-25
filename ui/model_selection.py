import tkinter as tk
from ui.cart import add_selection


def launch_model_selection(frame: tk.Frame, cart_frame: tk.Frame, config: dict):
    options = [
        "RANDOM_FORREST",
        "SVM",
        "MLP",
    ]
    clicked = tk.StringVar()
    clicked.set("RANDOM_FORREST")

    drop = tk.OptionMenu(frame, clicked, *options)
    drop.pack()

    def add_model():
        if config["selected_models"][str(clicked.get())]:
            return

        config["selected_models"][clicked.get()] = True
        add_selection(cart_frame, clicked.get())

        print(config)

    tk.Button(frame, text="ADD", command=add_model).pack()
