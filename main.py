import tkinter as tk

from config import config
from ui.config_setup import launch_ui_config


def launch_ui():

    root = tk.Tk()
    pad = 15
    root.geometry(
        f"{root.winfo_screenwidth() - pad}x{root.winfo_screenheight() - pad}+0+0"
    )
    root.title("IOT Ensemble Trainer")
    _geom = "200x200+0+0"

    def toggle_geom():
        nonlocal _geom
        geom = root.winfo_geometry()
        root.geometry(_geom)
        _geom = geom

    root.bind("<Escape>", toggle_geom)

    main = tk.Frame(root)
    main.pack(side=tk.TOP)

    launch_ui_config(main, config)

    root.mainloop()


if __name__ == "__main__":
    launch_ui()
