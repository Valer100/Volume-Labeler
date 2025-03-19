import tkinter as tk, strings, custom_ui
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from utils import preferences

def show(error: str):
    window = custom_ui.Toplevel()
    window.title(strings.lang.error)
    window.configure(padx = preferences.get_scaled_value(16), pady = 0)

    header = ttk.Frame(window)
    header.pack(anchor = "w", pady = (preferences.get_scaled_value(8), preferences.get_scaled_value(16)))

    ttk.Label(header, text = "\ue7ba ", font = ("Segoe UI", 17), padding = (0, 5, 0, 0)).pack(side = "left")
    ttk.Label(header, width = 25, text = strings.lang.error, font = ("Segoe UI Semibold", 17)).pack(side = "left")

    error_text = ScrolledText(window, width = 60, height = 7, wrap = "word", background = custom_ui.colors.entry_bg,
                                 foreground = custom_ui.colors.fg, selectbackground = custom_ui.colors.entry_select,
                                 selectforeground = "#ffffff", highlightthickness = 1, relief = "solid",
                                 highlightbackground = custom_ui.colors.entry_bd, highlightcolor = custom_ui.colors.entry_bd,
                                 border = 0, font = ("Consolas", 10))
    error_text.pack()
    error_text.insert("1.0", error)
    error_text.configure(state = "disabled")

    def copy_traceback():
        window.clipboard_append(error)
        messagebox.showinfo(parent = window, title = strings.lang.copy_traceback, message = strings.lang.copy_traceback_success)

    buttons = ttk.Frame(window)
    buttons.pack(pady = preferences.get_scaled_value(16), fill = "x")

    custom_ui.Button(buttons, text = strings.lang.copy_traceback, command = copy_traceback).pack(side = "left")
    custom_ui.Button(buttons, text = strings.lang.ok, default = "active", command = window.destroy).pack(side = "right", padx = (preferences.get_scaled_value(8), 0))

    window.resizable(False, False)
    window.focus_set()