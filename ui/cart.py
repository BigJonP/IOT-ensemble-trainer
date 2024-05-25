import tkinter as tk


def add_selection(frame: tk.Frame, model_name: str):
    tk.Label(frame, text=model_name, font=("Arial Bold", 10)).pack()
