import tkinter as tk

from config import config
from ui.model_selection import launch_model_selection
from model_infra.model import Model
from model_infra.nnverify import NNVerify


def start_ui():
    root = tk.Tk()
    root.geometry("700x550")
    root.title("IOT Ensemble Trainer")

    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP)

    bot_frame = tk.Frame(root)
    bot_frame.pack(side=tk.BOTTOM)

    launch_model_selection(top_frame, bot_frame, config)

    root.mainloop()


if __name__ == "__main__":
    # start_ui()

    test_model = Model(config)
    test_model.train_model()
    verify_obj = NNVerify(test_model)
    verify_obj.prepare_postcondition()
