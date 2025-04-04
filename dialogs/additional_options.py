import tkinter as tk, strings, custom_ui
from tkinter import ttk
from utils import preferences

window = None

def show(additional_options_vars):
    global window

    window = custom_ui.Toplevel()
    window.title(strings.lang.additional_options)
    window.configure(padx = preferences.get_scaled_value(16), pady = 0)

    header = ttk.Frame(window)
    header.pack(anchor = "w", pady = (preferences.get_scaled_value(4), preferences.get_scaled_value(8)))

    ttk.Label(header, text = "\ue713 ", font = ("Segoe UI", 17), padding = (0, 5, 0, 0)).pack(side = "left")
    ttk.Label(header, text = strings.lang.additional_options + " ", font = ("Segoe UI Semibold", 17)).pack(side = "left")

    def save_additional_preferences(): 
        preferences.additional_prefs = ""
        
        for i in range(0, len(additional_options_vars)):
            preferences.additional_prefs += str(int(additional_options_vars[i].get()))
        
        preferences.save_settings()

    def remove_additional_options_vars_traces():
        for variable in additional_options_vars:
            variable.trace_remove("write", variable.trace_info()[0][1])

        window.destroy()

    custom_ui.Checkbutton(window, text = strings.lang.hide_autorun, command = save_additional_preferences, variable = additional_options_vars[0]).pack(anchor = "w")
    custom_ui.Checkbutton(window, text = strings.lang.hide_vl_icon, command = save_additional_preferences, variable = additional_options_vars[1]).pack(anchor = "w")
    custom_ui.Checkbutton(window, text = strings.lang.backup_existing_autorun, command = save_additional_preferences, variable = additional_options_vars[2]).pack(anchor = "w")
    custom_ui.Checkbutton(window, text = strings.lang.refresh_volume_info_without_asking, command = save_additional_preferences, variable = additional_options_vars[3]).pack(anchor = "w")

    custom_ui.Button(window, text = strings.lang.ok, default = "active", command = remove_additional_options_vars_traces).pack(pady = preferences.get_scaled_value(16), anchor = "e")

    window.protocol("WM_DELETE_WINDOW", remove_additional_options_vars_traces)
    window.unbind("<Escape>")
    window.bind("<Escape>", lambda event: remove_additional_options_vars_traces())
    window.resizable(False, False)
    window.focus_set()