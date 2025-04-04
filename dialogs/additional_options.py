import tkinter as tk, strings, custom_ui
from tkinter import ttk, messagebox
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

    def reset_options_to_default():
        confirmation = messagebox.askyesno(strings.lang.reset_to_default, strings.lang.reset_to_default_confirmation, icon = "warning", default = "no", parent = window)

        if confirmation:
            additional_options_vars[0].set(True)
            additional_options_vars[1].set(True)
            additional_options_vars[2].set(True)
            additional_options_vars[3].set(False)

    hide_autorun = custom_ui.Checkbutton(window, text = strings.lang.hide_autorun, command = save_additional_preferences, variable = additional_options_vars[0])
    hide_autorun.pack(anchor = "w")

    hide_vl_icon = custom_ui.Checkbutton(window, text = strings.lang.hide_vl_icon, command = save_additional_preferences, variable = additional_options_vars[1])
    hide_vl_icon.pack(anchor = "w")
    
    backup_existing_autorun = custom_ui.Checkbutton(window, text = strings.lang.backup_existing_autorun, command = save_additional_preferences, variable = additional_options_vars[2])
    backup_existing_autorun.pack(anchor = "w")
    
    refresh_volume_info_without_asking = custom_ui.Checkbutton(window, text = strings.lang.refresh_volume_info_without_asking, command = save_additional_preferences, variable = additional_options_vars[3])
    refresh_volume_info_without_asking.pack(anchor = "w")

    window.update()
    style = ttk.Style()
    style.configure("Description.TLabel", wraplength = int(window.winfo_reqwidth() * 1.5))

    ttk.Label(window, text = strings.lang.hide_autorun_description, style = "Description.TLabel").pack(after = hide_autorun, anchor = "w", pady = (0, preferences.get_scaled_value(8)))
    ttk.Label(window, text = strings.lang.hide_vl_icon_description, style = "Description.TLabel").pack(after = hide_vl_icon, anchor = "w", pady = (0, preferences.get_scaled_value(8)))
    ttk.Label(window, text = strings.lang.backup_existing_autorun_description, style = "Description.TLabel").pack(after = backup_existing_autorun, anchor = "w", pady = (0, preferences.get_scaled_value(8)))
    ttk.Label(window, text = strings.lang.refresh_volume_info_without_asking_description, style = "Description.TLabel").pack(after = refresh_volume_info_without_asking, anchor = "w", pady = (0, preferences.get_scaled_value(8)))

    buttons = ttk.Frame(window)
    buttons.pack(fill = "x", pady = preferences.get_scaled_value(16))

    custom_ui.Button(buttons, text = strings.lang.reset_to_default, command = reset_options_to_default).pack(side = "left")
    custom_ui.Button(buttons, text = strings.lang.ok, default = "active", command = remove_additional_options_vars_traces).pack(side = "right")

    window.protocol("WM_DELETE_WINDOW", remove_additional_options_vars_traces)
    window.unbind("<Escape>")
    window.bind("<Escape>", lambda event: remove_additional_options_vars_traces())
    window.resizable(False, False)
    window.focus_set()